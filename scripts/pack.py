#!/usr/bin/env python3
"""Validate, audition, and install the Boris CESP pack (Python 3, no packages)."""
import argparse
import hashlib
import json
from pathlib import Path
import random
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
CATEGORIES = {'session.start', 'task.acknowledge', 'task.complete', 'task.error',
              'input.required', 'resource.limit', 'user.spam', 'session.end', 'task.progress'}


def validate(decode=False):
    manifest = json.loads((ROOT / 'openpeon.json').read_text())
    def require(condition, message):
        if not condition:
            raise ValueError(message)
    require(manifest['cesp_version'] == '1.0', 'Unsupported CESP version')
    require(re.fullmatch(r'[a-z0-9_-]+', manifest['name']), 'Invalid pack name')
    require(re.fullmatch(r'\d+\.\d+\.\d+', manifest['version']), 'Invalid version')
    require(1 <= len(manifest['display_name']) <= 128, 'Invalid display name')
    require(len(manifest.get('description', '')) <= 256, 'Description too long')
    require(manifest['categories'], 'No categories')
    files = set()
    if decode and not shutil.which('ffmpeg'):
        raise ValueError('--decode requires ffmpeg')
    for category, entry in manifest['categories'].items():
        require(category in CATEGORIES, f'Unknown category: {category}')
        require(entry['sounds'], f'Empty category: {category}')
        for sound in entry['sounds']:
            name = sound['file']
            require(re.fullmatch(r'sounds/[a-zA-Z0-9_-][a-zA-Z0-9._-]*\.mp3', name), f'Unsafe path: {name}')
            path = ROOT / name
            require(not path.is_symlink(), f'Symlink: {name}')
            data = path.read_bytes()
            require(0 < len(data) <= 1_000_000, f'Invalid size: {name}')
            require(data.startswith(b'ID3') or (len(data) > 1 and data[0] == 255 and data[1] & 224 == 224), f'Not MP3: {name}')
            require(hashlib.sha256(data).hexdigest() == sound['sha256'], f'Checksum mismatch: {name}')
            require(isinstance(sound['label'], str) and sound['label'].strip(), f'Missing label: {name}')
            if decode and name not in files:
                subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(path), '-f', 'null', '-'], check=True)
            files.add(name)
    require(files == {p.relative_to(ROOT).as_posix() for p in (ROOT / 'sounds').glob('*.mp3')}, 'Unreferenced audio files')
    total = sum((ROOT / name).stat().st_size for name in files)
    require(total <= 50_000_000, 'Pack exceeds 50 MB')
    print(f"Valid: {manifest['name']}, {len(manifest['categories'])} categories, {len(files)} clips, {total:,} bytes")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('validate').add_argument('--decode', action='store_true', help='Fully decode each MP3 with ffmpeg')
    play = sub.add_parser('play', help='Play one random clip locally; no PeonPing needed')
    play.add_argument('category', nargs='?', default='task.complete', choices=sorted(CATEGORIES))
    install = sub.add_parser('install', help='Install and activate in an existing PeonPing installation')
    install.add_argument('--force', action='store_true', help='Replace an existing Boris pack')
    args = parser.parse_args()
    manifest = validate(getattr(args, 'decode', False))
    if args.command == 'play':
        sounds = manifest['categories'].get(args.category, {}).get('sounds', [])
        if not sounds:
            raise ValueError(f'No sounds for {args.category}')
        sound = random.choice(sounds)
        path = str(ROOT / sound['file'])
        for executable, flags in [('afplay', []), ('ffplay', ['-nodisp', '-autoexit', '-loglevel', 'error']), ('mpg123', ['-q'])]:
            if shutil.which(executable):
                print(sound['label'], flush=True)
                subprocess.run([executable, *flags, path], check=True)
                break
        else:
            raise ValueError('Install ffmpeg or mpg123, or use the browser preview.')
    elif args.command == 'install':
        if not shutil.which('peon'):
            raise ValueError('PeonPing is not installed. Follow README.md setup, then rerun this command.')
        # Stage only pack assets: install-local copies the entire source directory.
        with tempfile.TemporaryDirectory(prefix='boris-pack-') as temporary:
            staging = Path(temporary)
            for filename in ('openpeon.json', 'CREDITS.md'):
                shutil.copy2(ROOT / filename, staging / filename)
            shutil.copytree(ROOT / 'sounds', staging / 'sounds')
            subprocess.run(['peon', 'packs', 'install-local', str(staging), *(['--force'] if args.force else [])], check=True)
        subprocess.run(['peon', 'packs', 'use', manifest['name']], check=True)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
        print(f'Error: {error}', file=sys.stderr)
        sys.exit(1)

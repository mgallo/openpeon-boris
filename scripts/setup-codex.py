#!/usr/bin/env python3
"""Set up Homebrew PeonPing for Boris and register this repo's Codex hooks."""
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys

from pack import ROOT, validate


def main():
    validate()
    prefix = Path(subprocess.check_output(['brew', '--prefix', 'peon-ping'], text=True).strip())
    brew_prefix = Path(subprocess.check_output(['brew', '--prefix'], text=True).strip())
    libexec = prefix / 'libexec'
    adapter = libexec / 'adapters/codex.sh'
    if not adapter.is_file():
        raise ValueError('Install PeonPing first: brew install PeonPing/tap/peon-ping')
    data = Path.home() / '.openpeon'
    (data / 'packs').mkdir(parents=True, exist_ok=True)
    for name in ('peon.sh', 'scripts', 'adapters', 'VERSION', 'docs'):
        target = data / name
        if not target.exists() and not target.is_symlink() and (libexec / name).exists():
            target.symlink_to(libexec / name, target_is_directory=(libexec / name).is_dir())
    config = data / 'config.json'
    if not config.exists():
        defaults = json.loads((libexec / 'config.json').read_text())
        defaults.update(default_pack='boris', desktop_notifications=False, terminal_tab_title=False)
        config.write_text(json.dumps(defaults, indent=2) + '\n')
    env = dict(os.environ, CLAUDE_PEON_DIR=str(data))
    subprocess.run([sys.executable, str(ROOT / 'scripts/pack.py'), 'install', '--force'], env=env, check=True)
    events = ['SessionStart', 'Stop', 'PermissionRequest', 'PreCompact', 'UserPromptSubmit']
    settings = {'data_dir': str(data), 'adapter': str(adapter),
                'bin_dir': str(brew_prefix / 'bin'), 'events': events}
    (ROOT / '.runtime').mkdir(exist_ok=True)
    (ROOT / '.runtime/codex-peon.json').write_text(json.dumps(settings, indent=2) + '\n')
    hooks_path = ROOT / '.codex/hooks.json'
    hooks_path.parent.mkdir(exist_ok=True)
    project_config = hooks_path.parent / 'config.toml'
    if not project_config.exists():
        project_config.write_text('# Boris sound hooks are configured alongside this file in hooks.json.\n')
    document = json.loads(hooks_path.read_text()) if hooks_path.exists() else {'hooks': {}}
    # Use the stable Homebrew executable path, not a versioned Python Cellar path.
    command = shlex.join([str(brew_prefix / 'bin/python3'), str(ROOT / 'scripts/codex-hook.py')])
    for event in events:
        entries = document.setdefault('hooks', {}).setdefault(event, [])
        if not any(hook.get('command') == command for entry in entries for hook in entry.get('hooks', [])):
            entries.append({'hooks': [{'type': 'command', 'command': command, 'async': True, 'timeout': 20}]})
    rendered = json.dumps(document, indent=2) + '\n'
    if hooks_path.exists() and hooks_path.read_text() != rendered:
        shutil.copy2(hooks_path, hooks_path.with_suffix('.json.bak'))
    hooks_path.write_text(rendered)
    print(f'Codex hooks installed: {hooks_path}')
    print('Restart Codex in this trusted workspace, then use /hooks to review and trust the Boris hooks.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(f'Setup failed: {error}', file=sys.stderr)
        sys.exit(1)

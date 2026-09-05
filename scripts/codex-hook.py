#!/usr/bin/env python3
"""Forward Codex lifecycle JSON to the installed PeonPing adapter, silently."""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent


def main():
    settings = json.loads((ROOT / '.runtime/codex-peon.json').read_text())
    if len(sys.argv) == 3 and sys.argv[1] == '--test':
        payload = {'hook_event_name': sys.argv[2], 'cwd': str(ROOT),
                   'session_id': f'boris-test-{os.getpid()}', 'permission_mode': 'default'}
    else:
        payload = json.load(sys.stdin)
    if payload.get('hook_event_name') not in settings['events']:
        return
    env = dict(os.environ, CLAUDE_PEON_DIR=settings['data_dir'])
    # Desktop apps may start with a minimal PATH.
    env['PATH'] = settings['bin_dir'] + os.pathsep + env.get('PATH', '/usr/bin:/bin')
    subprocess.run(['/bin/bash', settings['adapter']], input=json.dumps(payload),
                   text=True, env=env, stdout=subprocess.DEVNULL, check=True, timeout=15)


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        # An audio failure must never block a coding task or emit hook decisions.
        print(f'Boris notification: {error}', file=sys.stderr)
        if '--test' in sys.argv:
            sys.exit(1)

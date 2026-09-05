# Optional workspace setup

This is a developer convenience for a clone of this repository. Installing
the Boris sound pack does not require these scripts. Run commands from the
repository root.

PeonPing can be installed and connected specifically to this workspace with:

```sh
brew install PeonPing/tap/peon-ping
python3 scripts/setup-codex.py
```

The setup script installs Boris in `~/.openpeon`, selects it, and writes
project hooks to `.codex/hooks.json`. It uses the Homebrew Codex adapter and
preserves existing hook entries. Machine-specific paths are saved under the
ignored `.runtime/` directory; rerun setup after moving or cloning this repo.
The general `peon-ping-setup` command is not needed for this Codex-only setup.
Audio starts at 50% volume; desktop overlays are disabled on a fresh setup.

**Restart Codex or open a new session in this trusted workspace** after setup.
Run `/hooks` and review/trust the five entries pointing to `scripts/codex-hook.py`.
Codex skips new or changed hooks until you trust their exact definitions; workspace
trust alone is not enough. Then ask it to “Reply with OK” to hear a completion
quote. In the terminal:

```sh
codex -C .
```

Test the same hook directly without starting a model request:

```sh
python3 scripts/codex-hook.py --test Stop
python3 scripts/codex-hook.py --test PermissionRequest
peon preview task.complete
```

Registered events: `SessionStart` → greeting, `Stop` → completion,
`PermissionRequest` → input required, `PreCompact` → resource limit, and
`UserPromptSubmit` → acknowledgement / rapid-prompt detection. Acknowledgement
audio remains off by default. Hooks run asynchronously and emit no decisions.
This uses [Codex lifecycle hooks](https://learn.chatgpt.com/docs/hooks), available
and enabled in the locally tested Codex CLI 0.153.4. It does not use the older,
completion-only `notify` setting. Project hooks require workspace trust.

Controls: `peon pause`, `peon resume`, `peon volume 0.5`, and `peon status`.
To disconnect, remove the entries pointing to `scripts/codex-hook.py` from
`.codex/hooks.json` and restart Codex.


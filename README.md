# Boris — Dai, dai, dai!

A PeonPing sound pack with 16 original Italian clips from **Boris**: René,
Duccio, Stanis, and the crew reacting to your coding sessions. Contains explicit
language. All MP3s are included; no audio downloads or Python packages needed.

## Listen now

From this directory, run:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

Open http://localhost:8765 for the soundboard, grouped by event, with playback
and volume controls. Stop the server with Ctrl+C.

Or play a random completion clip directly (macOS uses built-in `afplay`; Linux
requires `ffplay` or `mpg123`):

```sh
python3 scripts/pack.py play task.complete
```

## Install in PeonPing

Requires Python 3 and a current [PeonPing installation](https://github.com/PeonPing/peon-ping#install)
with `peon packs install-local`. On macOS, install and register PeonPing first:

```sh
brew install PeonPing/tap/peon-ping
peon-ping-setup
```

Then, from this repository:

```sh
python3 scripts/pack.py install
peon preview task.complete
```

The script validates the pack, installs only its manifest, audio, and credits,
and selects `boris` as the active pack. It uses PeonPing's own installation and
configuration commands. To replace an earlier Boris installation, run
`python3 scripts/pack.py install --force`.

Agent hook setup belongs to PeonPing; installing this pack alone does not
register an agent adapter. Follow its documentation for your editor. Events
depend on the adapter: not every editor emits every category.

## Codex integration in this repo

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

## Event mapping

| Category | Clips |
| --- | --- |
| `session.start` | Dai, dai, dai! / Apri tutto |
| `task.acknowledge` | Apri tutto / Dai, dai, dai! |
| `task.complete` | Mito, genio / Bucio de culo / Sticazzi |
| `task.error` | A cazzo di cane / Cagna maledetta / È stato stocazzo / Sei molto italiano |
| `input.required` | Ce se capisce e ’nce se capisce / Ma tu chi cazzo sei? |
| `resource.limit` | La qualità c’ha rotto er cazzo / Attaccati al cazzo |
| `user.spam` | Muto / Non mi devi rompere i coglioni |
| `session.end` | Sticazzi |
| `task.progress` | Se me vedi distratto… |

`task.acknowledge` is disabled by default in PeonPing. `session.end` and
`task.progress` are optional CESP categories; current built-in PeonPing hooks
do not trigger them. They remain available for previews and compatible players.

## Validate

```sh
python3 scripts/pack.py validate
python3 scripts/pack.py validate --decode  # also requires ffmpeg
```

Checks manifest fields, category names, safe paths, MP3 signatures, per-file
and total size limits, SHA-256 hashes, and unreferenced audio. `--decode` also
fully decodes every unique recording to detect broken audio.

The pack follows [CESP 1.0](https://openpeon.com/spec). Clips are unchanged,
approximately 0.7–6.8 seconds long. See [CREDITS.md](CREDITS.md) for pinned
source provenance and audio rights. No registry publication is configured.

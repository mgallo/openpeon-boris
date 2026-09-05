# Boris — Dai, dai, dai!

16 Italian voice clips from **Boris**, ready for [PeonPing](https://github.com/PeonPing/peon-ping):
René, Duccio, Stanis, and the crew reacting to your coding sessions.
Contains explicit language.

## Install

Already have PeonPing configured for your editor?

1. Download **[boris-1.0.0.zip](https://github.com/mgallo/openpeon-boris/releases/download/v1.0.0/boris-1.0.0.zip)**.
2. Extract it. You will get a folder named `boris`.
3. Open a terminal in the folder containing `boris` and run:

   ```sh
   peon packs install-local ./boris
   peon packs use boris
   ```

That's it. The ZIP contains only the manifest, audio, and credits.
No cloning or project Python scripts required. PeonPing manages its own runtime dependencies.

To replace an existing Boris installation, use
`peon packs install-local ./boris --force`, then `peon packs use boris`.

Optional preview:

```sh
peon preview task.complete
```

Boris is not yet listed in the OpenPeon registry. Until it is accepted, use the
ZIP above. After registration, installation will also be available with
`peon packs use --install boris`.

## New to PeonPing?

Install PeonPing once, then configure its integration for your editor using the
[official setup instructions](https://github.com/PeonPing/peon-ping#install).
With Homebrew on macOS or Linux:

```sh
brew install PeonPing/tap/peon-ping
peon-ping-setup
```

Follow the adapter instructions for your editor, then install Boris above.
The pack supplies sounds; PeonPing and its editor adapter trigger playback.
Events available depend on the adapter.

## Controls

```sh
peon pause
peon resume
peon volume 0.5
peon status
```

## What you will hear

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

## Development

The source repo also includes a browser soundboard and optional Python tools
for validation, local playback, and release packaging. These tools are not part
of the downloadable sound pack.

- [Development and release guide](docs/development.md)
- [Optional workspace setup](docs/local-setup.md)
- [Audio credits and provenance](CREDITS.md)

The pack follows [CESP 1.0](https://openpeon.com/spec). Clips are unchanged,
approximately 0.7–6.8 seconds long. All audio rights remain with their respective owners.

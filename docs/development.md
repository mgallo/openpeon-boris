# Development and releases

Run these commands from the repository root. Python 3 is used for maintainer
tools only; people installing the release use PeonPing directly.

## Listen locally

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

Open http://localhost:8765 for the soundboard, with playback and volume controls.
Stop the server with Ctrl+C.

Or play a random completion clip:

```sh
python3 scripts/pack.py play task.complete
```

macOS uses `afplay`; Linux requires `ffplay` or `mpg123`.

## Validate

```sh
python3 scripts/pack.py validate
python3 scripts/pack.py validate --decode
```

Validation checks manifest fields, category names, safe paths, MP3 signatures,
size limits, SHA-256 hashes, and unreferenced audio. `--decode` additionally
requires ffmpeg and fully decodes every recording.

To install from a development checkout, `python3 scripts/pack.py install`
validates and stages only the pack files before calling PeonPing. Add `--force`
to replace an existing installation.

## Build a release

```sh
python3 scripts/pack.py build
```

This validates the pack and creates three files in the ignored `dist/` folder:

- `boris-<version>.zip`: a `boris/` folder with `openpeon.json`, `CREDITS.md`, and
  the 16 audio files. No scripts, local configuration, or Git metadata.
- `SHA256SUMS`: SHA-256 checksum of the ZIP.
- `registry-entry.json`: metadata for an OpenPeon registry submission.

The ZIP is reproducible: unchanged inputs produce an identical checksum.
The registry entry uses the build date; retain the original `added` date when
updating an existing registry listing. The sound count follows the registry's
CI convention of counting unique audio files.

## Publish

Update `openpeon.json` and the README download link for each new version. Build
and test the archive before tagging the committed source. For version 1.0.0:

```sh
git tag v1.0.0
git push origin main v1.0.0
```

The release workflow checks that the tag matches the manifest version, validates
and builds the pack, then publishes the ZIP and checksum using
`docs/release-notes.md`. It uses GitHub Actions authentication and does not need
a personal access token. Existing releases are never overwritten.
Check that the workflow succeeds and the README download URL works.
GitHub's automatic source archives contain developer files and are not the install ZIP.

## OpenPeon registry

Follow the [registry contribution guide](https://github.com/PeonPing/registry/blob/main/CONTRIBUTING.md):

1. Publish the tag so its manifest and audio are publicly accessible.
2. Fork `PeonPing/registry` and insert `dist/registry-entry.json` into the `packs`
   array in `index.json`, preserving alphabetical order by `name`.
3. Open a PR and let the registry's validation and review run.

The generated entry references `mgallo/openpeon-boris` at `v<version>` and pins
the manifest SHA-256. It uses the `community` trust tier. It omits the optional
license field because no license for the source recordings was supplied; see
[CREDITS.md](../CREDITS.md). Disclose the explicit language and audio provenance
in the submission so registry maintainers can assess it under their rules.

Only after the listing is merged and published should the README present
`peon packs use --install boris` as an available installation method.

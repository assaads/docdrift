# docdrift

Fail CI when your docs drift from your code — one manifest, any stack.

`docdrift` extracts a **surface** from your code (CLI commands, file stems, regex
captures, …) and fails the build when any element of that surface is missing from
the docs you declare. It ships with extractors for [Typer](https://typer.tiangolo.com/),
[Click](https://click.palletsprojects.com/), argparse, and two generic escape hatches
(`files`, `regex`), and is designed so new extractors drop in without touching the
checker, CLI, or manifest schema.

---

## Install

Run it once (no install needed) with `uvx`:

```bash
uvx --from git+https://github.com/assaads/docdrift@main docdrift --help
```

Or, in a Python repo that uses `uv`:

```bash
uv add docdrift               # then: uv run docdrift ...
```

**Python repos using pytest (recommended):** adding `docdrift` as a dev dependency
also enables the `pytest11` plugin — once a `.docdrift.yml` exists at the repo root,
`pytest` auto-runs a `test_docdrift` item, so docs drift is caught locally on every
test run, not only in CI.

## Quick start

```bash
docdrift init --stack typer   # writes a starter .docdrift.yml
$EDITOR .docdrift.yml         # point module/app at your CLI, set the program name
docdrift check                # exits 1 if any surface element is missing from the docs
```

The starter manifest is intentionally a stub — `init` gets you the right shape; you
edit the dotted module path, app attribute, and `format` program name before it works.

## CLI

`docdrift check` — Run every source's extractor against the declared docs and exit
`1` if any surface literal is missing. Pass `--config PATH` (repeatable, defaults to
`.docdrift.yml`) to check additional manifests. Pass `--json` for machine-readable
output.

`docdrift init --stack <typer|click|argparse|files|regex>` — Write a starter
`.docdrift.yml` for the given stack into the current directory. The starter is a
scaffold; edit the placeholder values before running `check`.

`docdrift list` — Print the extracted surface per source (`[name] ['cmd-a', ...]`).
Debug aid for seeing what the extractor actually resolves; never exits non-zero.

## Manifest schema

```yaml
version: 1                       # required, must be 1
docs: [README.md]                # required at top-level (overridable per-source)
sources:                         # required, list of Source
  - name: cli                    # optional, defaults to extractor name
    extractor: typer             # required, a registered extractor id
    format: 'PROG {item}'        # required, template; {item} = one surface element
    docs: [README.md]            # optional, overrides top-level docs for this source
    # ...extractor-specific fields (module/app, obj, factory, path, regex)...
```

`{item}` is substituted with one surface element at a time (e.g. a CLI command name
or a file stem). The resulting literal is searched for verbatim in every listed doc;
if it's missing from all of them, that's drift.

`Source` is an **open** pydantic model: any extra keys you put on a source are
passed to that source's extractor. Each extractor documents its own fields below.
Adding a new extractor never changes `Manifest`, `checker`, or the CLI.

## Examples — one per Phase-1 extractor

### typer

Extracts command names from a `typer.Typer()` app, honoring `@app.command(name=...)`.

```yaml
version: 1
docs: [README.md]
sources:
  - name: cli
    extractor: typer
    module: PKG.cli      # dotted path to the module holding the app
    app: app             # attribute name of the typer.Typer() instance
    format: 'PROG {item}'
```

### click

Extracts command names from a `click.Group`.

```yaml
version: 1
docs: [README.md]
sources:
  - name: cli
    extractor: click
    obj: PKG.cli:group   # module:attribute of the click.Group
    format: 'PROG {item}'
```

### argparse

Extracts subcommand names from an `ArgumentParser` built by a factory function.

```yaml
version: 1
docs: [README.md]
sources:
  - name: cli
    extractor: argparse
    factory: PKG.cli:build_parser   # module:function returning ArgumentParser
    format: 'PROG {item}'
```

### files

Generic escape hatch: globs files; `item` = file stem. Use when no language
extractor fits, or to assert that a list of files exists.

```yaml
version: 1
docs: [README.md]
sources:
  - name: files
    extractor: files
    path: 'src/**/*.py'   # glob; item = file stem
    format: '{item}'
```

### regex

Generic escape hatch: captures symbols from source files via regex (group 1 = item).

```yaml
version: 1
docs: [README.md]
sources:
  - name: fns
    extractor: regex
    path: 'src/cli.py'
    regex: '^def (\w+)\b'   # group 1 = item
    format: 'PROG {item}'
```

## CI opt-in

### Reusable workflow (once `assaads/docdrift` is tagged)

Add a job to your `.github/workflows/ci.yml` that calls the shared workflow:

```yaml
jobs:
  docs-drift:
    uses: assaads/docdrift/.github/workflows/docs-drift.yml@v0.1
```

### Fallback (pinned to `@main` until the repo is tagged `v0.1`)

Before the shared repo exists / is tagged, drop this verbatim into
`.github/workflows/docs-drift.yml` in the consuming repo:

```yaml
name: docs-drift
on: [push, pull_request]
permissions: { contents: read }
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - uses: astral-sh/setup-uv@v4
      - run: uvx --from "git+https://github.com/assaads/docdrift@main" docdrift check
```

### pytest plugin path (Python repos)

`pip install docdrift` (or `uv add docdrift`) registers a `pytest11` plugin. With a
`.docdrift.yml` at the repo root, `pytest` auto-collects a `test_docdrift` item that
runs the same check as `docdrift check`. No workflow edits required — drift fails your
existing test suite.

## License

MIT

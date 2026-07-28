# Stack detection markers + manifest templates

Detection uses a **positive marker** (a content pattern), never mere file presence.

## Phase 1 extractors (shipped)

### typer
- **Marker (positive):** a `.py` file containing `import typer` (or `from typer import`) AND `typer.Typer(`.
- **Manifest:**
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
- **Marker (positive):** a `.py` file containing `click.Group(` or `@cli.group(` / `@click.group(`.
- **Manifest:**
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
- **Marker (positive):** a `.py` file containing `add_subparsers(`.
- **Manifest:**
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
- **Marker (positive):** none (this is the generic escape hatch). Use when no language extractor fits, or to assert a list of files exists.
- **Manifest:**
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
- **Marker (positive):** none (escape hatch). Use to capture symbols from source files.
- **Manifest:**
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

## Phase 2-4 extractors (planned, not yet shipped)

- **package-json** (Phase 2, TS/JS): marker `package.json` with a `bin` or `exports` field. Extractor: `package-json`.
- **cli-help** (Phase 2/3, TS-JS / Go-Rust): marker `package.json`+`bin` OR `go.mod`/`Cargo.toml`; runs `<cmd> --help`, parses `Commands:`/`Available Commands:`. Extractor: `cli-help` (with `parse: regex` escape hatch).
- **compose-services** (Phase 4, Infra): marker `docker-compose.y*ml`; item = `services:` keys. Extractor: `compose-services`.
- **terraform-modules** (Phase 4, Infra): marker `*.tf`; regex `module\s+"([^"]+)"\s*\{`. Extractor: `terraform-modules`.
- **ansible-roles** (Phase 4, Infra): marker a `roles/` directory; item = subdir names. Extractor: `ansible-roles`.

Later phases add an extractor class + `@register`, a fixture + test, and an entry here. No change to `Manifest`/`checker`/`cli` — that is the point of the open `Source` + registry design.

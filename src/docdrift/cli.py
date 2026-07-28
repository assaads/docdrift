from __future__ import annotations

from pathlib import Path

import typer

from docdrift import checker as checker_mod
from docdrift import config as config_mod
from docdrift import ctx as ctx_mod

app = typer.Typer(name="docdrift", no_args_is_help=True, add_completion=False)

_TEMPLATES = {
    "typer": (
        "version: 1\ndocs: [README.md]\nsources:\n"
        "  - name: cli\n    extractor: typer\n    module: PKG.cli\n    app: app\n"
        "    format: 'PROG {item}'\n"
    ),
    "click": (
        "version: 1\ndocs: [README.md]\nsources:\n"
        "  - name: cli\n    extractor: click\n    obj: PKG.cli:group\n"
        "    format: 'PROG {item}'\n"
    ),
    "argparse": (
        "version: 1\ndocs: [README.md]\nsources:\n"
        "  - name: cli\n    extractor: argparse\n    factory: PKG.cli:build_parser\n"
        "    format: 'PROG {item}'\n"
    ),
    "files": (
        "version: 1\ndocs: [README.md]\nsources:\n"
        "  - name: files\n    extractor: files\n    path: 'src/**/*.py'\n"
        "    format: '{item}'\n"
    ),
    "regex": (
        "version: 1\ndocs: [README.md]\nsources:\n"
        "  - name: fns\n    extractor: regex\n    path: 'src/cli.py'\n"
        "    regex: '^def (\\w+)\\b'\n    format: 'PROG {item}'\n"
    ),
}


@app.command()
def check(
    config: list[Path] = typer.Option([".docdrift.yml"], "--config"),  # noqa: B008
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    """Fail (exit 1) if any source's surface is missing from the docs."""
    manifest = config_mod.load_first(config)
    report = checker_mod.run(manifest, ctx_mod.make_ctx(Path.cwd()))
    typer.echo(report.render(as_json=json_output))
    raise typer.Exit(code=1 if report.has_drift() else 0)


@app.command()
def init(
    stack: str = typer.Option("files", "--stack", help="typer|click|argparse|files|regex"),
    force: bool = typer.Option(False, "--force", help="overwrite an existing .docdrift.yml"),
) -> None:
    """Write a starter .docdrift.yml for the given stack."""
    tmpl = _TEMPLATES.get(stack)
    if tmpl is None:
        raise typer.BadParameter(f"unknown stack {stack!r}; choose from {sorted(_TEMPLATES)}")
    target = Path(".docdrift.yml")
    if target.exists() and not force:
        raise typer.BadParameter(".docdrift.yml already exists — pass --force to overwrite")
    target.write_text(tmpl, encoding="utf-8")
    typer.echo(f"wrote .docdrift.yml (stack={stack}) — edit PKG/PROG/path then run `docdrift check`")


@app.command(name="list")
def list_cmd(
    config: Path = typer.Option(Path(".docdrift.yml"), "--config"),  # noqa: B008
) -> None:
    """Print the extracted surface per source (debug aid; never exits non-zero)."""
    manifest = config_mod.load_first([config])
    report = checker_mod.run(manifest, ctx_mod.make_ctx(Path.cwd()))
    for sr in report.sources:
        typer.echo(f"[{sr.name}] {sr.items}")

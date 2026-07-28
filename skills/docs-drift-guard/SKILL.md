---
name: docs-drift-guard
description: Make a project fail CI when its docs drift from its code. Detects the stack, writes a .docdrift.yml manifest, wires a GitHub Actions job (or pytest entry) running the docdrift checker, then verifies. Use when the user says "docs drift", "guard docs", "fail CI on stale docs", or asks to keep README/CLI/service docs in sync with code.
---

# docs-drift-guard

Wire the `docdrift` checker into the current repo so its docs cannot drift from its code.

## Steps

1. **Detect the stack via a POSITIVE marker** (rules in `stacks.md` — `import typer`+`app = typer.Typer` -> typer; `click.Group` -> click; `add_subparsers` -> argparse; `package.json`+`bin`/`exports` -> package-json; `go.mod`/`Cargo.toml` -> cli-help; `docker-compose.y*ml` -> compose-services; `*.tf` -> terraform-modules; `roles/` -> ansible-roles). Mere file presence is NOT a marker.

2. **Generate `.docdrift.yml`** from the matching template in `stacks.md`.

3. **Low-confidence guard:** if no positive marker, do NOT guess a language extractor. Either (a) emit a `files`/`regex` manifest and state the assumption out loud, or (b) ask the user which extractor fits. Never silently write an extractor for a mis-detected stack.

4. **Wire CI:**
   - Default: the reusable workflow — add to `.github/workflows/ci.yml`:
     ```yaml
     jobs:
       docs-drift:
         uses: assaads/docdrift/.github/workflows/docs-drift.yml@v0.1
     ```
   - If `assaads/docdrift` is not created/tagged yet, write `fallback-workflow.yml` (sibling file) verbatim into `.github/workflows/docs-drift.yml` and tell the user it pins `@main` until the repo is tagged.
   - For Python repos using pytest, ALSO add `docdrift` to dev deps so drift is caught locally (not only CI): the `pytest11` plugin auto-runs `test_docdrift` from `.docdrift.yml`.

5. **Verify:** run `uvx --from git+https://github.com/assaads/docdrift@main docdrift check` (or `pytest` for the plugin path). On failure, print the exact missing literals and STOP — do not auto-edit the docs (that is the user's call).

6. **Report:** what was written, which extractor was chosen and why, and any assumptions flagged.

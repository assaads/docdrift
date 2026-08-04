import typer

app = typer.Typer()


@app.command()
def init() -> None: ...


@app.command()
def deploy() -> None: ...

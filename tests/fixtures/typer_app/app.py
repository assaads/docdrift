import typer

app = typer.Typer()


@app.command()
def init() -> None: ...


@app.command()
def push() -> None: ...


@app.command()
def status() -> None: ...

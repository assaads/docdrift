import click

cli = click.Group()


@cli.command()
def build() -> None: ...


@cli.command()
def deploy() -> None: ...

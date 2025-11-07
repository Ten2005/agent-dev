import typer
from cli.commands.data import app

cli = typer.Typer()
cli.add_typer(app, name="data")

if __name__ == "__main__":
    cli()

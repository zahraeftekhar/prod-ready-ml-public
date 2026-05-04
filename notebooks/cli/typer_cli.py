"""CLI using Typer."""

import typer

app = typer.Typer(name="CLI using Typer")


@app.command()
def say_hi(name):
    """Say hello to the user."""
    typer.echo(f"Hello: {name}")


@app.command()
def goodbye():
    """Say goodbye to the user."""
    typer.echo("Goodbye!")


@app.command()
def greet(name):
    """Greets the user."""
    typer.echo(f"Greetings, {name}!")


@app.command()
def welcome(name, greeting="Hello", enthusiastic: bool = False):
    """Welcomes the user."""
    if enthusiastic:
        typer.echo(f"{greeting}, {name}!!!")
    else:
        typer.echo(f"{greeting}, {name}")


if __name__ == "__main__":
    app()

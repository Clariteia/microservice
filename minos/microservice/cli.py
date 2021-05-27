import typer
from typing import Optional
from minos.microservice import EntrypointLauncher
from minos.common import MinosConfig

app = typer.Typer()
from pathlib import Path

DEFAULT_CONF_PATH = "tests/config.yml"


@app.command("start")
def start_microservice(conf: Optional[str] = typer.Argument(DEFAULT_CONF_PATH)):
    """Launch the microservice."""

    try:
        config = MinosConfig(path=Path(conf))
        launcher = EntrypointLauncher(config)
        # launcher.launch()
    except Exception as e:
        typer.echo(f"Error starting microservice: {str(e)}")
        raise typer.Exit(code=1)

    typer.echo("Microservice is up and running!\n")


@app.command("status")
def microservice_status():
    pass


def main():  # pragma: no cover
    app()

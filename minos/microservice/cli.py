"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from pathlib import Path
from typing import Optional

import typer

from minos.common import (
    MinosConfig,
    EntrypointLauncher,
)

from .constants import DEFAULT_CONFIGURATION_FILE_PATH

app = typer.Typer()


@app.command("start")
def start(
    file_path: Optional[Path] = typer.Argument(DEFAULT_CONFIGURATION_FILE_PATH, help="Microservice configuration file.")
):
    """Start the microservice."""

    try:
        config = MinosConfig(file_path)
    except Exception as exc:
        typer.echo(f"Error loading config: {exc!r}")
        raise typer.Exit(code=1)

    try:
        # noinspection PyUnresolvedReferences
        from run import injector, services
    except Exception as exc:
        typer.echo(f"Error loading config: {exc!r}")
        raise typer.Exit(code=1)

    launcher = EntrypointLauncher(injector=injector, services=services)
    try:
        launcher.launch()
    except Exception as exc:
        typer.echo(f"Error launching microservice: {exc!r}")
        raise typer.Exit(code=1)

    typer.echo("Microservice is up and running!\n")


@app.command("status")
def status():
    """Get the microservice status."""
    raise NotImplementedError


@app.command("stop")
def stop():
    """Stop the microservice."""
    raise NotImplementedError

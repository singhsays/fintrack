import sys
from pathlib import Path

import click
from loguru import logger as log

__version__ = "0.1.0"


@click.group()
@click.option("--log_level", default="INFO", help="sets logging level")
@click.option("--log_file", default=None, help="path to log file")
def cli(log_level, log_file):
    log.remove()
    log.add(sys.stderr, level=log_level)
    if log_file is not None:
        f = Path(log_file)
        f.parent.mkdir(parents=True, exist_ok=True)
        f.touch(exist_ok=True)
        log.add(
            str(f.absolute()), rotation="1 day", retention="30 days", level=log_level
        )


@cli.command()
def version():
    print(__version__)

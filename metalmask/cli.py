"""
DESCRIPTION:
    <<describe the purpose of the script>>

INSTALL:
    pip install metalmask
    pip install git+https://github.com/HarmonicHemispheres/metalmask/archive/master.zip
    [DEV] poetry install

USAGE EXAMPLE:
    > python mask "234-43-2425"

LICENSE:
    MIT
"""


# ::IMPORTS ------------------------------------------------------------------------ #

# cli framework - https://pypi.org/project/typer/
import typer

# data types for validation - https://docs.python.org/3/library/typing.html
from typing import Optional

# cross platform path handling - https://docs.python.org/3/library/pathlib.html
from pathlib import Path

# Standard library import for package version retrieval - https://docs.python.org/3/library/importlib.metadata.html
from importlib.metadata import version

# NOTE: only include if needed
# Rich print for better formatting - https://rich.readthed.com/
from rich import print

# project imports
import metalmask as mm


# ::SETUP -------------------------------------------------------------------------- #
app = typer.Typer(
    add_completion=False, 
    no_args_is_help=True,
)

# ::SETUP SUBPARSERS --------------------------------------------------------------- #
# app.add_typer(<<module.app>>, name="subparser")

# ::GLOBALS --------------------------------------------------------------------- #
PKG_NAME = "metalmask"

# ::CORE LOGIC --------------------------------------------------------------------- #
# place core script logic here and call functions
# from the cli command functions to separate CLI from business logic

# ::EXAMPLE CLI COMMANDS ---------------------------------------------------------------------------- #
@app.command()
def mask(src: str = typer.Argument(None, help="File to mask sensitive data in"),
         dest: str = typer.Argument(None, help="Output file to write masked data to")
         ):
    """ example command leave blank for dev to fill out """
    # -- define vars
    metal = mm.Manager()
    resp = metal.mask(src)

    if dest and Path(dest).exists():
        with open(Path(dest), 'w') as f:
            f.write(resp)
        print(f"Masked data written to {dest}")
    else:
        print(resp)


# @app.command()
# def example_loading_spinner_cmd():
#     """ example command with rich package spinner for cli loading indicator """
#     # NOTE: 'from rich.console import Console' must be added to imports for this command
#     console = Console()
#     with console.status(f"[green4] Task is running [/green4]", spinner="dots") as status:
#         # do some action
#         pass

# @app.command()
# def example_user_input_cmd():
#     """ example command to get user input """
#     person_name = typer.prompt("What's your name?")
#     print(f"Hello {person_name}")



# ::DEFAULT CLI COMMANDS ---------------------------------------------------------------------------- #
@app.command()
def version():
    """ get the version of the package """
    package_version = version(PKG_NAME)
    typer.echo(package_version)


# ::EXECUTE ------------------------------------------------------------------------ #
if __name__ == "__main__":  # ensure importing the script will not execute
    app()

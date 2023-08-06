import typer
from typer.main import get_command
from .download import download_cli


SDIST_SUFFIX = ".tar.gz"
WHEEL_SUFFIX = "-py3-none-any.whl"
COMMAND = "python -m dictnet"
NAME = 'dictnet'


Arg = typer.Argument
Opt = typer.Option


app = typer.Typer(name=NAME)
app.command(name='download')(download_cli)


@app.command(hidden=True)
def mock():
    raise NotImplementedError()


def setup_cli() -> None:
    # Ensure that the help messages always display the correct prompt
    command = get_command(app)
    command(prog_name=COMMAND)

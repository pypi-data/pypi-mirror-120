from typing import Optional, Sequence
import typer
from wasabi import msg
import sys
from ..util import run_command


Arg = typer.Argument


DATA_URL = {
    "cambridge_sense_000": {
        "0.0.1": "https://github.com/nlpersimon/dictnet_data/releases/download/cambridge_sense_000-v0.0.1/cambridge_sense_000-0.0.1-py3-none-any.whl",
        "0.0.2": "https://github.com/nlpersimon/dictnet_data/releases/download/cambridge_sense_000-v0.0.2/cambridge_sense_000-0.0.2-py3-none-any.whl"
    }
}

DATA_LATEST_VERSION = {
    "cambridge_sense_000": "0.0.2"
}


app = typer.Typer()


@app.command(
    "download",
    context_settings={"allow_extra_args": True,
                      "ignore_unknown_options": True},
)
def download_cli(
    # fmt: off
    ctx: typer.Context,
    data: str = Arg(..., help="Name of dictnet data to download")
    # fmt: on
):
    download(data, *ctx.args)


def download(data: str, *pip_args) -> None:
    data_name = data
    version = DATA_LATEST_VERSION[data_name]
    download_data(data_name, version, pip_args)
    msg.good(
        "Download and installation successful",
        f"You can now load the package via dictnet.load('{data_name}')",
    )


def download_data(
    data_name: str, version: str, user_pip_args: Optional[Sequence[str]] = None
) -> None:
    download_url = DATA_URL[data_name][version]
    pip_args = list(user_pip_args) if user_pip_args is not None else []
    cmd = [sys.executable, "-m", "pip", "install"] + pip_args + [download_url]
    run_command(cmd)


if __name__ == '__main__':
    app()

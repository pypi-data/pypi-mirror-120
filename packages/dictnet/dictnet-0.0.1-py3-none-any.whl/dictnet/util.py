from typing import List, Union, Any, Optional
import os
import sys
import shlex
import subprocess
import importlib
from ._dictnet import Dictnet

is_windows = sys.platform.startswith("win")


# begin of copy
# from https://github.com/explosion/spaCy/blob/9fde2580538967dc16f63d4c3bc55660d031d09e/spacy/util.py#L816
def run_command(
    command: Union[str, List[str]],
    *,
    stdin: Optional[Any] = None,
    capture: bool = False,
) -> Optional[subprocess.CompletedProcess]:
    """Run a command on the command line as a subprocess. If the subprocess
    returns a non-zero exit code, a system exit is performed.
    command (str / List[str]): The command. If provided as a string, the
        string will be split using shlex.split.
    stdin (Optional[Any]): stdin to read from or None.
    capture (bool): Whether to capture the output and errors. If False,
        the stdout and stderr will not be redirected, and if there's an error,
        sys.exit will be called with the return code. You should use capture=False
        when you want to turn over execution to the command, and capture=True
        when you want to run the command more like a function.
    RETURNS (Optional[CompletedProcess]): The process object.
    """
    if isinstance(command, str):
        cmd_list = split_command(command)
        cmd_str = command
    else:
        cmd_list = command
        cmd_str = " ".join(command)
    try:
        ret = subprocess.run(
            cmd_list,
            env=os.environ.copy(),
            input=stdin,
            encoding="utf8",
            check=False,
            stdout=subprocess.PIPE if capture else None,
            stderr=subprocess.STDOUT if capture else None,
        )
    except FileNotFoundError:
        # Indicates the *command* wasn't found, it's an error before the command
        # is run.
        raise FileNotFoundError(
            f'{cmd_str} not found'
        ) from None
    if ret.returncode != 0 and capture:
        message = f"Error running command:\n\n{cmd_str}\n\n"
        message += f"Subprocess exited with status {ret.returncode}"
        if ret.stdout is not None:
            message += f"\n\nProcess log (stdout and stderr):\n\n"
            message += ret.stdout
        error = subprocess.SubprocessError(message)
        error.ret = ret
        error.command = cmd_str
        raise error
    elif ret.returncode != 0:
        sys.exit(ret.returncode)
    return ret


def split_command(command: str) -> List[str]:
    """Split a string command using shlex. Handles platform compatibility.
    command (str) : The command to split
    RETURNS (List[str]): The split command.
    """
    return shlex.split(command, posix=not is_windows)

# end of copy


def load(data_name: str) -> Dictnet:
    data = importlib.import_module(data_name)
    senses = data.senses
    def_embeds = data.def_embeds
    dictnet = Dictnet(senses, def_embeds)
    return dictnet

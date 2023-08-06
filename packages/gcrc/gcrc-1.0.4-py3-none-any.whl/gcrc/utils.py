import shutil
import subprocess  # nosec

import typer


def run(cmd: list[str]):
    orig = cmd[0]
    cmd[0] = shutil.which(orig)
    if cmd[0] is None:
        raise subprocess.SubprocessError(f"Invalid executable {orig}")

    result = subprocess.run(cmd, capture_output=True)  # nosec
    if result.returncode:
        typer.echo(typer.style(result.stdout.decode("utf-8"), fg=typer.colors.GREEN))
        typer.echo(typer.style(result.stderr.decode("utf-8"), fg=typer.colors.RED))
        raise subprocess.CalledProcessError(result.returncode, cmd)

    return result

import re
import subprocess
import webbrowser
from typing import Optional

import typer

app = typer.Typer(name="git-open")


def extract_url(url: str) -> str:
    pattern = re.compile(r".*://(.*@)?(.*?)(:\d+)?/(.*)")
    match = pattern.match(url)
    user = match.group(1)
    host = match.group(2)
    port = match.group(3)
    path = match.group(4)
    return f"https://{host}/{path}"


def get_git_url(path: Optional[str] = ".") -> str:
    # result = subprocess.run(["git", "remote", "-v"], capture_output=True)
    cmd = f"pushd {path} > /dev/null 2>&1; git remote -v | awk '/fetch/{{print $2}}'; popd > /dev/null 2>&1"
    result = subprocess.run(cmd, capture_output=True, shell=True)
    url = result.stdout.decode().strip("\n")
    _ = None
    return url


@app.command()
def git_open(
    path: str = typer.Argument(".", help="path in directory of the desired repo."),
):
    url = get_git_url(path)
    git_url = extract_url(url)
    typer.secho(f"{git_url}", err=False, fg=None)
    webbrowser.open(git_url, new=2)


if __name__ == "__main__":
    app()

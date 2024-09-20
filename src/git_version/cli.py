"""
Python script that returns a version string based on the git history of a repository.

Some of the code has been copied or adapted from <https://gitlab.com/rocshers/python/poetry-git-version-plugin/-/tree/release?ref_type=heads>.
Since this repository does not use poetry, I wanted a standalone script that can be used to version a python repository in a similar way.

### Usage

The script is intended to be used as a CLI tool, and can be run with the following command:

```bash
python git_version.py version \
    path/to/git/repo \
    --path-to-pyproject path/to/pyproject.toml
```

The script will automatically parse configuration options from a `pyproject.toml` file in the current working directory if available.
You can pass a path to a `pyproject.toml` file with the `--path-to-pyproject` option.

You may also use environment variables:

```bash
export GIT_VERSION_ROOT_DIR=path/to/git/repo
export GIT_VERSION_PYPROJECT_PATH=path/to/pyproject.toml
python git_version.py version
```

To enable debug logging, use the `--debug` option:

```bash
python git_version.py --debug version ...
```

### Configuration

The configuration options are limited. This script will either:
- Parse a tag name from a git source and return the version string
- Parse a tag name from a git source and return the version string, with the distance from the last tag and optionally the commit hash

You can also specify a pyproject.toml file with a `tool.git-version` section to configure the script:

```toml
[tool.git-version]
pre_release_commit_hash = true # Set to false if you don't want to include the commit hash in the version string
```
"""

import logging
import pathlib as plb
import typing

import typer
from git import Repo
from typing_extensions import Annotated

from git_version import _config, _core

logger = logging.getLogger("git-version")
handler = logging.StreamHandler()
format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
handler.setFormatter(format)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


app = typer.Typer(
    name="git-version",
    no_args_is_help=True,
    help="A tool to handle versioning from git repositories",
    pretty_exceptions_show_locals=False,
)


@app.callback()
def main(debug: bool = typer.Option(False, help="Enable debug logging.")):
    if debug:
        logger.setLevel(logging.DEBUG)


@app.command()
def version(
    path_to_repo: Annotated[
        plb.Path,
        typer.Argument(
            help="Path to git repository. Defaults to current working directory",
            envvar="GIT_VERSION_ROOT_DIR",
        ),
    ] = plb.Path.cwd().resolve(),
    path_to_pyproject: Annotated[
        typing.Optional[plb.Path],
        typer.Option(
            help="Path to pyproject.toml that contains a 'tool.git-version' configuration",
            envvar="GIT_VERSION_PYPROJECT_PATH",
        ),
    ] = None,
):
    """Get the current version of a git repository"""
    ver = _core.Versioner(
        _core.GitRepo(repo=Repo(path_to_repo)),
        _config.get_version_config(path_to_pyproject),
    )
    typer.echo(ver.version)


def entrypoint():
    app()

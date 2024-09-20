import logging
import os
import pathlib as plb
import tomllib
import typing

import pydantic

logger = logging.getLogger("git_version._config")


class GitVersionConfig(pydantic.BaseModel):
    pre_release_commit_hash: bool


default_conf = GitVersionConfig(pre_release_commit_hash=False)


def get_version_config(
    path_to_pyproject: typing.Optional[plb.Path] = None,
) -> GitVersionConfig:
    """Parse git version config from a pyproject.toml file

    Args:
        path_to_pyproject (typing.Optional[str], optional): Explicit path to a pyproject.toml. Defaults to None, in which
         case we look for a pyproject.toml file in the current working directory.

    Returns:
        GitVersionConfig: A pydantic model with the parsed configuration
    """
    if path_to_pyproject is not None:
        path = plb.Path(path_to_pyproject)
    else:  # Use current wd
        logger.debug(f"Using current working directory to parse options: {os.getcwd()}")
        path = plb.Path(os.getcwd()) / "pyproject.toml"
    logger.debug(f"Path to pyproject.toml: {path}")
    conf = default_conf.model_copy()
    if path.exists() and path.is_file():
        logger.debug(f"Found file at {path}")
        with path.open("rb") as inFile:
            pyproject_def = tomllib.load(inFile)
        if pyproject_def.get("tool"):
            if pyproject_def["tool"].get("git-version"):
                logger.debug("Found git-version config in pyproject.toml")
                logger.debug(f"Config: {pyproject_def['tool']['git-version']}")
                conf = GitVersionConfig(**pyproject_def["tool"]["git-version"])
    else:
        logger.debug(f"No file found at {path}")
        logger.debug(f"Returning default config: {conf}")
    return conf

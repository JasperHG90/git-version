import pathlib as plb

import pytest

from git_version import _config


@pytest.fixture(params=[True, False])
def pyproject(request) -> str:
    return f"""
    [tool.git-version]
    pre_release_commit_hash={'true' if request.param else 'false'}
    """.strip()


@pytest.fixture()
def pyproject_on_disk(tmp_path: plb.Path, pyproject: str) -> plb.Path:
    pyproject_path = tmp_path / "pyproject.toml"
    with pyproject_path.open("w") as f:
        f.write(pyproject)
    return pyproject_path


def test_get_version_config(pyproject_on_disk: plb.Path):
    _config.get_version_config(pyproject_on_disk)


def test_default_version_config_returned(pyproject_on_disk: plb.Path):
    config = _config.get_version_config(pyproject_on_disk / ".bs")  # Does not exist
    assert config.pre_release_commit_hash is False

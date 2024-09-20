from unittest import mock

import pytest

from git_version import _config, _core


class MockTag:
    def __init__(self, name, commit):
        self.name = name
        self.commit = commit


@pytest.fixture(params=["v1.2.3", "1.2.3"])
def tag(request) -> MockTag:
    return MockTag(request.param, "abcdefg")


def test_parse_tag(tag: MockTag):
    res = _core.parse_tag(tag)
    assert res["major"] == 1
    assert res["minor"] == 2
    assert res["patch"] == 3


def test_parse_tag_fails():
    res = _core.parse_tag(MockTag("v1.2.3.4", "abcdefg"))
    assert res["major"] == 0
    assert res["minor"] == 0
    assert res["patch"] == 0


def test_versioner():
    with mock.MagicMock() as mock_git_repo:
        mock_git_repo.get_last_tag.return_value = MockTag(
            name="v1.2.3", commit="abcdefg"
        )
        mock_git_repo.get_distance.return_value = 4
        mock_git_repo.get_commit_short_hash.return_value = "abcdefg"

        version = _core.Versioner(
            repo_info=mock_git_repo,
            config=_config.GitVersionConfig(pre_release_commit_hash=True),
        )

    assert version.version == "1.2.3a4+abcdefg"


def test_current_tag():
    with mock.MagicMock() as mock_git_repo:
        mock_git_repo.head.commit = "bhs213d2"
        mock_git_repo.tags = [
            MockTag("v1.2.3", "abcdefg"),
            MockTag("v1.2.4", "bhs213d2"),
        ]
        repo = _core.GitRepo(repo=mock_git_repo)
        assert repo.current_tag().name == "v1.2.4"


def test_get_last_tag():
    with mock.MagicMock() as mock_git_repo:
        mock_git_repo.tags = [
            MockTag("v1.2.3", "abcdefg"),
            MockTag("v1.2.4", "bhs213d2"),
        ]
        mock_git_repo.iter_commits.return_value = ["bhs213d2", "abcdefg"]
        repo = _core.GitRepo(repo=mock_git_repo)
        assert repo.get_last_tag().name == "v1.2.4"


@pytest.mark.parametrize(
    "major,minor,patch,distance,commit_hash,pre_release,build_metadata,expected",
    [
        (1, 2, 3, 0, None, "", "", "1.2.3"),
        (1, 2, 3, 8, "abf4yu7", "", "", "1.2.3a8+abf4yu7"),
        (1, 2, 3, 12, None, "", "", "1.2.3a12"),
    ],
)
def test_version_info(
    major, minor, patch, distance, commit_hash, pre_release, build_metadata, expected
):
    version_info = _core.VersionInfo(
        major=major,
        minor=minor,
        patch=patch,
        distance=distance,
        commit_hash_short=commit_hash,
        pre_release=pre_release,
        build_metadata=build_metadata,
    )
    version_str = version_info.fmt()
    assert version_str == expected

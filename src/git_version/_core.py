import dataclasses
import logging
import typing

from git import Repo, Tag
from git.objects import Commit
from typing_extensions import TypedDict

from git_version import _config, _const

logger = logging.getLogger("git_version._core")


VersionDict = TypedDict(
    "VersionDict",
    {
        "major": int,
        "minor": int,
        "patch": int,
        "pre_release": str,
        "build_metadata": str,
    },
)


class GitRepo:
    """
    Class to handle git repository operations for versioning
    """

    def __init__(self, repo: Repo):
        """
        Args:
            path (str): Path to git repository
        """
        self.repo = repo

    @property
    def commits(self) -> typing.List[Commit]:
        return [*self.repo.iter_commits()]

    @property
    def head_commit(self) -> Commit:
        return self.repo.head.commit

    @property
    def tags(self) -> typing.List[Tag]:
        return [*reversed([*self.repo.tags])]

    def current_tag(self) -> typing.Optional[Tag]:
        for tag in self.tags:
            if tag.commit == self.head_commit:
                return tag
        return None

    def get_last_tag(self) -> typing.Optional[Tag]:
        tag_dict = {tag.commit: tag for tag in self.tags}

        for commit in self.commits:
            if commit in tag_dict:
                return tag_dict[commit]

        return None

    def get_commit_short_hash(self, commit: Commit) -> str:
        return commit.hexsha[:7]

    def get_distance(self, from_commit: Commit, to_commit: Commit) -> int:
        return len(
            [*self.repo.iter_commits(f"{from_commit.hexsha}...{to_commit.hexsha}")]
        )


@dataclasses.dataclass
class VersionInfo:
    major: int
    minor: int
    patch: int
    distance: int
    commit_hash_short: typing.Optional[str]
    pre_release: str
    build_metadata: str

    def fmt(self) -> str:
        """Format version information into <MAJOR>.<MINOR>.<PATCH> possible with
         distance and commit hash

        Returns:
            str: Formatted version string
        """
        ver = f"{self.major}.{self.minor}.{self.patch}"
        if self.distance > 0:
            ver += (
                f"a{self.distance}+{self.commit_hash_short}"
                if self.commit_hash_short
                else f"a{self.distance}"
            )
        return ver


def parse_tag(tag: typing.Optional[Tag]) -> VersionDict:
    """Parse a git tag into a dictionary with version information

    Args:
        tag (typing.Optional[Tag]): Git Tag object to parse. If None, returns a dictionary with default info

    Returns:
        typing.Dict[str, typing.Union[str, int]]: Dictionary with version information
    """

    if tag is None:
        return {
            "major": 0,
            "minor": 0,
            "patch": 0,
            "pre_release": "",
            "build_metadata": "",
        }
    else:
        reg = _const.REGEX_PATTERN.search(tag.name)
        reg_dict = {}

        if reg is not None:
            reg_dict = reg.groupdict()
        else:
            logger.warning(f"Could not parse tag {tag.name}. Returning default values")

        return {
            "major": int(reg_dict.get("major", 0)),
            "minor": int(reg_dict.get("minor", 0)),
            "patch": int(reg_dict.get("patch", 0)),
            "pre_release": reg_dict.get("pre_release", ""),
            "build_metadata": reg_dict.get("build_metadata", ""),
        }


def get_version_info(
    parsed_tag: VersionDict,
    distance: int,
    commit_hash_short: typing.Optional[str] = None,
) -> VersionInfo:
    """Create a VersionInfo object from parsed tag information

    Args:
        parsed_tag (VersionDict): Dictionary with parsed tag information
        distance (int): Distance from last tag, i.e. number of commits since last tag
        commit_hash_short (typing.Optional[str], optional): Git commit SHA, shortened to 8 characters.
            If given, will be added to version information Defaults to None.

    Returns:
        VersionInfo: VersionInfo object
    """
    return VersionInfo(
        **parsed_tag, distance=distance, commit_hash_short=commit_hash_short
    )


class Versioner:

    def __init__(self, repo_info: GitRepo, config: _config.GitVersionConfig):
        """Main class to handle versioning from a git repository

        Args:
            repo_info (GitRepo): GitRepo object with repository information
            config (GitVersionConfig): Configuration object
        """
        self.repo = repo_info
        self.config = config
        self.version_info = self._get_version()

    @property
    def version(self) -> str:
        return self.version_info.fmt()

    def _get_version(self) -> VersionInfo:

        last_tag = self.repo.get_last_tag()
        last_tag_commit = (
            last_tag.commit if last_tag is not None else self.repo.commits[-1]
        )
        distance = self.repo.get_distance(self.repo.head_commit, last_tag_commit)
        commit_hash_short = self.repo.get_commit_short_hash(self.repo.head_commit)

        return get_version_info(
            parse_tag(last_tag),
            distance,
            commit_hash_short if self.config.pre_release_commit_hash else None,
        )

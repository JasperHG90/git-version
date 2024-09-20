#!/bin/sh -l

git config --global --add safe.directory /github/workspace
VERSION=$(/.venv/bin/git_version version $1 --path-to-pyproject $2)
echo "Version: $VERSION"
echo "VERSION=$VERSION" >> $GITHUB_ENV

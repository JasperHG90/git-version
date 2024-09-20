#!/bin/sh -l

VERSION=$(/.venv/bin/git_version version $1 --path-to-pyproject $2)
echo "Version: $VERSION"
echo "VERSION=$VERSION" >> $GITHUB_ENV

#!/bin/sh -l

#git config --global --add safe.directory /github/workspace
VERSION=$(/.venv/bin/git_version version $1 --path-to-pyproject $2)
exit_code=$?
if [ $exit_code -ne 0 ]; then
  echo "Failed to get version"
  exit $exit_code
fi
echo "Version: $VERSION"
echo "VERSION=$VERSION" >> $GITHUB_ENV

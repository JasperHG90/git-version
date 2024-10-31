#!/bin/sh -l

git config --global --add safe.directory /github/workspace
cd $1
VERSION=$(bash /git_version.sh)
exit_code=$?
if [ $exit_code -ne 0 ]; then
  echo "Failed to get version"
  exit $exit_code
fi
echo "Version: $VERSION"
echo "version=$VERSION" >> $GITHUB_OUTPUT

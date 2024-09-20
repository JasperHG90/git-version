#!/bin/sh -l

VERSION=$(/.venv/bin/git-version run $1 $2)
echo "VERSION=$VERSION" >> $GITHUB_ENV

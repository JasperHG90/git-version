# Git-version

Python CLI tool to retrieve a PEP-compatible version based on git history and tags.

This repository is inspired by [poetry-git-version-plugin](https://pypi.org/project/poetry-git-version-plugin/). Unlike that package, this action has been written in bash.

## Usage

To use this action, you can add the following step in your pipeline:

```yaml
jobs:
  test_git_version_action:
    runs-on: ubuntu-latest
    name: 'Test GHA'
    needs: tests
    steps:
      - name: checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: 'Get version'
        id: version
        uses: JasperHG90/git-version@v2.0.0
      - name: 'Print version'
        run: echo "Version is ${{ steps.version.outputs.version }}"
```

The action will return a version based on the **release tag**. E.g. 'v1.0.0' will become '1.0.0'. 

If HEAD is not tagged, then the script will take the last tag that is formatted as 'v*', compute the distance from that tag and the current commit, and add that distance to the version with a short commit SHA. For example:

1.0.0a50+7342fed

# Git-version

Python CLI tool to retrieve a PEP-compatible version based on git history and tags.

A large chunk of the code has been copied from [poetry-git-version-plugin](https://pypi.org/project/poetry-git-version-plugin/). Unlike that package, this action will work for other build tools than Poetry.

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
        uses: JasperHG90/git-version@v1.0.0
      - name: 'Print version'
        run: echo "Version is ${{ steps.version.outputs.version }}"
```

You can optionally specify the path to the repo that you want to retrieve a version for, as well as the pyproject.toml that contains configuration options:

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
        uses: JasperHG90/git-version@v1.0.0
        with:
            repo_path: '/path/to/repo/'
            pyproject_path: '/path/to/repo/pyproject.toml'
      - name: 'Print version'
        run: echo "Version is ${{ steps.version.outputs.version }}"
```

In general, you won't need to do this as the default points to the directory that is used by GHA.

## Configuration

You can add the following configuration to a pyproject.toml:

```
[tool.git-version]
pre_release_commit_hash = true / false
```

This setting will optionally append a short commit SHA to the version string (e.g. '0.0.1a67' or '0.0.1a67+ghf5t64'). By default, the commit SHA is not added.

Package Diff
============

[![Lint](https://github.com/khwiri/package-diff/actions/workflows/lint.yml/badge.svg)](https://github.com/khwiri/package-diff/actions/workflows/lint.yml)
[![Test](https://github.com/khwiri/package-diff/actions/workflows/test.yml/badge.svg)](https://github.com/khwiri/package-diff/actions/workflows/test.yml)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://github.com/khwiri/package-diff)

Package Diff is a command-line tool that can be used to quickly describe
both concrete and transitive dependency changes when managing project requirements.
It interfaces with git to help automate commit messages containing this information.

### Quick Example

```
:construction_worker: Update Python Dependencies

Default Dependencies
- click==8.0.3 (upgrade from 8.0.0)
- flask==2.0.0 (add)
- requests==2.26.0 (downgrade from 2.27.1)
- rich==11.1.0 (remove)

Develop Dependencies
- ipython==8.0.1 (add)
- isort==5.10.1 (upgrade from 5.9.3)
- pylint==2.12.2 (remove)
- pytest==6.1.2 (downgrade from 6.2.5)

# Please enter the commit message for your changes. Lines starting
# with '#' will be ignored, and an empty message aborts the commit.
#
# On branch main
# Your branch is up to date with 'origin/main'.
#
# Changes to be committed:
#       modified:   toolbox/sandbox/Pipfile.lock
#
# Changes not staged for commit:
#       modified:   README.md
#
```

Installing
----------

Install with [pip](https://pip.pypa.io/en/stable).

*Note: Passing --editable so that pip freeze produces usable requirements.*

```
> pip install --editable git+https://github.com/khwiri/package-diff.git@main#egg=package-diff
```

Installing with [pipenv](https://pipenv.pypa.io/en/latest).

```
> pipenv install git+https://github.com/khwiri/package-diff.git@main#egg=package-diff
```

Usage
-----

Package Diff is meant to be used with [Pipfile](https://github.com/pypa/pipfile) files.
In other words, `Pipfile` and `Pipfile.lock` files. [Pipenv](https://github.com/pypa/pipenv)
is a tool that currently uses these files for managing project requirements.

```
> pipenv run package-diff --help
Usage: package-diff [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  commit  Commit dependency changes.
  view    Print text output of commit message only.
```

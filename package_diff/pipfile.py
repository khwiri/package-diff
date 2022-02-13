import json
from enum import Enum
from typing import Dict
from typing import Iterator
from typing import Optional
from pathlib import Path
from subprocess import check_output
from dataclasses import dataclass

from .version import Version


class State(Enum):
    ADD       = 1
    REMOVE    = 2
    UPGRADE   = 3
    DOWNGRADE = 4

class Package:
    def __init__(self, name :str, version :str):
        self.name    = name
        self.version = Version(version)

    def __eq__(self, o :'Package'):
        return self.name == o.name

    def __lt__(self, o :'Package'):
        return self.name < o.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return f'{self.name}=={self.version}'


@dataclass
class PackageState:
    state        :State
    package      :Package
    from_version :Optional[str] =None


def load_pipfile_lock(pipfile_lock :Path) -> Dict:
    with pipfile_lock.open() as f:
        return json.load(f)


def load_pipfile_lock_from_git_head(pipfile_lock :Path) -> Dict:
    stdout = check_output(['git', 'show', f'HEAD:{pipfile_lock}'])
    return json.loads(stdout)


def get_package_change_states(pipfile :Path, dependencies_group :str) -> Iterator[PackageState]:
    pipfile_lock = Path(f'{pipfile}.lock')
    if not pipfile_lock.is_file():
        raise FileNotFoundError()

    curr_pipfile_lock = load_pipfile_lock(pipfile_lock)
    from_pipfile_lock = load_pipfile_lock_from_git_head(pipfile_lock)

    curr_pipfile_packages_dict = {
        k:Package(k, v.get('version'))
        for k,v in curr_pipfile_lock.get(dependencies_group, {}).items()
    }
    from_pipfile_packages_dict = {
        k:Package(k, v.get('version'))
        for k,v in from_pipfile_lock.get(dependencies_group, {}).items()
    }

    curr_pipfile_packages_set = set(curr_pipfile_packages_dict.values())
    from_pipfile_packages_set = set(from_pipfile_packages_dict.values())

    yield from map(lambda x: PackageState(State.ADD,    x), curr_pipfile_packages_set - from_pipfile_packages_set)
    yield from map(lambda x: PackageState(State.REMOVE, x), from_pipfile_packages_set - curr_pipfile_packages_set)

    for common_package in (from_pipfile_packages_set & curr_pipfile_packages_set):
        curr_package = curr_pipfile_packages_dict.get(common_package.name)
        from_package = from_pipfile_packages_dict.get(common_package.name)

        if curr_package.version > from_package.version:
            yield PackageState(State.UPGRADE, curr_package, from_package.version)

        elif curr_package.version < from_package.version:
            yield PackageState(State.DOWNGRADE, curr_package, from_package.version)


def find_pipfile(root :Optional[Path] =None) -> Path:
    if root is None:
        root = Path('.')

    pipfile = root / 'Pipfile'
    if not pipfile.is_file():
        raise FileNotFoundError()

    return pipfile

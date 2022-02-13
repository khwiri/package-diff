from string import Template
from typing import List
from pathlib import Path
from tempfile import NamedTemporaryFile
from tempfile import _TemporaryFileWrapper
from functools import partial
from contextlib import AbstractContextManager
from contextlib import contextmanager
from subprocess import call
from subprocess import check_call
from collections import defaultdict

from .pipfile import State
from .pipfile import PackageState


def render_package_change_state(add_template :str, remove_template :str, upgrade_template :str, downgrade_template :str, package_state :PackageState) -> str:
    template_mapping = defaultdict(
        lambda: partial(Template, 'Unknown'),
        [
            (State.ADD,       partial(Template, add_template)      ),
            (State.REMOVE,    partial(Template, remove_template)   ),
            (State.UPGRADE,   partial(Template, upgrade_template)  ),
            (State.DOWNGRADE, partial(Template, downgrade_template)),
        ]
    )

    substitute_mapping = dict(
        package=package_state.package
    )

    if package_state.state in (State.UPGRADE, State.DOWNGRADE):
        substitute_mapping.update(dict(from_version=package_state.from_version))

    template = template_mapping[package_state.state]()
    return template.safe_substitute(substitute_mapping)


def text(default_package_changes :List[str], develop_package_changes :List[str], title :str, summary :str) -> None:
    with create_temp_commit_message_file(default_package_changes, develop_package_changes, title, summary) as f:
        print(
            *[l.decode() for l in f.readlines()],
            sep=''
        )


@contextmanager
def create_temp_commit_message_file(default_package_changes :List[str], develop_package_changes :List[str], title :str, summary :str) -> AbstractContextManager[_TemporaryFileWrapper]:
    with NamedTemporaryFile() as f:
        f.write(f'{title}\n\n'.encode())

        if summary:
            f.write(f'{summary}\n\n'.encode())

        if default_package_changes:
            f.write('Default Dependencies\n'.encode())
            for package_change in default_package_changes:
                f.write(f'{package_change}\n'.encode())

        if develop_package_changes:
            f.write('\nDevelop Dependencies\n'.encode())
            for package_change in develop_package_changes:
                f.write(f'{package_change}\n'.encode())

        f.flush()
        f.seek(0)

        yield f


def commit(pipfile :Path, default_package_changes :List[str], develop_package_changes :List[str], title :str, summary :str, no_edit :bool) -> None:
    if not pipfile.is_file():
        raise FileNotFoundError()

    pipfile_lock = Path(f'{pipfile}.lock')
    if not pipfile_lock.is_file():
        raise FileNotFoundError()

    check_call(
        ['git', 'add', pipfile, pipfile_lock]
    )

    with create_temp_commit_message_file(default_package_changes, develop_package_changes, title, summary) as f:
        # Note: Using call without worrying about the returncode because the commit could be aborted
        call(
            [
                'git',
                'commit',
                '--file' if no_edit else '--template',
                f.name,
            ]
        )

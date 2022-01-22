from typing import List
from pathlib import Path
from tempfile import NamedTemporaryFile
from tempfile import _TemporaryFileWrapper
from contextlib import AbstractContextManager
from contextlib import contextmanager
from subprocess import check_call


def text(package_states :List[str], title :str, summary :str) -> None:
    with create_temp_commit_message_file(package_states, title, summary) as f:
        print(
            *[l.decode() for l in f.readlines()],
            sep=''
        )


@contextmanager
def create_temp_commit_message_file(package_states :List[str], title :str, summary :str) -> AbstractContextManager[_TemporaryFileWrapper]:
    with NamedTemporaryFile() as f:
        f.write(f'{title}\n\n'.encode())

        if summary:
            f.write(f'{summary}\n\n'.encode())

        for package_state in package_states:
            f.write(f'{package_state}\n'.encode())

        f.flush()
        f.seek(0)

        yield f


def commit(pipfile :Path, package_states :List[str], title :str, summary :str, no_edit :bool) -> None:
    if not pipfile.is_file():
        raise FileNotFoundError()

    pipfile_lock = Path(f'{pipfile}.lock')
    if not pipfile_lock.is_file():
        raise FileNotFoundError()

    check_call(
        ['git', 'add', pipfile, pipfile_lock]
    )

    with create_temp_commit_message_file(package_states, title, summary) as f:
        check_call(
            [
                'git',
                'commit',
                '--file' if no_edit else '--template',
                f.name,
            ]
        )

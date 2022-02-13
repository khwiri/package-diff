
from typing import Callable
from typing import Optional
from pathlib import Path as PathLibPath
from functools import reduce
from functools import partial

from click import Path as ClickPath
from click import group
from click import option
from click import argument

from .pipfile import find_pipfile
from .pipfile import get_package_change_states
from .produce import text as produce_text
from .produce import commit as produce_commit
from .produce import render_package_change_state


get_sorted_default_package_change_states = lambda x: sorted(list(get_package_change_states(x, 'default')), key=lambda y: y.package)
get_sorted_develop_package_change_states = lambda x: sorted(list(get_package_change_states(x, 'develop')), key=lambda y: y.package)


DEFAULT_COMMIT_TITLE       = ':construction_worker: Update Python Dependencies'

DEFAULT_ADD_TEMPLATE       = '- $package (add)'
DEFAULT_REMOVE_TEMPLATE    = '- $package (remove)'
DEFAULT_UPGRADE_TEMPLATE   = '- $package (upgrade from $from_version)'
DEFAULT_DOWNGRADE_TEMPLATE = '- $package (downgrade from $from_version)'


def apply_template_click_options(func :Callable) -> Callable:
    options = [
        option('--title',              default=DEFAULT_COMMIT_TITLE,       help='Set git commit message title.'       ),
        option('--summary',            type=str,                           help='Set git commit message summary.'     ),
        option('--add-template',       default=DEFAULT_ADD_TEMPLATE,       help='Set template for added dependencies.'),
        option('--remove-template',    default=DEFAULT_REMOVE_TEMPLATE,    help='Git Commit Message Summary'          ),
        option('--upgrade-template',   default=DEFAULT_UPGRADE_TEMPLATE,   help='Git Commit Message Summary'          ),
        option('--downgrade-template', default=DEFAULT_DOWNGRADE_TEMPLATE, help='Git Commit Message Summary'          ),
    ]

    func = reduce(
        lambda f, o: o(f), # f == func, o == option, example: func = option(func)
        reversed(options),
        func
    )

    return func


@group()
def cli():
    pass


@cli.command()
@apply_template_click_options
@argument('pipfile', type=ClickPath(exists=True), required=False)
def view(pipfile :Optional[str], title :str, summary :Optional[str], add_template :str, remove_template :str, upgrade_template :str, downgrade_template :str) -> None:
    '''Print text output of commit message only.'''
    pipfile = find_pipfile() if pipfile is None else PathLibPath(pipfile)

    render_package_change_state_  = partial(
        render_package_change_state,
        add_template,
        remove_template,
        upgrade_template,
        downgrade_template
    )

    produce_text(
        map(render_package_change_state_, get_sorted_default_package_change_states(pipfile)),
        map(render_package_change_state_, get_sorted_develop_package_change_states(pipfile)),
        title,
        summary
    )


@cli.command()
@apply_template_click_options
@option('--no-edit', is_flag=True, help='Use generated commit message without launching an editor.')
@argument('pipfile', type=ClickPath(), required=False)
def commit(pipfile :Optional[str], title :str, summary :Optional[str], add_template :str, remove_template :str, upgrade_template :str, downgrade_template :str, no_edit :bool) -> None:
    '''Commit dependency changes.'''
    pipfile = find_pipfile() if pipfile is None else PathLibPath(pipfile)

    render_package_change_state_  = partial(
        render_package_change_state,
        add_template,
        remove_template,
        upgrade_template,
        downgrade_template
    )

    produce_commit(
        pipfile,
        map(render_package_change_state_, get_sorted_default_package_change_states(pipfile)),
        map(render_package_change_state_, get_sorted_develop_package_change_states(pipfile)),
        title,
        summary,
        no_edit
    )

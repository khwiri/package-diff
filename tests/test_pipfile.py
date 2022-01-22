from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from functools import partial
from unittest.mock import Mock

from pytest import MonkeyPatch
from pytest import mark
from pytest import param
from _pytest.mark.structures import ParameterSet
from pkg_resources.extern.packaging.version import Version

from package_diff.pipfile import State
from package_diff.pipfile import Package
from package_diff.pipfile import PackageState
from package_diff.pipfile import get_package_change_states
from package_diff.pipfile import render_package_change_state


ParamTestId       = str
ParamTestArgs     = Any # variable length (ie: *args)
ParamTestExpected = Any
ParamTestData     = List[
    Tuple[
        ParamTestId,
        ParamTestArgs,
        ParamTestExpected
    ]
]


def convert_test_data_to_params(data :ParamTestData) -> List[ParameterSet]:
    return list(map(lambda x: param(*x[1:], id=x[0]), data))


FromPipfilePackages         = Dict
CurrPipfilePackages         = Dict
PackageChangeStatesExpected = List[PackageState]
PackageChangeStatesTestData = List[
    Tuple[
        ParamTestId,
        FromPipfilePackages,
        CurrPipfilePackages,
        PackageChangeStatesExpected,
    ]
]
PACKAGE_CHANGE_STATES_TEST_DATA :PackageChangeStatesTestData = [
    (
        'no-package-changes',
        {'faux_package': {'version': '==0.0.1'}},
        {'faux_package': {'version': '==0.0.1'}},
        [],
    ),
    (
        'package-add',
        {'faux_package': {'version': '==0.0.1'}},
        {'faux_package': {'version': '==0.0.1'}, 'faux_package_add': {'version': '==0.0.2'}},
        [
            PackageState(
                state=State.ADD,
                package=Package('faux_package_add', '==0.0.2')
            ),
        ],
    ),
    (
        'package-remove',
        {'faux_package': {'version': '==0.0.1'}, 'faux_package_remove': {'version': '==0.0.2'}},
        {'faux_package': {'version': '==0.0.1'}},
        [
            PackageState(
                state=State.REMOVE,
                package=Package('faux_package_remove', '==0.0.2')
            ),
        ],
    ),
    (
        'package-upgrade',
        {'faux_package': {'version': '==0.0.1'}, 'faux_package_upgrade': {'version': '==0.0.1'}},
        {'faux_package': {'version': '==0.0.1'}, 'faux_package_upgrade': {'version': '==0.0.2'}},
        [
            PackageState(
                state=State.UPGRADE,
                package=Package('faux_package_upgrade', '==0.0.2'),
                from_version=Version('0.0.1')
            ),
        ],
    ),
    (
        'package-downgrade',
        {'faux_package': {'version': '==0.0.1'}, 'faux_package_upgrade': {'version': '==0.0.2'}},
        {'faux_package': {'version': '==0.0.1'}, 'faux_package_upgrade': {'version': '==0.0.1'}},
        [
            PackageState(
                state=State.DOWNGRADE,
                package=Package('faux_package_upgrade', '==0.0.1'),
                from_version=Version('0.0.2')
            ),
        ],
    ),
]


RenderedPackageChangeStateExpected = str
RenderPackageChangeStateTestData   = List[
    Tuple[
        ParamTestId,
        PackageState,
        RenderedPackageChangeStateExpected,
    ]
]
RENDER_PACKAGE_CHANGE_STATE_TEST_DATA :RenderPackageChangeStateTestData = [
    (
        'template-add',
        PackageState(State.ADD, Package('faux_package', '==0.0.1')),
        '- faux_package==0.0.1 (add)',
    ),
    (
        'template-remove',
        PackageState(State.REMOVE, Package('faux_package', '==0.0.1')),
        '- faux_package==0.0.1 (remove)',
    ),
    (
        'template-upgrade',
        PackageState(State.UPGRADE, Package('faux_package', '==0.0.2'), from_version=Version('0.0.1')),
        '- faux_package==0.0.2 (upgrade from 0.0.1)',
    ),
    (
        'template-downgrade',
        PackageState(State.DOWNGRADE, Package('faux_package', '==0.0.1'), from_version=Version('0.0.2')),
        '- faux_package==0.0.1 (downgrade from 0.0.2)',
    ),
    (
        'template-unknown',
        PackageState(10, Package('faux_package', '==0.0.1')),
        'Unknown',
    ),
]


@mark.parametrize(['from_pipfile_packages', 'curr_pipfile_packages', 'expected'], convert_test_data_to_params(PACKAGE_CHANGE_STATES_TEST_DATA))
def test_package_changes(from_pipfile_packages :FromPipfilePackages, curr_pipfile_packages :CurrPipfilePackages, expected :PackageChangeStatesExpected, monkeypatch :MonkeyPatch) -> None:
    monkeypatch.setattr('pathlib.Path.is_file', lambda _: True)
    monkeypatch.setattr('package_diff.pipfile.load_pipfile_lock', lambda _: dict(default=curr_pipfile_packages))
    monkeypatch.setattr('package_diff.pipfile.load_pipfile_lock_from_git_head', lambda _: dict(default=from_pipfile_packages))

    package_states = get_package_change_states(Mock())

    assert list(package_states) == expected


@mark.parametrize(['package_state', 'expected'], convert_test_data_to_params(RENDER_PACKAGE_CHANGE_STATE_TEST_DATA))
def test_render_package_change_state(package_state :PackageState, expected) -> None:
    add_template           = '- $package (add)'
    remove_template        = '- $package (remove)'
    upgrade_template       = '- $package (upgrade from $from_version)'
    downgrade_template     = '- $package (downgrade from $from_version)'

    render_package_change_state_ = partial(
        render_package_change_state,
        add_template,
        remove_template,
        upgrade_template,
        downgrade_template
    )

    rendered = render_package_change_state_(package_state)

    assert rendered == expected

from typing import Dict
from typing import List
from typing import Tuple
from unittest.mock import Mock

from pytest import MonkeyPatch
from pytest import mark

from package_diff.pipfile import State
from package_diff.pipfile import Package
from package_diff.pipfile import PackageState
from package_diff.pipfile import get_package_change_states
from package_diff.version import Version

from tests.params import ParamTestId
from tests.params import convert_test_data_to_params


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
@mark.parametrize(['from_pipfile_packages', 'curr_pipfile_packages', 'expected'], convert_test_data_to_params(PACKAGE_CHANGE_STATES_TEST_DATA))
def test_package_changes(from_pipfile_packages :FromPipfilePackages, curr_pipfile_packages :CurrPipfilePackages, expected :PackageChangeStatesExpected, monkeypatch :MonkeyPatch) -> None:
    monkeypatch.setattr('pathlib.Path.is_file', lambda _: True)
    monkeypatch.setattr('package_diff.pipfile.load_pipfile_lock', lambda _: dict(default=curr_pipfile_packages))
    monkeypatch.setattr('package_diff.pipfile.load_pipfile_lock_from_git_head', lambda _: dict(default=from_pipfile_packages))

    package_states = get_package_change_states(Mock(), 'default')

    assert list(package_states) == expected

from typing import List
from typing import Tuple
from functools import partial

from pytest import mark

from package_diff.pipfile import State
from package_diff.pipfile import Package
from package_diff.pipfile import PackageState
from package_diff.produce import render_package_change_state
from package_diff.version import Version

from tests.params import ParamTestId
from tests.params import convert_test_data_to_params


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

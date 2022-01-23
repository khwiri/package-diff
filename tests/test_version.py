from pytest import mark
from package_diff.version import Version


GREATER_THAN_TEST_DATA = [
    ('2.0.0', '1.0.0'),
    ('1.0.0',   '2.0'),
    (  '2.0', '0.1.0'),
]
@mark.parametrize(['version_left', 'version_right'], GREATER_THAN_TEST_DATA)
def test_version_compare_greater_than(version_left :str, version_right :str) -> None:
    assert Version(version_left) > Version(version_right)


LESS_THAN_TEST_DATA = [
    ('1.0.0', '2.0.0'),
    (  '2.0', '1.0.0'),
    ('0.1.0',   '2.0'),
]
@mark.parametrize(['version_left', 'version_right'], LESS_THAN_TEST_DATA)
def test_version_compare_less_than(version_left :str, version_right :str) -> None:
    assert Version(version_left) < Version(version_right)


EQUAL_TO_TEST_DATA = [
    ('1.0.0', '1.0.0'),
    ('0.2.0',   '2.0'),
    (  '2.0', '0.2.0'),
]
@mark.parametrize(['version_left', 'version_right'], EQUAL_TO_TEST_DATA)
def test_version_compare_equal_to(version_left :str, version_right :str) -> None:
    assert Version(version_left) == Version(version_right)


VERSION_STRING_COMPARE_TEST_DATA = [
    ('1.0.0',),
    (  '1.0',),
]
@mark.parametrize(['version'], VERSION_STRING_COMPARE_TEST_DATA)
def test_version_as_string(version :str) -> None:
    assert str(Version(version))  == version

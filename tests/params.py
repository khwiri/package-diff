from typing import Any
from typing import List
from typing import Tuple

from pytest import param
from _pytest.mark.structures import ParameterSet


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

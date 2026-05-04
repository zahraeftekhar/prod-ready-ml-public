from typing import cast

import pytest

from animal_shelter import data


def test_convert_camel_case() -> None:
    assert data.convert_camel_case("CamelCase") == "camel_case"
    assert data.convert_camel_case("CamelCASE") == "camel_case"
    assert data.convert_camel_case("camel-case") != "camel_case"


# def test_convert_camel_case_raises_type_error():
#     with pytest.raises(TypeError):
#         data.convert_camel_case(123)


def test_convert_camel_case_raises_type_error_message() -> None:
    with pytest.raises(TypeError, match="str"):
        data.convert_camel_case(cast(str, 123))
    # assert "str" in str(exc.value).lower()

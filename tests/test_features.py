import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_series_equal

from animal_shelter import features


def test_check_has_name() -> None:
    s = pd.Series(["Ivo", "Henk", "unknown"])
    result = features.check_has_name(s)
    expected = pd.Series([True, True, False])
    assert_series_equal(result, expected)


def test_check_is_dog() -> None:
    s = pd.Series(["dog", "Dog", "cat", "DOG"])
    result = features.check_is_dog(s)
    expected = pd.Series([True, True, False, True])
    assert_series_equal(result, expected)

    # def test_get_sex():
    #     s = pd.Series(
    #         [
    #             "Neutered Male",
    #             "Spayed Female",
    #             "Intact Male",
    #             "Intact Female",
    #             "Unknown",
    #             None,
    #         ]
    #     )

    #     result = features.get_sex(s)

    #     expected = pd.Series(
    #         [
    #             "male",
    #             "female",
    #             "male",
    #             "female",
    #             "unknown",
    #             "unknown",
    #         ]
    #     )

    assert_series_equal(result, expected)


# def test_get_neutered():
#     s = pd.Series(["Neutered Male", "Spayed Female", "Intact Male", "Unknown", None])
#     result = features.get_neutered(s)
#     expected = pd.Series(["fixed", "fixed", "intact", "unknown", "unknown"])
#     assert_series_equal(result, expected)


def test_get_hair_type() -> None:
    s = pd.Series(
        [
            "Domestic Shorthair Mix",
            "Domestic Short Hair",
            "Domestic Medium Hair",
            "Domestic Mediumhair",
            "Domestic Longhair",
            "Domestic Long Hair",
            "Siamese",
            None,
        ]
    )
    result = features.get_hair_type(s)
    expected = pd.Series(
        [
            "shorthair",
            "shorthair",
            "medium hair",
            "medium hair",
            "longhair",
            "longhair",
            "unknown",
            "unknown",
        ]
    )
    assert_series_equal(result, expected)


def test_compute_days_upon_outcome() -> None:
    s = pd.Series(["2 years", "3 months", "4 weeks", "5 days", "Unknown", None])
    result = features.compute_days_upon_outcome(s)
    expected = pd.Series([730.0, 90.0, 28.0, 5.0, np.nan, np.nan])
    assert_series_equal(result, expected)


def test_add_features() -> None:
    df = pd.DataFrame(
        {
            "animal_type": ["Dog", "Cat"],
            "name": ["Buddy", "unknown"],
            "sex_upon_outcome": ["Neutered Male", "Spayed Female"],
            "breed": ["Domestic Shorthair Mix", "Domestic Longhair"],
            "age_upon_outcome": ["2 years", "3 months"],
        }
    )

    result = features.add_features(df)

    assert_series_equal(result["is_dog"], pd.Series([True, False], name="is_dog"))
    assert_series_equal(result["has_name"], pd.Series([True, False], name="has_name"))
    assert_series_equal(result["sex"], pd.Series(["male", "female"], name="sex"))
    assert_series_equal(
        result["neutered"], pd.Series(["fixed", "fixed"], name="neutered")
    )
    assert_series_equal(
        result["hair_type"], pd.Series(["shorthair", "longhair"], name="hair_type")
    )
    assert_series_equal(
        result["days_upon_outcome"],
        pd.Series([730.0, 90.0], name="days_upon_outcome"),
    )


@pytest.fixture(scope="module")  # type: ignore[misc]
def sex_upon_outcome() -> pd.Series:
    return pd.Series(
        [
            "Neutered Male",
            "Spayed Female",
            "Intact Male",
            "Intact Female",
            "Unknown",
            None,
        ]
    )


def test_get_sex(sex_upon_outcome: pd.Series) -> None:
    result = features.get_sex(sex_upon_outcome)

    expected = pd.Series(
        [
            "male",
            "female",
            "male",
            "female",
            "unknown",
            "unknown",
        ]
    )

    assert_series_equal(result, expected)


def test_get_neutered(sex_upon_outcome: pd.Series) -> None:
    result = features.get_neutered(sex_upon_outcome)

    expected = pd.Series(
        [
            "fixed",
            "fixed",
            "intact",
            "intact",
            "unknown",
            "unknown",
        ]
    )

    assert_series_equal(result, expected)

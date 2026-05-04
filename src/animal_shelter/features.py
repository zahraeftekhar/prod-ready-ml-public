import numpy as np
import pandas as pd


def add_features(df):
    """Add some features to our data.
    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with data (see load_data)
    Returns
    -------
    with_features : pandas.DataFrame
        DataFrame with some column features added
    """
    df["is_dog"] = check_is_dog(df["animal_type"])

    # Check if it has a name.
    df["has_name"] = df["name"].str.lower() != "unknown"

    # Get sex.
    sexUponOutcome = df["sex_upon_outcome"]
    sex = pd.Series("unknown", index=sexUponOutcome.index)

    sex.loc[sexUponOutcome.str.endswith("Female")] = "female"
    sex.loc[sexUponOutcome.str.endswith("Male")] = "male"
    df["sex"] = sex

    # Check if neutered.
    neutered = sexUponOutcome.str.lower()
    neutered.loc[neutered.str.contains("neutered")] = "fixed"
    neutered.loc[neutered.str.contains("spayed")] = "fixed"

    neutered.loc[neutered.str.contains("intact")] = "intact"
    neutered.loc[~neutered.isin(["fixed", "intact"])] = "unknown"

    df["neutered"] = neutered

    # Get hair type.

    hairType = df["breed"].str.lower()
    Valid_hair_types = ["shorthair", "medium hair", "longhair"]

    for hair in Valid_hair_types:
        is_hair_type = hairType.str.contains(hair)
        hairType[is_hair_type] = hair

    hairType[~hairType.isin(Valid_hair_types)] = "unknown"

    df["hair_type"] = hairType

    # Age in days upon outcome.

    Split_Age = df["age_upon_outcome"].str.split()
    time = Split_Age.apply(lambda x: x[0] if x[0] != "Unknown" else np.nan)
    period = Split_Age.apply(lambda x: x[1] if x[0] != "Unknown" else None)
    period_Mapping = {
        "year": 365,
        "years": 365,
        "weeks": 7,
        "week": 7,
        "month": 30,
        "months": 30,
        "days": 1,
        "day": 1,
    }
    days_upon_outcome = time.astype(float) * period.map(period_Mapping)
    df["days_upon_outcome"] = days_upon_outcome

    return df


def check_is_dog(animal_type):
    """Check if the animal is a dog, otherwise return False.
    Parameters
    ----------
    animal_type : pandas.Series
        Type of animal
    Returns
    -------
    result : pandas.Series
        Dog or not
    """
    # Check if it's either a cat or a dog.
    is_cat_dog = animal_type.str.lower().isin(["dog", "cat"])
    if not is_cat_dog.all():
        print("Found something else but dogs and cats:\n%s", animal_type[~is_cat_dog])
        raise RuntimeError("Found pets that are not dogs or cats.")
    is_dog = animal_type.str.lower() == "dog"
    return is_dog

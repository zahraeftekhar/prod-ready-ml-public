import numpy as np
import pandas as pd

# 1) from packaging excersize
# def add_features(df):
#     """Add some features to our data.
#     Parameters
#     ----------
#     df : pandas.DataFrame
#         DataFrame with data (see load_data)
#     Returns
#     -------
#     with_features : pandas.DataFrame
#         DataFrame with some column features added
#     """
#     df['is_dog'] = check_is_dog(df['animal_type'])


#     # Check if it has a name.
#     df['has_name'] = df['name'].str.lower() != 'unknown'


#     # Get sex.
#     sexUponOutcome = df['sex_upon_outcome']
#     sex = pd.Series('unknown', index=sexUponOutcome.index)

#     sex.loc[sexUponOutcome.str.endswith('Female')] = 'female'
#     sex.loc[sexUponOutcome.str.endswith('Male')] = 'male'
#     df['sex'] = sex


#     # Check if neutered.
#     neutered = sexUponOutcome.str.lower()
#     neutered.loc[neutered.str.contains('neutered')] = 'fixed'
#     neutered.loc[neutered.str.contains('spayed')] = 'fixed'


#     neutered.loc[neutered.str.contains('intact')] = 'intact'
#     neutered.loc[~neutered.isin(['fixed', 'intact'])] = 'unknown'


#     df['neutered'] = neutered


#     # Get hair type.

#     hairType = df['breed'].str.lower()
#     Valid_hair_types = ['shorthair', 'medium hair', 'longhair']


#     for hair in Valid_hair_types:
#         is_hair_type = hairType.str.contains(hair)
#         hairType[is_hair_type] = hair

#     hairType[~hairType.isin(Valid_hair_types)] = 'unknown'


#     df['hair_type'] = hairType


#     # Age in days upon outcome.

#     Split_Age = df['age_upon_outcome'].str.split()
#     time = Split_Age.apply(lambda x: x[0] if x[0] != 'Unknown' else np.nan)
#     period = Split_Age.apply(lambda x: x[1] if x[0] != 'Unknown' else None)
#     period_Mapping = {'year': 365, 'years': 365, 'weeks': 7, 'week': 7,
#                       'month': 30, 'months': 30, 'days': 1, 'day': 1}
#     days_upon_outcome = time.astype(float) * period.map(period_Mapping)
#     df['days_upon_outcome'] = days_upon_outcome


#     return df

# def check_is_dog(animal_type):
#     """Check if the animal is a dog, otherwise return False.
#     Parameters
#     ----------
#     animal_type : pandas.Series
#         Type of animal
#     Returns
#     -------
#     result : pandas.Series
#         Dog or not
#     """
#     # Check if it's either a cat or a dog.
#     is_cat_dog = animal_type.str.lower().isin(['dog', 'cat'])
#     if not is_cat_dog.all():
#         print('Found something else but dogs and cats:\n%s',
#               animal_type[~is_cat_dog])
#         raise RuntimeError("Found pets that are not dogs or cats.")
#     is_dog = animal_type.str.lower() == 'dog'
#     return is_dog

# 2) from code quality excersize


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["is_dog"] = check_is_dog(df["animal_type"])
    df["has_name"] = check_has_name(df["name"])
    df["sex"] = get_sex(df["sex_upon_outcome"])
    df["neutered"] = get_neutered(df["sex_upon_outcome"])
    df["hair_type"] = get_hair_type(df["breed"])
    df["days_upon_outcome"] = compute_days_upon_outcome(df["age_upon_outcome"])

    return df


def check_is_dog(animal_type: pd.Series) -> pd.Series:
    animal_type = animal_type.str.lower()

    is_cat_dog = animal_type.isin(["dog", "cat"])
    if not is_cat_dog.all():
        raise RuntimeError("Found pets that are not dogs or cats.")

    return animal_type == "dog"


def check_has_name(name: pd.Series) -> pd.Series:
    return name.notna() & (name.str.lower().str.strip() != "unknown")


def get_sex(sex_upon_outcome: pd.Series) -> pd.Series:
    sex_upon_outcome = sex_upon_outcome.fillna("").str.lower()

    sex = pd.Series("unknown", index=sex_upon_outcome.index)
    sex.loc[sex_upon_outcome.str.endswith("female")] = "female"
    sex.loc[sex_upon_outcome.str.endswith("male")] = "male"

    return sex


def get_neutered(sex_upon_outcome: pd.Series) -> pd.Series:
    sex_upon_outcome = sex_upon_outcome.fillna("").str.lower()

    neutered = pd.Series("unknown", index=sex_upon_outcome.index)
    neutered.loc[sex_upon_outcome.str.contains("neutered|spayed")] = "fixed"
    neutered.loc[sex_upon_outcome.str.contains("intact")] = "intact"

    return neutered


def get_hair_type(breed: pd.Series) -> pd.Series:
    breed = breed.fillna("").str.lower()

    hair_type = pd.Series("unknown", index=breed.index)
    hair_type.loc[breed.str.contains("shorthair|short hair")] = "shorthair"
    hair_type.loc[breed.str.contains("medium hair|mediumhair")] = "medium hair"
    hair_type.loc[breed.str.contains("longhair|long hair")] = "longhair"

    return hair_type


def compute_days_upon_outcome(age_upon_outcome: pd.Series) -> pd.Series:
    age = age_upon_outcome.fillna("unknown").str.lower().str.strip()

    split_age = age.str.split()
    value = split_age.apply(
        lambda x: float(x[0]) if len(x) >= 2 and x[0].isdigit() else np.nan
    )
    period = split_age.apply(lambda x: x[1] if len(x) >= 2 and x[0].isdigit() else None)

    period_mapping = {
        "year": 365,
        "years": 365,
        "month": 30,
        "months": 30,
        "week": 7,
        "weeks": 7,
        "day": 1,
        "days": 1,
    }

    return value * period.map(period_mapping)

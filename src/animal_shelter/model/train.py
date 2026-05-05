from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from animal_shelter.data import load_data
from animal_shelter.features import add_features

CAT_FEATURES = ["animal_type", "is_dog", "has_name", "sex", "hair_type"]
NUM_FEATURES = ["days_upon_outcome"]
TARGET = "outcome_type"


def train(data_path: str | Path, model_path: str | Path) -> Pipeline:
    """Train model given a data path and save it to model path."""
    raw_data = load_data(data_path)
    data = add_features(raw_data)

    model = _build_pipeline()
    model = _fit_model(model, data)
    _save_model(model, model_path)

    return model


def _build_pipeline() -> Pipeline:
    """Build the sklearn model pipeline."""
    num_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer()),
            ("scaler", StandardScaler()),
        ]
    )

    cat_transformer = Pipeline(
        steps=[
            ("onehot", OneHotEncoder(drop="first", handle_unknown="ignore")),
        ]
    )

    transformer = ColumnTransformer(
        transformers=[
            ("numeric", num_transformer, NUM_FEATURES),
            ("categorical", cat_transformer, CAT_FEATURES),
        ]
    )

    return Pipeline(
        steps=[
            ("transformer", transformer),
            ("model", RandomForestClassifier()),
        ]
    )


def _fit_model(model: Pipeline, data: pd.DataFrame) -> Pipeline:
    """Train the sklearn pipeline."""
    x = data[CAT_FEATURES + NUM_FEATURES]
    y = data[TARGET]

    model.fit(x, y)
    return model


def _save_model(model: Pipeline, model_path: str | Path) -> None:
    """Save the trained model."""
    model_path = Path(model_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)

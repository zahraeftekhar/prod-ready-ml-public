from pathlib import Path

import joblib
import pandas as pd

from animal_shelter.data import load_data
from animal_shelter.features import add_features
from animal_shelter.model.train import CAT_FEATURES, NUM_FEATURES


def predict(data_path: str | Path, model_path: str | Path) -> pd.Series:
    """Generate predictions using a saved model."""
    data = load_data(data_path)
    data = add_features(data)

    model = _load_model(model_path)
    predictions = _predict(model, data)

    return pd.Series(predictions, index=data.index, name="prediction")


def _load_model(model_path: str | Path):
    """Load a trained model."""
    return joblib.load(model_path)


def _predict(model, data: pd.DataFrame):
    """Generate predictions from the model."""
    x = data[CAT_FEATURES + NUM_FEATURES]
    return model.predict(x)

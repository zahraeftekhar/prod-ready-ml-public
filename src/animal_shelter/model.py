from pathlib import Path

import joblib
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

FEATURE_COLUMNS = [
    "is_dog",
    "has_name",
    "sex",
    "neutered",
    "hair_type",
    "days_upon_outcome",
]


def build_feature_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Convert engineered features into a model-ready matrix."""
    features = pd.get_dummies(df[FEATURE_COLUMNS], dummy_na=True)
    return features.fillna(0)


def train_decision_tree(
    features: pd.DataFrame,
    labels: pd.Series,
    *,
    max_depth: int = 3,
    random_state: int = 42,
) -> DecisionTreeClassifier:
    """Train a simple decision tree classifier."""
    model = DecisionTreeClassifier(max_depth=max_depth, random_state=random_state)
    model.fit(features, labels)
    return model


def save_model(model: DecisionTreeClassifier, path: Path | str) -> Path:
    """Persist a fitted model and verify that it was written to disk."""
    model_path = Path(path)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)

    if not model_path.is_file():
        raise RuntimeError(f"Model was not saved to {model_path}")

    model_path.read_bytes()

    return model_path


def load_model(path: Path | str) -> DecisionTreeClassifier:
    """Load a saved model from disk."""
    return joblib.load(Path(path))

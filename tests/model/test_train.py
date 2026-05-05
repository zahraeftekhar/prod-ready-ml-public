import pandas as pd
from sklearn.pipeline import Pipeline

from animal_shelter.model.train import _build_pipeline, _fit_model


def test_build_pipeline() -> None:
    model = _build_pipeline()

    assert isinstance(model, Pipeline)
    assert "transformer" in model.named_steps
    assert "model" in model.named_steps


def test_fit_model() -> None:
    data = pd.DataFrame(
        {
            "animal_type": ["Dog", "Cat"],
            "is_dog": [True, False],
            "has_name": [True, False],
            "sex": ["male", "female"],
            "hair_type": ["shorthair", "longhair"],
            "days_upon_outcome": [365.0, 120.0],
            "outcome_type": ["Adoption", "Transfer"],
        }
    )

    model = _build_pipeline()
    fitted_model = _fit_model(model, data)

    assert isinstance(fitted_model, Pipeline)

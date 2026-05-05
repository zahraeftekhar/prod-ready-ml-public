import pandas as pd

from animal_shelter.model.predict import _predict
from animal_shelter.model.train import _build_pipeline, _fit_model


def test_predict() -> None:
    train_data = pd.DataFrame(
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

    model = _fit_model(_build_pipeline(), train_data)

    test_data = train_data.drop(columns=["outcome_type"])
    predictions = _predict(model, test_data)

    assert len(predictions) == len(test_data)

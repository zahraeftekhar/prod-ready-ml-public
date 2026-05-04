# from pathlib import Path

# import pandas as pd

# from animal_shelter.model import (
#     build_feature_matrix,
#     load_model,
#     save_model,
#     train_decision_tree,
# )


# def _sample_feature_frame() -> pd.DataFrame:
#     return pd.DataFrame(
#         {
#             "is_dog": [True, False],
#             "has_name": [True, False],
#             "sex": ["male", "female"],
#             "neutered": ["fixed", "intact"],
#             "hair_type": ["shorthair", "longhair"],
#             "days_upon_outcome": [365.0, 30.0],
#         }
#     )


# # def test_build_feature_matrix_creates_expected_columns() -> None:
# #     features = build_feature_matrix(_sample_feature_frame())

# #     assert len(features) == 2
# #     assert any(column.startswith("is_dog_") for column in features.columns)
# #     assert any(column.startswith("sex_") for column in features.columns)
# #     assert any(column.startswith("neutered_") for column in features.columns)
# #     assert any(column.startswith("hair_type_") for column in features.columns)
# #     assert "days_upon_outcome" in features.columns


# def test_train_decision_tree_fits_and_predicts() -> None:
#     features = build_feature_matrix(_sample_feature_frame())
#     labels = pd.Series(["adoption", "transfer"])

#     model = train_decision_tree(features, labels, max_depth=2, random_state=123)

#     assert model.get_depth() <= 2
#     assert list(model.predict(features)) == ["adoption", "transfer"]


# def test_save_and_load_model_roundtrip(tmp_path: Path) -> None:
#     features = build_feature_matrix(_sample_feature_frame())
#     labels = pd.Series(["adoption", "transfer"])
#     model = train_decision_tree(features, labels)

#     model_path = tmp_path / "decision_tree.joblib"
#     saved_path = save_model(model, model_path)

#     assert saved_path == model_path
#     assert model_path.is_file()

#     loaded_model = load_model(saved_path)
#     assert list(loaded_model.predict(features)) == ["adoption", "transfer"]

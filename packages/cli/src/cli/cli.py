# """CLI using Typer."""

# import typer

# app = typer.Typer(
#     name="CLI using Typer"
# )

# @app.command()
# def say_hi(name):
#     """Say hello to the user."""
#     typer.echo(f"Hello: {name}")

# @app.command()
# def goodbye():
#     """Say goodbye to the user."""
#     typer.echo("Goodbye!")

# if __name__ == "__main__":
#     app()

import json
import logging
from pathlib import Path

import pandas as pd
import typer
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from animal_shelter.data import load_data
from animal_shelter.features import add_features
from animal_shelter.model import (
    FEATURE_COLUMNS,
    build_feature_matrix,
    load_model,
    save_model,
    train_decision_tree,
)

app = typer.Typer()


# Always gets called before all subcommands
@app.callback()
def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)-15s] %(name)s - %(levelname)s - %(message)s",
    )


def _prepare_training_data(input_path: Path) -> tuple[pd.DataFrame, pd.Series]:
    raw_data = load_data(input_path)
    featured_data = add_features(raw_data)
    features = build_feature_matrix(featured_data)
    labels = raw_data["outcome_type"].str.lower()
    return features, labels


def _compute_metrics(y_true: pd.Series, y_pred: pd.Series) -> dict[str, float]:
    """Compute a small summary of classification metrics."""
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, average="macro", zero_division=0),
        "recall": recall_score(y_true, y_pred, average="macro", zero_division=0),
        "f1": f1_score(y_true, y_pred, average="macro", zero_division=0),
    }


@app.command()
def train(input_path: Path, model_path: Path) -> None:
    """Trains a simple decision-tree classifier on dog/cat outcomes."""
    logger = logging.getLogger(__name__)
    logger.info("Loading input dataset from %s", input_path)

    features, labels = _prepare_training_data(input_path)
    logger.info(
        "Training model on %d rows and %d features",
        len(features),
        len(features.columns),
    )
    model = train_decision_tree(features, labels, max_depth=3, random_state=42)
    saved_model_path = save_model(model, model_path)
    reloaded_model = load_model(saved_model_path)

    typer.echo(f"Trained decision tree on {len(features)} rows.")
    typer.echo(f"Model saved to {saved_model_path}")
    typer.echo(f"Reloaded model depth: {reloaded_model.get_depth()}")


@app.command()
def predict(input_path: Path, model_path: Path, output_path: Path) -> None:
    """Applies a trained model to the given dataset."""
    logger = logging.getLogger(__name__)
    logger.info("Loading input dataset from %s", input_path)

    raw_data = load_data(input_path)
    featured_data = add_features(raw_data)
    features = build_feature_matrix(featured_data)
    model = load_model(model_path)
    predictions = model.predict(features)

    id_column = "animal_id" if "animal_id" in raw_data.columns else "id"
    output = raw_data[[id_column]].copy()
    output["predicted_outcome_type"] = predictions
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(output_path, index=False)

    typer.echo(f"Saved {len(output)} predictions to {output_path}\n")

    # Display prediction summary
    typer.echo("=== PREDICTION SUMMARY ===")
    pred_counts = pd.Series(predictions).value_counts().sort_values(ascending=False)
    typer.echo(f"Total predictions: {len(predictions)}")
    for outcome, count in pred_counts.items():
        pct = 100 * count / len(predictions)
        typer.echo(f"  {outcome:20s}: {count:5d} ({pct:5.1f}%)")

    # Display sample predictions with engineered features
    typer.echo("\n=== SAMPLE PREDICTIONS + FEATURES (first 10 rows) ===")
    sample = featured_data[[id_column, *FEATURE_COLUMNS]].copy().head(10)
    sample["predicted_outcome_type"] = predictions[: len(sample)]
    typer.echo(sample.to_string(index=False))
    logger.info("predictions saved to %s", output_path)

    # Compute and display metrics if true labels are available
    if "outcome_type" in raw_data.columns:
        metrics = _compute_metrics(raw_data["outcome_type"].str.lower(), predictions)
        metrics_path = output_path.with_suffix(".metrics.json")
        metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

        typer.echo("\n=== METRICS ===")
        typer.echo(
            f"Accuracy:  {metrics['accuracy']:.3f}\n"
            f"Precision: {metrics['precision']:.3f}\n"
            f"Recall:    {metrics['recall']:.3f}\n"
            f"F1 Score:  {metrics['f1']:.3f}"
        )
        typer.echo(f"Saved metrics to {metrics_path}")
    else:
        typer.echo("\n⚠️  No outcome_type column found—skipping metrics computation.")

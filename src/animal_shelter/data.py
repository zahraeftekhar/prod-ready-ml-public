import logging
import re

import pandas as pd

logger = logging.getLogger(__name__)


def load_data(path):
    logger.info(f"Loading data from {path}")

    df = (
        pd.read_csv(path, parse_dates=["DateTime"])
        .rename(columns=lambda x: x.replace("upon", "Upon"))
        .rename(columns=convert_camel_case)
        .fillna("Unknown")
    )

    logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")
    logger.debug(f"Columns: {list(df.columns)}")

    return df


def convert_camel_case(name: str) -> str:
    """Convert camelCaseString to snake_case_string."""
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

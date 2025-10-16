"""
CSV loading + validation using pandas.
- train.csv: x, y1, y2, y3, y4
- ideal.csv: x, y1..y50
- test.csv:  x, y
"""

from typing import List
import pandas as pd
from .exceptions import DataValidationError


class CSVLoader:
    """Loads and validates CSV data into pandas DataFrames."""

    def __init__(self, path: str, required_min_cols: int = 2):
        self.path = path
        self.required_min_cols = required_min_cols

    def load(self) -> pd.DataFrame:
        """Load CSV and perform basic sanity checks."""
        try:
            df = pd.read_csv(self.path)
        except FileNotFoundError as e:
            raise DataValidationError(f"File not found: {self.path}") from e
        except pd.errors.EmptyDataError as e:
            raise DataValidationError(f"Empty CSV file: {self.path}") from e

        if df.shape[1] < self.required_min_cols:
            raise DataValidationError(
                f"{self.path} must have at least {self.required_min_cols} columns."
            )
        if df.isnull().any().any():
            raise DataValidationError(f"{self.path} contains missing values.")

        # enforce first column named 'x' (IU convention); if not, rename it
        first_col = df.columns[0]
        if first_col.lower() != "x":
            df = df.rename(columns={first_col: "x"})

        # make sure x is numeric and sorted
        try:
            df["x"] = pd.to_numeric(df["x"])
        except ValueError:
            raise DataValidationError(f"{self.path} has non-numeric x values.")

        # sort by x and reset index (keeps downstream merges clean)
        df = df.sort_values("x").reset_index(drop=True)
        return df


def assert_same_x_grid(dfs: List[pd.DataFrame]) -> None:
    """Ensure all provided DataFrames share the exact same x grid."""
    if not dfs:
        return
    x0 = dfs[0]["x"].values
    for i, df in enumerate(dfs[1:], start=2):
        if not (df["x"].values == x0).all():
            raise DataValidationError(
                f"CSV #{i} has x-values not matching the others. "
             
            )

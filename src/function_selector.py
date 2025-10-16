"""
Select 4 ideal functions that best fit each training column by least-squares.
Also compute max |y_train - y_ideal| over training grid for √2 mapping threshold.
"""


from typing import Dict, List
import numpy as np
import pandas as pd


class FunctionSelector:
    """
    Given training_df (x, y1..y4) and ideal_df (x, y1..y50),
    find for each training column the ideal column minimizing sum of squared errors.
    """

    def __init__(self, training_df: pd.DataFrame, ideal_df: pd.DataFrame):
        self.training_df = training_df
        self.ideal_df = ideal_df

        # columns
        self.x_col = "x"
        self.train_cols: List[str] = [c for c in training_df.columns if c != self.x_col]
        self.ideal_cols: List[str] = [c for c in ideal_df.columns if c != self.x_col]

    def _ls_error(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        diff = y_true - y_pred
        return float(np.dot(diff, diff))  # sum of squares

    def select(self) -> Dict[str, Dict[str, float]]:
        """
        Returns dict keyed by training column, each value:
          {
            'ideal_col': str,
            'ls_error': float,
            'max_train_abs_dev': float
          }
        """
        # align on x (assumed identical & sorted; enforced by loader)
        results: Dict[str, Dict[str, float]] = {}
        x = self.training_df[self.x_col].values

        # build matrix arrays for speed
        train_mat = self.training_df[self.train_cols].to_numpy()  # n x 4
        ideal_mat = self.ideal_df[self.ideal_cols].to_numpy()     # n x 50

        for t_idx, t_col in enumerate(self.train_cols):
            y_true = train_mat[:, t_idx]

            # compute SSE vs all ideal cols vectorized
            # (y_true - ideal_col)^2 summed over rows
            diffs = y_true.reshape(-1, 1) - ideal_mat  # n x 50
            sse = (diffs ** 2).sum(axis=0)            # 50,
            best_j = int(np.argmin(sse))
            best_ideal_col = self.ideal_cols[best_j]

            # max absolute deviation on training grid for the chosen ideal
            max_abs_dev = float(np.abs(diffs[:, best_j]).max())

            results[t_col] = {
                "ideal_col": best_ideal_col,
                "ls_error": float(sse[best_j]),
                "max_train_abs_dev": max_abs_dev,
            }

        # the spec wants 4 training datasets → we return all 4 picks
        return results

    @staticmethod
    def ideal_thresholds(selected: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        """
        Map ideal_col → threshold (sqrt(2) * max_train_abs_dev).
        If the same ideal function is chosen for multiple training cols,
        we take the MAX of their thresholds (safest application of the rule).
        """
        out: Dict[str, float] = {}
        factor = np.sqrt(2.0)
        for info in selected.values():
            col = info["ideal_col"]
            thr = factor * info["max_train_abs_dev"]
            out[col] = max(out.get(col, 0.0), thr)
        return out

"""
Map each test (x,y) to the closest of the 4 selected ideal functions
IF its absolute deviation <= √2 * (max training deviation for that ideal).
"""

from typing import Dict, List
import numpy as np
import pandas as pd


class TestDataMapper:
    """Maps test points to selected ideal functions under the IU √2 rule."""

    def __init__(
        self,
        test_df: pd.DataFrame,
        ideal_df: pd.DataFrame,
        selected_map: Dict[str, Dict[str, float]],
    ):
        """
        selected_map: output of FunctionSelector.select()
        """
        self.test_df = test_df
        self.ideal_df = ideal_df
        self.selected_map = selected_map
        self.x_col = "x"
        self.test_y_col = [c for c in test_df.columns if c != self.x_col][0]

        # derive ideal thresholds {ideal_col: threshold}
        from .function_selector import FunctionSelector
        self.thresholds: Dict[str, float] = FunctionSelector.ideal_thresholds(selected_map)

        # the chosen ideal columns
        self.selected_ideals: List[str] = list(self.thresholds.keys())

    def map_points(self) -> pd.DataFrame:
        """
        Returns DataFrame with columns:
        x, y_test, ideal_func (or None), deviation (abs), accepted (bool)
        Only rows that PASS the rule are included (per spec: "… and save it … if so").
        """
        # fast lookup for ideal y via merge on x
        use_cols = [self.x_col] + self.selected_ideals
        ideal_sel = self.ideal_df[use_cols]

        merged = pd.merge(self.test_df, ideal_sel, on=self.x_col, how="left")
        records = []

        for _, row in merged.iterrows():
            x = float(row[self.x_col])
            y = float(row[self.test_y_col])

            best_name = None
            best_dev = np.inf

            for col in self.selected_ideals:
                y_pred = float(row[col])
                dev = abs(y - y_pred)
                if dev < best_dev:
                    best_dev = dev
                    best_name = col

            # apply √2 rule using that best ideal's threshold
            thr = self.thresholds.get(best_name, np.inf)
            if best_dev <= thr:
                records.append(
                    {"x": x, "y_test": y, "ideal_func": best_name, "deviation": best_dev}
                )

        return pd.DataFrame.from_records(records, columns=["x", "y_test", "ideal_func", "deviation"])

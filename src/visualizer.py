"""
Interactive visualization with Bokeh.
Shows the 4 training series and their paired ideal functions, plus mapped test points.
"""

from typing import Dict
import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, HoverTool


class BokehVisualizer:
    def __init__(self, title: str = "IU Function Mapping Visualization"):
        self.title = title

    def plot(
        self,
        training_df: pd.DataFrame,
        ideal_df: pd.DataFrame,
        mapped_df: pd.DataFrame,
        selected_map: Dict[str, Dict[str, float]],
    ) -> None:
        """
        training_df: x,y1..y4
        ideal_df:    x,y1..y50
        mapped_df:   x,y_test,ideal_func,deviation   (only accepted points)
        selected_map: {train_col: {'ideal_col': ..., 'ls_error': ..., 'max_train_abs_dev': ...}}
        """
        output_file("function_mapping_visual.html")

        p = figure(title=self.title, width=1000, height=560)
        p.xaxis.axis_label = "x"
        p.yaxis.axis_label = "y"

        x = training_df["x"]

        # plot each training column
        for t_col, info in selected_map.items():
            p.line(x, training_df[t_col], line_width=2, legend_label=f"train:{t_col}")

            ideal_col = info["ideal_col"]
            p.line(
                ideal_df["x"],
                ideal_df[ideal_col],
                line_width=2,
                line_dash="dashed",
                legend_label=f"ideal:{ideal_col}",
            )

        # mapped test points
        if not mapped_df.empty:
            cds = ColumnDataSource(mapped_df.rename(columns={"x": "xv", "y_test": "yv"}))
            r = p.circle("xv", "yv", size=6, source=cds, legend_label="mapped test")
            hover = HoverTool(
                renderers=[r],
                tooltips=[("x", "@xv"), ("y", "@yv"), ("ideal", "@ideal_func"), ("|Δ|", "@deviation")],
            )
            p.add_tools(hover)

        p.legend.click_policy = "hide"
        show(p)

"""
Debug-safe orchestrator for the IU DLMDSPWP01 Function Mapping assignment.
Run from project root:  python -m src.main
"""

import os
import sys
from .data_loader import CSVLoader, assert_same_x_grid
from .database_manager import DatabaseManager
from .function_selector import FunctionSelector
from .mapper import TestDataMapper
from .visualizer import BokehVisualizer


def log(msg: str):
    """Simple progress logger that always flushes."""
    print(msg)
    sys.stdout.flush()


def main():
    log("🔹 Starting Function Mapping pipeline...")

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(root, "data")
    db_path = os.path.join(root, "function_mapping.db")
    html_path = os.path.join(root, "function_mapping_visual.html")

    try:
        log("➡️  Loading datasets...")
        train_df = CSVLoader(os.path.join(data_dir, "train.csv")).load()
        ideal_df = CSVLoader(os.path.join(data_dir, "ideal.csv")).load()
        test_df = CSVLoader(os.path.join(data_dir, "test.csv")).load()
        log("   ✅ Data loaded successfully.")

        assert_same_x_grid([train_df, ideal_df])
        log("   ✅ X grids verified identical.")

        db = DatabaseManager(db_path)
        db.insert_dataframe(train_df, "training_data")
        db.insert_dataframe(ideal_df, "ideal_functions")
        db.insert_dataframe(test_df, "test_data_raw")
        log("   ✅ Data inserted into SQLite DB.")

        selector = FunctionSelector(train_df, ideal_df)
        selected_map = selector.select()
        log("   ✅ Selected ideal functions:")
        for k, v in selected_map.items():
            log(f"      {k} -> {v['ideal_col']}")

        mapper = TestDataMapper(test_df, ideal_df, selected_map)
        mapped_df = mapper.map_points()
        db.insert_dataframe(mapped_df, "mapped_test_data")
        log(f"   ✅ Mapped {len(mapped_df)} test points to ideal functions.")

        vis = BokehVisualizer()
        vis.plot(
            training_df=train_df,
            ideal_df=ideal_df,
            mapped_df=mapped_df,
            selected_map=selected_map,
        )
        log("   ✅ Visualization generated.")

        log("\n📁 Created files:")
        for f in [db_path, html_path]:
            log(f" - {f}  exists? {os.path.exists(f)}")

    except Exception as e:
        log(f"❌ ERROR: {type(e).__name__} - {e}")
        raise


if __name__ == "__main__":
    main()

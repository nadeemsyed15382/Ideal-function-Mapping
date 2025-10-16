"""
SQLite via SQLAlchemy helpers.
Creates/replaces tables from DataFrames.
"""

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
from .exceptions import DatabaseError


class DatabaseManager:
    """Handles database setup and inserts using pandas + SQLAlchemy."""

    def __init__(self, db_path: str = "function_mapping.db"):
        # check_same_thread=False not needed here; single-threaded use
        self.engine = create_engine(f"sqlite:///{db_path}")

    def insert_dataframe(self, df: pd.DataFrame, table_name: str) -> None:
        """Replace table with the DataFrame contents."""
        try:
            df.to_sql(table_name, self.engine, if_exists="replace", index=False)
        except SQLAlchemyError as e:
            raise DatabaseError(f"Insert failed for table '{table_name}': {e}") from e

import pandas as pd
from typing import Optional, Any
from .types import StringMapper, ColumnList, StringDict
from .cleanup import Cleanup


def cleanup_dataframe(
        df: pd.DataFrame,
        rename_columns: Optional[StringMapper] = None,
        column_cleanup_mode: int = Cleanup.NONE,
        mandatory_columns: Optional[ColumnList] = None,
        dtype_conversions: Optional[StringDict] = None,
        fillna_value: Any = None) -> pd.DataFrame:
    df = df.rename(columns=lambda x: Cleanup.cleanup(x, cleanup_mode=column_cleanup_mode))

    if rename_columns is not None:
        df = df.rename(columns=rename_columns)

    if mandatory_columns is not None:
        missing_columns: list = list()
        for c in mandatory_columns:
            if Cleanup.cleanup(c, cleanup_mode=column_cleanup_mode) not in df.columns:
                missing_columns.append(c)
        if len(missing_columns) > 0:
            raise ValueError(f"Missing input dataframe columns: {missing_columns}\n")

    if dtype_conversions is not None:
        for (c, t) in dtype_conversions.items():
            df[c] = df[c].astype(t)

    if fillna_value is not None:
        df.fillna(value=fillna_value, inplace=True)

    return df

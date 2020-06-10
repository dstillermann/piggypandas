import pandas as pd
from pathlib import Path
from typing import Any, Optional, Union, List, Mapping, Callable
# import xlsxwriter as xls
from .cleanup import Cleanup


StringMapper = Union[Mapping[str, str], Callable[[str], str]]
ColumnList = List[str]


def read_dataframe(path: Union[str, Path],
                   sheet_name: Optional[str] = None,
                   column_cleanup_mode: int = Cleanup.CASE_SENSITIVE,
                   rename_columns: Optional[StringMapper] = None,
                   mandatory_columns: Optional[ColumnList] = None,
                   dtype_conversions: Optional[StringMapper] = None,
                   fillna_value: Any = None
                   ) -> pd.DataFrame:
    file_in: Path = path if isinstance(path, Path) else Path(path)

    d_in: pd.DataFrame
    if not file_in.is_file():
        raise FileNotFoundError(f"File {str(file_in)} does not exist")
    elif file_in.suffix in ['.csv']:
        d_in = pd.read_csv(str(file_in))
    elif file_in.suffix in ['.xls', '.xlsx']:
        d_in = pd.read_excel(str(file_in), sheet_name=sheet_name)
    else:
        raise NotImplementedError(f"Can not read {str(file_in)}, unsupported format")

    d_in = d_in.rename(columns=lambda x: Cleanup.cleanup(x, cleanup_mode=column_cleanup_mode))

    if rename_columns is not None:
        d_in = d_in.rename(columns=rename_columns)

    if mandatory_columns is not None:
        missing_columns: list = list()
        for c in mandatory_columns:
            if Cleanup.cleanup(c, cleanup_mode=column_cleanup_mode) not in d_in.columns:
                missing_columns.append(c)
        if len(missing_columns) > 0:
            raise ValueError(f"Missing input dataframe columns: {missing_columns}\n")

    if dtype_conversions is not None:
        for (c, t) in dtype_conversions.items():
            d_in[c] = d_in[c].astype(t)

    if fillna_value is not None:
        d_in.fillna(value=fillna_value, inplace=True)

    return d_in

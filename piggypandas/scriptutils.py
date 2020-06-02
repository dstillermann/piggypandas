import pandas as pd
from pathlib import Path
from typing import Optional, Union, List, Dict
# import xlsxwriter as xls
from .cleanup import Cleanup


def read_dataframe(path: Union[str, Path],
                   sheet_name: Optional[str] = None,
                   mandatory_columns: Optional[List[str]] = None,
                   dtype_conversions: Optional[Dict[str, str]] = None,
                   rename_columns: Optional[Dict[str, str]] = None,
                   cleanup_mode: int = Cleanup.CASE_SENSITIVE
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

    if rename_columns is not None:
        d_in = d_in.rename(columns=rename_columns)

    d_in = d_in.rename(columns=lambda x: Cleanup.cleanup(x, cleanup_mode=cleanup_mode))

    if mandatory_columns is not None:
        missing_columns: list = list()
        for c in mandatory_columns:
            if Cleanup.cleanup(c, cleanup_mode=cleanup_mode) not in d_in.columns:
                missing_columns.append(c)
        if len(missing_columns) > 0:
            raise ValueError(f"Missing input dataframe columns: {missing_columns}\n")

    if dtype_conversions is not None:
        for (c, t) in dtype_conversions.items():
            d_in[c] = d_in[c].astype(t)

    return d_in


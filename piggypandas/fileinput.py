import pandas as pd
from pathlib import Path
from typing import Any, Optional, Union
from .cleanup import Cleanup
from .types import ColumnList, StringMapper
from .dfutils import cleanup_dataframe


def read_dataframe(path: Union[str, Path],
                   sheet_name: Optional[str] = None,
                   rename_columns: Optional[StringMapper] = None,
                   column_cleanup_mode: int = Cleanup.CASE_SENSITIVE,
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

    return cleanup_dataframe(d_in,
                             rename_columns=rename_columns,
                             column_cleanup_mode=column_cleanup_mode,
                             mandatory_columns=mandatory_columns,
                             dtype_conversions=dtype_conversions,
                             fillna_value=fillna_value)

import adodbapi
import pandas as pd
import re
from typing import Optional, Any
from .types import ColumnList, StringMapper, ColumnREMapper
from .cleanup import Cleanup
from .dfutils import cleanup_dataframe


def read_mdx(connection: adodbapi.Connection,
             mdx_cmd: str,
             column_map: Optional[ColumnREMapper] = None,
             rename_columns: Optional[StringMapper] = None,
             column_cleanup_mode: int = Cleanup.CASE_SENSITIVE,
             mandatory_columns: Optional[ColumnList] = None,
             dtype_conversions: Optional[StringMapper] = None,
             fillna_value: Any = None
             ) -> pd.DataFrame:
    with connection.cursor() as cur:
        cur.execute(mdx_cmd)
        r = cur.fetchall()
        col_arrays = r.ado_results

        data: dict = dict()
        if column_map is None:
            column_map = list()
        for raw_cname in r.columnNames.keys():
            found: bool = False
            for (pattern, cname) in column_map:
                if re.search(pattern, raw_cname, flags=re.IGNORECASE):
                    if cname in data:
                        raise KeyError(f"Duplicate column \"{cname}\"")
                    data[cname] = col_arrays[r.columnNames[raw_cname]]
                    found = True
                    break
            if not found:
                if raw_cname in data:
                    raise KeyError(f"Duplicate column \"{raw_cname}\"")
                data[raw_cname] = col_arrays[r.columnNames[raw_cname]]

        cur.close()
        d_in: pd.DataFrame = pd.DataFrame(data=data)

        return cleanup_dataframe(d_in,
                                 rename_columns=rename_columns,
                                 column_cleanup_mode=column_cleanup_mode,
                                 mandatory_columns=mandatory_columns,
                                 dtype_conversions=dtype_conversions,
                                 fillna_value=fillna_value)

import adodbapi
import pandas as pd
import re
from typing import Optional, Any
from .types import ColumnList, StringMapper, ColumnREMapper, StringDict
from .cleanup import Cleanup
from .dfutils import cleanup_dataframe
import logging

_logger = logging.getLogger(__name__)


def read_mdx(connection: adodbapi.Connection,
             mdx_cmd: str,
             column_map: Optional[ColumnREMapper] = None,
             rename_columns: Optional[StringMapper] = None,
             column_cleanup_mode: int = Cleanup.CASE_SENSITIVE,
             mandatory_columns: Optional[ColumnList] = None,
             dtype_conversions: Optional[StringDict] = None,
             fillna_value: Any = None
             ) -> pd.DataFrame:
    with connection.cursor() as cur:
        _logger.debug(f"executing MDX {mdx_cmd[:80]}")
        cur.execute(mdx_cmd)
        r = cur.fetchall()
        _logger.debug(f"MDX query complete")
        col_arrays = r.ado_results

        data: dict = dict()
        if column_map is None:
            column_map = list()
        for raw_cname in r.columnNames.keys():
            found: bool = False
            for (pattern, cname) in column_map:
                if re.search(pattern, raw_cname, flags=re.IGNORECASE):
                    if cname in data:
                        msg = f"Duplicate column \"{cname}\""
                        _logger.exception(msg)
                        raise KeyError(msg)
                    data[cname] = col_arrays[r.columnNames[raw_cname]]
                    found = True
                    break
            if not found:
                if raw_cname in data:
                    msg = f"Duplicate column \"{raw_cname}\""
                    _logger.exception(msg)
                    raise KeyError(msg)
                data[raw_cname] = col_arrays[r.columnNames[raw_cname]]

        cur.close()

        _logger.debug("creating dataframe")
        d_in: pd.DataFrame = pd.DataFrame(data=data)
        d_in = cleanup_dataframe(d_in,
                                 rename_columns=rename_columns,
                                 column_cleanup_mode=column_cleanup_mode,
                                 mandatory_columns=mandatory_columns,
                                 dtype_conversions=dtype_conversions,
                                 fillna_value=fillna_value)
        _logger.debug("dataframe created")

        return d_in

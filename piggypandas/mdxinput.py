import adodbapi
import pandas as pd
import re
from typing import List, Tuple, Optional, Mapping


def read_mdx(connection: adodbapi.Connection,
             mdx_cmd: str,
             column_map: Optional[List[Tuple[str, str]]] = None,
             column_list: Optional[List[str]] = None
             ) -> pd.DataFrame:
    if column_map is not None and column_list is not None:
        raise ValueError('Both column_map and column_list passed; expecting just one')

    with connection.cursor() as cur:
        cur.execute(mdx_cmd)
        r = cur.fetchall()
        col_arrays = r.ado_results

        data: dict = dict()
        if column_list is None:
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
        else:
            common_len: int = min(len(col_arrays), len(column_list))
            for i in range(common_len):
                cname: str = str(column_list[i])
                if cname in data:
                    raise KeyError(f"Duplicate column \"{cname}\"")
                data[cname] = col_arrays[i]
            reverse_col_map: Mapping[int, str] = {v: k for (k, v) in r.columnNames.items()}
            for i in range(common_len, len(col_arrays)):
                cname: str = str(column_list[i]) if i in reverse_col_map else f"Column {i}"
                if cname in data:
                    raise KeyError(f"Duplicate column \"{cname}\"")
                data[cname] = col_arrays[i]

        cur.close()
        df: pd.DataFrame = pd.DataFrame(data=data)
        return df


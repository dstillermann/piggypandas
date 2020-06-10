import adodbapi
import pandas as pd
import re
from typing import List, Tuple, Optional


def read_mdx(connection: adodbapi.Connection,
             mdx_cmd: str,
             column_map: Optional[List[Tuple[str, str]]] = None
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
        df: pd.DataFrame = pd.DataFrame(data=data)
        return df


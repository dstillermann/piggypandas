import pandas as pd
import xlsxwriter as xls
from pathlib import Path
from typing import Union, List, Mapping, Optional, Tuple, Dict
import re
import logging

_logger = logging.getLogger('piggypandas')

SheetDataFrame = Tuple[str, pd.DataFrame, Dict]
SheetDataFrameList = List[SheetDataFrame]
SheetFormat = Tuple[str, Mapping[str, str], float]
SheetFormatList = List[SheetFormat]


def write_dataframes(path: Union[str, Path],
                     sheets: SheetDataFrameList,
                     formats: Optional[SheetFormatList] = None
                     ):
    file_out: Path = path if isinstance(path, Path) else Path(path)
    if file_out.suffix in ['.xls', '.xlsx']:
        with pd.ExcelWriter(str(file_out), engine='xlsxwriter') as writer:
            for sheet_name, df, kwargs in sheets:
                df.to_excel(writer, sheet_name=sheet_name, **kwargs)

            wb: xls.Workbook = writer.book
            fmt_header = wb.add_format({'bold': True, 'text_wrap': True, 'align': 'center', 'valign': 'vcenter'})
            for ws in wb.worksheets():
                ws.set_row(row=0, height=48.0, cell_format=fmt_header)

            if formats is not None:
                compiled_formats = [(r, wb.add_format(d), w) for (r, d, w) in formats]

                for sheet_name, df, _ in sheets:
                    ws = writer.sheets[sheet_name]
                    for i in range(df.columns.size):
                        cname: str = df.columns[i]
                        for rgxp, fmt, width in compiled_formats:
                            if re.search(rgxp, cname, re.I):
                                ws.set_column(first_col=i, last_col=i, width=width, cell_format=fmt)
                                break

            writer.save()
    else:
        msg = f"Can't write {str(file_out)}, unsupported format"
        _logger.error(msg)
        raise NotImplementedError(msg)


def write_dataframe(path: Union[str, Path],
                    df: pd.DataFrame,
                    sheet_name: str,
                    formats: Optional[SheetFormatList],
                    **kwargs
                    ):
    write_dataframes(path=path,
                     sheets=[(sheet_name, df, kwargs)],
                     formats=formats)

import pandas as pd
import xlsxwriter as xls
from pathlib import Path
from typing import Union, List, Mapping, Optional, Tuple, Dict, Any
import re
import logging
import copy

_logger = logging.getLogger('piggypandas')

SheetDataFrame = Tuple[str, pd.DataFrame, Dict]
SheetDataFrameList = List[SheetDataFrame]
CellFormat = Mapping[str, Any]
SheetFormat = Tuple[str, CellFormat, float]
SheetFormatList = List[SheetFormat]


def write_dataframes(path: Union[str, Path],
                     sheets: SheetDataFrameList,
                     formats: Optional[SheetFormatList] = None,
                     common_format: Optional[CellFormat] = None,
                     header_format: Optional[CellFormat] = None
                     ):
    file_out: Path = path if isinstance(path, Path) else Path(path)
    if file_out.suffix in ['.xls', '.xlsx']:
        with pd.ExcelWriter(str(file_out), engine='xlsxwriter') as writer:
            wb: xls.Workbook = writer.book

            _common_format: Dict[str, Any] = dict()
            if common_format:
                _common_format = dict(common_format)

            def _add_format(cell_format: CellFormat) -> Any:
                return wb.add_format(_common_format | cell_format)

            if header_format:
                fmt_header = _add_format(header_format)
            else:
                fmt_header = _add_format({'bold': True, 'text_wrap': True})

            # To avoid pandas' nasty header formatting, we have to write and format the header ourselves
            # after we apply the user formats.
            for sheet_name, df, kwargs in sheets:
                new_kwargs = copy.copy(kwargs)
                new_kwargs['startrow'] = 1
                new_kwargs['header'] = False
                df.to_excel(writer, sheet_name=sheet_name, **new_kwargs)

            # Applying the user formats.
            if formats is not None:
                compiled_formats = [(r, _add_format(d), w) for (r, d, w) in formats]

                for sheet_name, df, _ in sheets:
                    ws = writer.sheets[sheet_name]
                    for i in range(df.columns.size):
                        cname: str = df.columns[i]
                        for rgxp, fmt, width in compiled_formats:
                            if re.search(rgxp, cname, re.I):
                                ws.set_column(first_col=i, last_col=i, width=width, cell_format=fmt)
                                break

            # Now is the time to write and format header.
            for sheet_name, df, _ in sheets:
                ws = writer.sheets[sheet_name]
                ws.set_row(row=0, height=48.0, cell_format=fmt_header)
                for i in range(df.columns.size):
                    ws.write_string(row=0, col=i, string=str(df.columns[i]), cell_format=fmt_header)

            # used to cause close() warning due to xlsxwriter stupid logic
            # writer.save()
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

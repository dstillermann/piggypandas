import pandas as pd
import numpy as np
from pandas.io.formats.style import Styler
import xlsxwriter as xls
from pathlib import Path
from typing import Union, List, Mapping, Optional, Tuple, Dict, Any, Iterable, Set
import re
import logging
import copy
import datetime

_logger = logging.getLogger('piggypandas')


DataFrameOrStyler = Union[pd.DataFrame, Styler]
SheetDataFrame = Tuple[str, DataFrameOrStyler, Dict[str, Any]]
SheetDataFrameList = List[SheetDataFrame]
CellFormat = Mapping[str, Any]
SheetFormat = Tuple[str, CellFormat, float]
SheetFormatList = List[SheetFormat]


def excelize_date_columns(data: pd.DataFrame,
                          columns: Optional[Iterable[str]] = None,
                          column_patterns: Optional[Iterable[str]] = None,
                          all_date_columns: bool = False,
                          epoch_1904: bool = False
                          ) -> pd.DataFrame:
    columns_to_convert: Set[str] = set()
    if all_date_columns:
        for c in data.columns:
            dt = data[c].dtype
            if dt == 'datetime64[ns]' or isinstance(dt, np.dtypes.DateTime64DType):
                columns_to_convert.add(str(c))
    if columns is not None:
        columns_to_convert.update(columns)
    if column_patterns is not None:
        for pattern in column_patterns:
            columns_to_convert.update([str(c) for c in data.columns if re.search(pattern, str(c), re.I)])

    epoch = pd.to_datetime(datetime.date(1903 if epoch_1904 else 1899, 12, 30))
    for c in columns_to_convert:
        data[c] = (pd.to_datetime(data[c]) - epoch).dt.days.astype('float64')

    return data


def write_dataframes(path: Union[str, Path],
                     sheets: SheetDataFrameList,
                     formats: Optional[SheetFormatList] = None,
                     common_format: Optional[CellFormat] = None,
                     header_format: Optional[CellFormat] = None,
                     header_height: Optional[float] = None
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
            for sheet_name, data, kwargs in sheets:
                is_styler = isinstance(data, Styler)
                new_kwargs = copy.copy(kwargs)
                if not is_styler:
                    new_kwargs['startrow'] = 1
                    new_kwargs['header'] = False
                data.to_excel(writer, sheet_name=sheet_name, **new_kwargs)

            # Applying the user formats.
            if formats is not None:
                compiled_formats = [(r, _add_format(d), w) for (r, d, w) in formats]

                for sheet_name, data, _ in sheets:
                    is_styler = isinstance(data, Styler)
                    df = data.data if is_styler else data
                    ws = writer.sheets[sheet_name]
                    for i in range(df.columns.size):
                        cname: str = df.columns[i]
                        for rgxp, fmt, width in compiled_formats:
                            if re.search(rgxp, cname, re.I):
                                if is_styler:
                                    ws.set_column(first_col=i, last_col=i, width=width)
                                else:
                                    ws.set_column(first_col=i, last_col=i, width=width, cell_format=fmt)
                                break

            # Now is the time to write and format header.
            for sheet_name, data, _ in sheets:
                is_styler = isinstance(data, Styler)
                if not is_styler:
                    df = data
                    ws = writer.sheets[sheet_name]
                    if header_height is None:
                        ws.set_row(row=0, cell_format=fmt_header)
                    else:
                        ws.set_row(row=0, height=header_height, cell_format=fmt_header)
                    for i in range(df.columns.size):
                        ws.write_string(row=0, col=i, string=str(df.columns[i]), cell_format=fmt_header)

            # used to cause close() warning due to xlsxwriter stupid logic
            # writer.save()
    else:
        msg = f"Can't write {str(file_out)}, unsupported format"
        _logger.error(msg)
        raise NotImplementedError(msg)


def write_dataframe(path: Union[str, Path],
                    data: DataFrameOrStyler,
                    sheet_name: str,
                    formats: Optional[SheetFormatList],
                    common_format: Optional[CellFormat] = None,
                    header_format: Optional[CellFormat] = None,
                    header_height: Optional[float] = None,
                    **kwargs
                    ):
    write_dataframes(path=path,
                     sheets=[(sheet_name, data, kwargs)],
                     formats=formats, common_format=common_format,
                     header_format=header_format, header_height=header_height)

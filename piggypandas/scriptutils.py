import pandas as pd
from pathlib import Path
from typing import Union


class ScriptUtils:

    @staticmethod
    def read_dataframe(file_in: Path,
                       sheet_name: str,
                       ) -> pd.DataFrame:
        if not isinstance(file_in, Path):
            file_in = Path(str(file_in))

        d_in: pd.DataFrame
        if not file_in.is_file():
            raise FileNotFoundError(f"File {str(file_in)} doesn't exist")
        elif file_in.suffix in ['.csv']:
            d_in = pd.read_csv(str(file_in))
        elif file_in.suffix in ['.xls', '.xlsx']:
            d_in = pd.read_excel(str(file_in), sheet_name=sheet_name)
        else:
            raise NotImplementedError(f"Can't read {str(file_in)}, unknown format")

        d_in = d_in.rename(Mapper.cleanup, axis=1)
        missing_columns: list = []
        for c in ['STAFF NAME', 'STAFF TOP SKILL', 'COUNTRY', 'LOCATION', 'QUALIFICATION NAME',
                  'QUALIFICATION LEVEL NAME', \
                  'TIMESHEET TIME', 'SALARY OC PRO RATA']:
            if c not in d_in.columns:
                missing_columns.append(c)
        if len(missing_columns) > 0:
            sys.stderr.write(f"Missing input columns: {missing_columns}\n")
            sys.exit(1)

        d_in = d_in.rename({
            'STAFF TOP SKILL': 'STAFF TOPSKILL',
            'QUALIFICATION NAME': 'RAW QNAME',
            'QUALIFICATION LEVEL NAME': 'RAW QLEVEL'
        }, axis=1)

        for (c, v) in [('REGION', ''),
                       ('BASIC QNAME', ''),
                       ('BASIC QLEVEL', ''),
                       ('DETAILED QNAME', ''),
                       ('DETAILED QLEVEL', ''),
                       ('QUALIFICATION COUNT', 0),
                       ('TOPSKILL COUNT', 0),
                       ('INTERNAL RATE', 0.0),
                       ('EXCEPTIONS', ''),
                       ('RAW DATA', '')]:
            d_in[c] = pd.Series(data=[v] * d_in.index.size, index=d_in.index)

        for (c, t) in [('TIMESHEET TIME', 'float64'),
                       ('SALARY OC PRO RATA', 'float64'),
                       ('INTERNAL RATE', 'float64'),
                       ('QUALIFICATION COUNT', 'int64'),
                       ('TOPSKILL COUNT', 'int64')]:
            d_in[c] = d_in[c].astype(t)

        return d_in


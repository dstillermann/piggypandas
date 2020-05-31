import pandas as pd
from pathlib import Path
import sys


class Mapper2:

    _all = []

    @staticmethod
    def flush_all():
        for m in Mapper2._all:
            m.flush()

    @staticmethod
    def cleanup(s: str, ignore_case: bool = False) -> str:
        if ignore_case:
            return str(s).strip().upper()
        else:
            return str(s).strip()

    @staticmethod
    def _mapping_dir() -> Path:
        p: Path = Path("./mapping")
        if p.is_dir():
            return p.resolve()
        p = Path(sys.argv[0]).resolve().parent.joinpath("mapping")
        if p.is_dir():
            return p
        return Path(".").resolve()

    @staticmethod
    def _mapping_file(slug: str) -> Path:
        f: Path = Path(slug)
        if f.is_file():
            return f
        p: Path = Mapper2._mapping_dir()
        f = p.joinpath(slug)
        if f.is_file():
            return f
        for suffix in ['.xls', '.csv']:
            f: Path = p.joinpath(slug + suffix)
            if f.is_file():
                return f
        return p.joinpath(slug + '.xlsx')

    @staticmethod
    def _mapping_filename(slug: str) -> str:
        return str(Mapper2._mapping_file(slug))

    def __init__(self, slug: str, columns: list, sheet_name: str ='DATA', ignore_case: bool = False):
        Mapper2._all.append(self)
        self._ignore_case: bool = ignore_case
        self._columns: list = columns
        self._sheet_name: str = sheet_name
        self._path: Path = Mapper2._mapping_file(slug)
        self._load()
        self._is_changed: bool = False

    def _cleanup(self, s: str) -> str:
        return Mapper2.cleanup(s, self._ignore_case)

    def _load(self):
        self._df: pd.DataFrame = None
        if self._path.is_file():
            if self._path.suffix in ['.csv']:
                self._df = pd.read_csv(str(self._path), index_col=False)
            elif self._path.suffix in ['.xls', '.xlsx']:
                self._df = pd.read_excel(str(self._path), sheet_name=self._sheet_name, index_col=False)
            else:
                raise NotImplementedError(f"Can't read {str(self._path)}, unsupported format")

        if isinstance(self._df, pd.DataFrame):
            if isinstance(self._columns, list) and len(self._columns) > 0:
                df_columns: list = self._df.columns.values
                df_columns_cmp: dict = {self._cleanup(x): x for x in df_columns}
                self_columns_cmp: dict = {self._cleanup(x): x for x in self._columns}
                missing_columns: list = [x for x in self_columns_cmp.keys() if x not in df_columns_cmp.keys()]
                if len(missing_columns) > 0:
                    raise ValueError(f"Missing columns {','.join(missing_columns)} for Mapper {str(self._path)}")
                added_columns: list = [df_columns_cmp[x] for x in df_columns_cmp.keys() if x not in self_columns_cmp.keys()]
                self._columns.extend(added_columns)
            else:
                self._columns = self._df.columns.values
        else:
            if not isinstance(self._columns, list) or len(self._columns) < 1:
                raise ValueError(f"No columns provided for Mapper {str(self._path)}")
            self._df = pd.DataFrame(columns=self._columns)

        assert isinstance(self._df, pd.DataFrame)
        assert isinstance(self._columns, list)
        assert len(self._columns) > 0

        self._keycolumn: str = self._columns[0]
        ix: pd.Index = pd.Index(data=[self._cleanup(x) for x in self._df[self._keycolumn]])
        if not ix.is_unique:
            raise KeyError(f"Non-unique key column \"{self._keycolumn}\" in Mapper {str(self._path)}")
        self._df.set_index(keys=ix, inplace=True)

        self._columnmap = {self._cleanup(x): x for x in self._columns}
        if self._ignore_case:
            self._df.rename(columns={x: self._cleanup(x) for x in self._columns}, inplace=True)

        self._defaultgetcolumn = self._cleanup(self._columns[0] if len(self._columns) == 1 else self._columns[1])

    @property
    def is_changed(self) -> bool:
        return self._is_changed

    def flush(self):
        if self._is_changed:
            self._flush()
            self._is_changed = False

    def _flush(self):
        if not isinstance(self._df, pd.DataFrame):
            return
        if self._path.suffix in ['.csv']:
            self._df.to_csv(str(self._path), index=False)
        elif self._path.suffix in ['.xls', '.xlsx']:
            self._df.to_excel(str(self._path), sheet_name=self._sheet_name, index=False)
        else:
            raise NotImplementedError(f"Can't save {str(self._path)}, unsupported format")

    def get(self, key: str, col: str = None, defaultvalue: str = None):
        key = self._cleanup(key)
        col = self._defaultgetcolumn if col is None else self._cleanup(col)
        try:
            return str(self._df.loc[key, col])
        except KeyError as e:
            if defaultvalue is not None:
                self._df.loc[key, col] = defaultvalue
                self._is_changed = True
                return defaultvalue
            else:
                raise KeyError(f"[{key}, {col}] not found") from e


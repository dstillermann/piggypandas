import json
import re
import pandas as pd
from copy import copy
from pathlib import Path
import sys


class Mapper:
    _all = []

    @staticmethod
    def flush_all():
        for m in Mapper._all:
            m.flush()

    @staticmethod
    def cleanup(s: str) -> str:
        if not isinstance(s, str):
            s = str(s)
        s = re.sub(r'^\s+([^\s])', r'\1', s)
        s = re.sub(r'([^\s])\s+$', r'\1', s)
        s = re.sub(r'\s+', r' ', s)
        return s.upper()

    @staticmethod
    def mapping_dir() -> Path:
        p: Path = Path("./mapping")
        if p.is_dir():
            return p.resolve()
        p = Path(sys.argv[0]).resolve().parent.joinpath("mapping")
        if p.is_dir():
            return p
        return Path(".").resolve()

    @staticmethod
    def mapping_file(filename: str) -> Path:
        p: Path = Mapper.mapping_dir()
        if p is not None:
            return p.joinpath(filename).resolve()
        else:
            return Path(filename)

    @staticmethod
    def mapping_filename(filename: str) -> str:
        return str(Mapper.mapping_file(filename))

    def __init__(self):
        Mapper._all.append(self)
        self._dict = {}
        self._load()
        self._is_changed = False

    @property
    def is_changed(self):
        return self._is_changed

    def flush(self):
        if self._is_changed:
            self._flush()
            self._is_changed = False

    def _load(self):
        raise NotImplementedError

    def _flush(self):
        raise NotImplementedError

    def get(self, key: str, defaultvalue=None):
        key = Mapper.cleanup(key)
        if len(key) < 1:
            return defaultvalue
        elif key in self._dict:
            return self._dict[key]
        elif defaultvalue is not None:
            self._dict[key] = defaultvalue
            self._is_changed = True
            return defaultvalue
        else:
            return defaultvalue

    def touch(self, key: str, defaultvalue=None):
        key = Mapper.cleanup(key)
        if len(key) > 0:
            if (key not in self._dict) and (defaultvalue is not None):
                self._dict[key] = defaultvalue
                self._is_changed = True

    def set(self, key: str, value):
        key = Mapper.cleanup(key)
        if len(key) > 0 and value is not None:
            self._dict[key] = value
            self._is_changed = True

    def has(self, key: str, defaultvalue=None):
        key = Mapper.cleanup(key)
        if len(key) < 1:
            return False
        elif key in self._dict:
            return True
        elif defaultvalue is not None:
            self._dict[key] = defaultvalue
            self._is_changed = True
            return True
        else:
            return False


class JSONMapper(Mapper):

    def __init__(self, slug: str):
        self._slug = str(slug)
        self._filename = Mapper.mapping_filename(self._slug + '.json')
        super().__init__()

    def _load(self):
        try:
            with open(self._filename, 'r') as f:
                self._dict = json.load(f)
                f.close()
        except:
            self._dict = {}

    def _flush(self):
        try:
            with open(self._filename, 'w') as f:
                json.dump(self._dict, f, skipkeys=True, allow_nan=False, indent=1)
                f.close()
        except:
            pass


class DataFrameMapper(Mapper):

    def __init__(self):
        super().__init__()
        self._columns = None

    def _load(self):
        self._columns = None
        try:
            df: pd.DataFrame = self._load_dataframe()
            self._columns: pd.Index = copy(df.columns)
            cols = self._columns.array
            for ix in df.index:
                s: pd.Series = df.loc[ix]
                k = s.iat[0]
                kstr: str = str(k)
                if len(kstr) > 0:
                    if len(cols) <= 1:
                        self._dict[kstr] = ''
                    elif len(cols) == 2:
                        self._dict[kstr] = s.iat[1]
                    else:
                        d = {}
                        for ic in range(1, len(cols)):
                            cstr: str = str(cols[ic])
                            if len(cstr) > 0:
                                d[cstr] = s.iat[ic]
                        self._dict[kstr] = d
        except:
            self._dict = {}
            self._columns = None
        assert self._dict is not None

    def _flush(self):
        out = {}
        if self._columns is None:
            ix = 0
            for key, val in self._dict.items():
                out[ix] = [key, val]
                ix += 1
        else:
            cols = self._columns.array
            ix = 0
            for key, val in self._dict.items():
                if len(cols) <= 1:
                    out[ix] = [key]
                elif len(cols) == 2:
                    out[ix] = [key, val]
                else:
                    row = [key]
                    for ic in range(1, len(cols)):
                        cstr: str = str(cols[ic])
                        row.append(val[cstr])
                    out[ix] = row
                ix += 1
        try:
            self._flush_dataframe(pd.DataFrame.from_dict(data=out, orient='index', columns=self._columns))
        except:
            pass

    def _load_dataframe(self):
        raise NotImplementedError

    def _flush_dataframe(self, df: pd.DataFrame):
        raise NotImplementedError


class CSVMapper(DataFrameMapper):
    def __init__(self, slug: str):
        self._slug: str = str(slug)
        self._filename: str = Mapper.mapping_filename(self._slug + '.csv')
        super().__init__()

    def _load_dataframe(self):
        return pd.read_csv(self._filename)

    def _flush_dataframe(self, df: pd.DataFrame):
        df.to_csv(self._filename, index=False)


class ExcelMapper(DataFrameMapper):
    def __init__(self, slug: str):
        self._slug: str = str(slug)
        self._filename: str = Mapper.mapping_filename(self._slug + '.xlsx')
        super().__init__()

    def _load_dataframe(self):
        return pd.read_excel(io=self._filename, sheet_name="DATA")

    def _flush_dataframe(self, df: pd.DataFrame):
        df.to_excel(excel_writer=self._filename, sheet_name="DATA", index=False)

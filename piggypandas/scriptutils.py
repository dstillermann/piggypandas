from pathlib import Path
from typing import Union


def overwrite_protected_path(f: Union[str, Path]) -> Path:
    if not isinstance(f, Path):
        f = Path(str(f))
    if f.is_dir():
        return f
    n: int = 0
    f_result = f
    while f_result.is_file():
        n += 1
        f_result = f.with_name(f.stem + f" ({n})" + f.suffix)
    return f_result


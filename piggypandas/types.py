from typing import Union, Mapping, Callable, List, Tuple

StringMapper = Union[Mapping[str, str], Callable[[str], str]]
ColumnList = List[str]
ColumnREMapper = List[Tuple[str, str]]

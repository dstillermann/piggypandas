from typing import Union, Mapping, Callable, List, Tuple


StringDict = Mapping[str, str]
StringMapper = Union[StringDict, Callable[[str], str]]
ColumnList = List[str]
ColumnREMapper = List[Tuple[str, str]]

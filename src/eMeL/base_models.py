from typing import Dict, List, Optional, Tuple, Union

from pydantic import BaseModel

Range = Tuple[Union[int, None], Union[int, None]]
ColumnNames = Union[List[str], Tuple[str, ...]]
ColumnIndexes = Union[List[int], Tuple[int, ...]]


class DataframeSpec(BaseModel):
    id: str
    columns: Union[ColumnNames, ColumnIndexes, None]
    rows: Range


class ApiResponse(BaseModel):
    success: bool
    data: Union[Dict, List]
    err: Optional[str]
    msg: Optional[str]

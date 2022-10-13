from typing import Dict, List, Optional, Tuple, Union

from pydantic import BaseModel

Range = Tuple[Union[int, None], Union[int, None]]
ColumnNames = Union[List[str], Tuple[str, ...]]
ColumnIndexes = Union[List[int], Tuple[int, ...]]


class Transform(BaseModel):
    name: Union[str, None] = None
    type: Union[str, None] = None
    order: int = 0


class ColumnTransform(BaseModel):
    column_index: int
    transforms: List[Transform]


class TransformSpec(BaseModel):
    id: str
    columns_transforms: List[ColumnTransform]
    dataframe_transforms: List[Transform]


class ApiResponse(BaseModel):
    success: bool
    data: Union[Dict, List]
    err: Optional[str]
    msg: Optional[str]

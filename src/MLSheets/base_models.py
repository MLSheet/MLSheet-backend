from datetime import datetime
from typing import Any, List, Optional, Tuple, Union

import pandas as pd  # type: ignore
from pydantic import BaseModel, validator

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


class StoredDataFrame(BaseModel):
    id: str
    name: str
    timestamp: str
    df: pd.DataFrame

    @validator('timestamp')
    def timestamp_must_be_iso_formatted(cls, val):  # type: ignore
        datetime.strptime(val, '%Y-%m-%dT%H:%M:%SZ')
        return val

    class Config:
        arbitrary_types_allowed = True


class ApiResponse(BaseModel):
    success: bool
    data: Any
    err: Optional[str]
    msg: Optional[str]

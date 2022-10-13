from typing import Dict, Union

import pandas as pd  # type: ignore

from MLSheets.base_models import ColumnIndexes, ColumnNames

dataframes: Dict[str, pd.DataFrame] = {}


async def all_columns_exist(required_columns: Union[ColumnNames, ColumnIndexes], available_columns: ColumnNames) -> bool:
    if all(map(lambda column: isinstance(column, str), required_columns)):
        return all([required_column in available_columns for required_column in required_columns])
    else:
        return int(max(required_columns)) < len(available_columns)


async def get_dataframe_from_id(df_id: str) -> pd.DataFrame:
    global dataframes
    return dataframes[df_id]


async def get_dataframes() -> Dict[str, pd.DataFrame]:
    global dataframes
    return dataframes


async def store_dataframe(df: pd.DataFrame, df_id: str) -> None:
    global dataframes
    dataframes[df_id] = df


def preformat_dataframe(df: pd.DataFrame) -> Dict:
    dictionary = df.to_dict(orient='split')
    dictionary['data'] = [[{'value': cell} for cell in row] for row in dictionary['data']]
    return dictionary

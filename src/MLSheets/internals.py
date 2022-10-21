from typing import Dict, List, Union

import pandas as pd  # type: ignore

from MLSheets.base_models import ColumnIndexes, ColumnNames, StoredDataFrame

dataframes: Dict[str, pd.DataFrame] = {}


async def all_columns_exist(required_columns: Union[ColumnNames, ColumnIndexes], available_columns: ColumnNames) -> bool:
    if all(map(lambda column: isinstance(column, str), required_columns)):
        return all([required_column in available_columns for required_column in required_columns])
    else:
        return int(max(required_columns)) < len(available_columns)


async def get_dataframe_from_id(df_id: str) -> pd.DataFrame:
    global dataframes
    return dataframes[df_id].df


async def get_dataframes() -> List[Dict[str, str]]:
    global dataframes
    return [{'id': stored_df.id, 'name': stored_df.name, 'timestamp': stored_df.timestamp} for stored_df in dataframes.values()]


async def store_dataframe(df: pd.DataFrame, df_id: str, df_name: str, timestamp: str) -> None:
    global dataframes
    dataframes[df_id] = StoredDataFrame(id=df_id, name=df_name, df=df, timestamp=timestamp)


def preformat_dataframe(df: pd.DataFrame) -> Dict:
    dictionary = df.to_dict(orient='split')
    dictionary['data'] = [[{'value': cell} for cell in row] for row in dictionary['data']]
    return dict(dictionary)

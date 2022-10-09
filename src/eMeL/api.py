from typing import List, Tuple, Union, cast
from uuid import uuid4

import pandas as pd  # type: ignore
from cytoolz.dicttoolz import assoc  # type: ignore
from fastapi import FastAPI, Response, UploadFile, status
from fastapi.responses import HTMLResponse

from eMeL.base_models import ApiResponse, ColumnIndexes, ColumnNames, DataframeSpec

app = FastAPI()

dataframes: dict = {}


async def all_columns_exist(required_columns: Union[ColumnNames, ColumnIndexes], available_columns: ColumnNames) -> bool:
    if all(map(lambda column: isinstance(column, str), required_columns)):
        return all([required_column in available_columns for required_column in required_columns])
    else:
        return int(max(required_columns)) < len(available_columns)


async def get_dataframe_from_spec(df_spec: DataframeSpec) -> Tuple[Union[pd.DataFrame, ApiResponse], bool]:
    global dataframes
    try:
        df = dataframes[df_spec.id]
    except KeyError:
        return ApiResponse(success=False, data=None, err='DF_NOT_FOUND', msg=f'Dataframe with ID {df_spec.id} not found'), False
    if df_spec.columns and not all_columns_exist(df_spec.columns, df.columns):
        return (
            ApiResponse(
                success=False,
                data=None,
                err='COLUMNS_NONEXISTENT',
                msg=f'Columns {df_spec.columns} not found for Dataframe with ID {df_spec.id}',
            ),
            False,
        )
    return df, True


async def store_df(df: pd.DataFrame, df_id: str) -> Tuple[Union[None, str], bool]:
    global dataframes
    try:
        dataframes = assoc(dataframes, df_id, df)
        return None, True
    except Exception as ex:
        return str(ex), False


@app.get('/')
async def upload_form() -> HTMLResponse:
    with open(file='./src/eMeL/form.html') as fh:
        return HTMLResponse(content=fh.read(), status_code=status.HTTP_200_OK)


@app.post('/upload-csv/')
async def api_upload_csv(file: UploadFile, response: Response) -> ApiResponse:
    try:
        df = pd.read_csv(file.file)
    except Exception as ex:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return ApiResponse(success=False, data=None, err='PARSING_FAILED', msg=str(ex))
    df_id = str(uuid4())
    await store_df(df, df_id)
    return ApiResponse(success=True, data={'id': df_id}, err=None, msg=None)


@app.post('/upload-excel/')
async def api_upload_excel(file: UploadFile, response: Response, sheets: Union[List[int], List[str], None] = None) -> ApiResponse:
    try:
        df = pd.read_excel(file.file, sheet_name=sheets)
    except Exception as ex:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return ApiResponse(success=False, data=None, err='PARSING_FAILED', msg=str(ex))
    df_id = str(uuid4())
    await store_df(df, df_id)
    return ApiResponse(success=True, data={'id': df_id}, err=None, msg=None)


@app.get('/dataframe/')
async def api_get_dataframe(df_spec: DataframeSpec, response: Response) -> ApiResponse:
    res, success = await get_dataframe_from_spec(df_spec=df_spec)
    if not success:
        response.status_code = status.HTTP_404_NOT_FOUND
        return res
    return ApiResponse(success=True, data=cast(pd.DataFrame, res).to_dict(), err=None, msg=None)


@app.get('/columns/')
async def api_get_columns_for_dataframe(df_spec: DataframeSpec, response: Response) -> ApiResponse:
    res, success = await get_dataframe_from_spec(df_spec=df_spec)
    if not success:
        response.status_code = status.HTTP_404_NOT_FOUND
        return res

    if df_spec.columns:
        columns = df_spec.columns
    else:
        columns = cast(pd.DataFrame, res).columns
    return ApiResponse(success=True, data=columns, err=None, msg=None)

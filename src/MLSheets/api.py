from typing import List, Union
from uuid import uuid4

import pandas as pd  # type: ignore
from fastapi import FastAPI, Form, Response, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware

from MLSheets.base_models import ApiResponse, TransformSpec
from MLSheets.internals import (
    get_dataframe_from_id,
    get_dataframes,
    preformat_dataframe,
    store_dataframe,
)

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=['*'])


@app.post('/upload-csv/')
async def api_upload_csv(file: UploadFile, response: Response, timestamp: str = Form(), df_name: str = Form()) -> ApiResponse:
    """Endpoint to upload a .csv file to

    Args:
        file (UploadFile): Some form/multipart formatted file
        response (Response): Response. Used to set response code.
        timestamp (str, optional): A timestamp received from the frontend. Defaults to Form().
        df_name (str, optional): A name for the DataFrame. Defaults to Form().

    Returns:
        ApiResponse: An object that represents the response sent from the API.
    """
    try:
        df = pd.read_csv(file.file)
    except Exception as ex:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return ApiResponse(success=False, data=None, err='PARSING_FAILED', msg=str(ex))
    df_id = str(uuid4())
    try:
        await store_dataframe(df, df_id, df_name, timestamp)
    except Exception as ex:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return ApiResponse(success=False, data=None, err='DATAFRAME_STORING_FAILED', msg=str(ex))
    return ApiResponse(success=True, data={'id': df_id}, err=None, msg=None)


@app.post('/upload-excel/')
async def api_upload_excel(
    file: UploadFile,
    response: Response,
    df_name: str = Form(),
    timestamp: str = Form(),
    sheets: Union[List[int], List[str], None] = None,
) -> ApiResponse:
    """Endpoint to upload an excel file to

    Args:
        file (UploadFile): Some form/multipart formatted file
        response (Response): Response. Used to set response code.
        timestamp (str, optional): A timestamp received from the frontend. Defaults to Form().
        df_name (str, optional): A name for the DataFrame. Defaults to Form().
        sheets (Union[List[int], List[str], None], optional): A list of sheet names or indexes. Defaults to None.

    Returns:
        ApiResponse: An object that represents the response sent from the API.
    """
    try:
        df = pd.read_excel(file.file, sheet_name=sheets)
    except Exception as ex:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return ApiResponse(success=False, data=None, err='DATA_PARSING_FAILED', msg=str(ex))
    df_id = str(uuid4())
    try:
        await store_dataframe(df, df_id, df_name, timestamp)
    except Exception as ex:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return ApiResponse(success=False, data=None, err='DATAFRAME_STORING_FAILED', msg=str(ex))
    return ApiResponse(success=True, data={'id': df_id}, err=None, msg=None)


@app.get('/dataframes')
async def api_get_dataframes() -> ApiResponse:
    """Endpoint to fetch the dataframes from.

    Returns:
        ApiResponse: An object that represents the response sent from the API.
    """
    print(await get_dataframes())
    return ApiResponse(success=True, data=await get_dataframes(), err=None, msg=None)


@app.get('/dataframes/{df_id}')
async def api_get_dataframe(df_id: str, response: Response) -> ApiResponse:
    """Endpoint to fetch a specific DataFrame

    Args:
        df_id (str): ID of the DataFrame to fetch
        response (Response): Response. Used to set response code.

    Returns:
        ApiResponse: An object that represents the response sent from the API.
    """
    try:
        df = await get_dataframe_from_id(df_id=df_id)
    except KeyError:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ApiResponse(success=False, data=None, err='DF_NOT_FOUND', msg=f'Dataframe with ID {df_id} not found')
    return ApiResponse(success=True, data=preformat_dataframe(df), err=None, msg=None)


@app.get('/dataframes/{df_id}/columns')
async def api_get_columns_for_dataframe(df_id: str, response: Response) -> ApiResponse:
    """Endpoint to fetch columns of a DataFrame

    Args:
        df_id (str): ID of the DataFrame to fetch
        response (Response): Response. Used to set response code.

    Returns:
        ApiResponse: An object that represents the response sent from the API.
    """
    try:
        df = await get_dataframe_from_id(df_id=df_id)
    except KeyError:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ApiResponse(success=False, data=None, err='DF_NOT_FOUND', msg=f'Dataframe with ID {df_id} not found')
    return ApiResponse(success=True, data=df.columns, err=None, msg=None)


@app.get('/dataframes/{df_id}/columns/{column_index}')
async def api_get_column(df_id: str, column_index: int, response: Response) -> ApiResponse:
    """Endpoint to fetch the contents of a specific column

    Args:
        df_id (str): ID of the DataFrame to fetch
        column_index (int): An index of the column to fetch
        response (Response): Response. Used to set response code.

    Returns:
        ApiResponse: An object that represents the response sent from the API.
    """
    try:
        df = await get_dataframe_from_id(df_id=df_id)
    except KeyError:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ApiResponse(success=False, data=None, err='DF_NOT_FOUND', msg=f'Dataframe with ID {df_id} not found')
    return ApiResponse(success=True, data=preformat_dataframe(df.iloc[:, column_index]), err=None, msg=None)


@app.post('/transform')
async def transform_dataframe(transform_spec: TransformSpec) -> ApiResponse:
    pass

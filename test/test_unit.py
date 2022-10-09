from eMeL.api import all_columns_exist, get_dataframe_from_spec, store_df, app, dataframes
from ward import test
from fastapi.testclient import TestClient
from expycted import expect


test_client = TestClient(app=app)

@test(f'All the string column names exist in target')
async def _():
    expect(await all_columns_exist(['a', 'b'], ['a', 'b', 'c'])).to.be_true()

@test(f'Not all the string column names exist in target')
async def _():
    expect(await all_columns_exist(['a', 'b'], ['a', 'c'])).to.be_false()

@test(f'All column indexes exist in target')
async def _():
    expect(await all_columns_exist([1,2], ['a', 'c', 'd'])).to.be_true()

@test(f'Not all column indexes exist in target')
async def _():
    expect(await all_columns_exist([1,2], ['a', 'c'])).to.be_false()

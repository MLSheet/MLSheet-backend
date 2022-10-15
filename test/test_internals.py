import mock
from pandas import DataFrame
from MLSheets.base_models import StoredDataFrame
from MLSheets.internals import all_columns_exist, get_dataframe_from_id, get_dataframes, store_dataframe, dataframes
from MLSheets.api import app
from ward import raises, test
from fastapi.testclient import TestClient
from expycted import expect

from cytoolz.dicttoolz import assoc


test_client = TestClient(app=app)

@test('Getting columns string names that exist in target')
async def _():
    expect(await all_columns_exist(['a', 'b'], ['a', 'b', 'c'])).to.be_true()

@test('Getting columns string names that do not exist in target')
async def _():
    expect(await all_columns_exist(['a', 'b'], ['a', 'c'])).to.be_false()

@test('Getting columns indexes that exist in target')
async def _():
    expect(await all_columns_exist([1,2], ['a', 'c', 'd'])).to.be_true()

@test('Getting columns indexes that do not exist in target')
async def _():
    expect(await all_columns_exist([1,2], ['a', 'c'])).to.be_false()

@test('Getting DataFrame that exists')
async def _():
    test_dataframe = StoredDataFrame(id="1", name="test", df=DataFrame([0,1,2,3]))
    with mock.patch('MLSheets.internals.dataframes', {'1': test_dataframe}):
        expect((await get_dataframe_from_id('1')).to_dict()).to.be_equal_to({0: {0: 0, 1: 1, 2: 2, 3: 3}})

@test('Getting DataFrame that does not exist')
async def _():
    with mock.patch('MLSheets.internals.dataframes', {'1': 'DataFrame'}):
        with raises(KeyError):
            await get_dataframe_from_id('2')

@test('Getting all DataFrames')
async def _():
    test_dataframe = StoredDataFrame(id="1", name="test", df=DataFrame())
    with mock.patch('MLSheets.internals.dataframes', {'1': test_dataframe}):
        expect(await get_dataframes()).to.be_equal_to([{'id': '1', 'name': 'test'}])

@test('Storing a DataFrame')
async def _():
    with mock.patch('MLSheets.internals.dataframes', {'1': 'DataFrame'}) as mock_dataframes:
        test_df = DataFrame()
        await store_dataframe(test_df, '2', 'Jozo')
        expect(mock_dataframes.keys()).to.contain(('2'))
        expect(list(mock_dataframes.values())[1]).to.be_of_type(StoredDataFrame)

@test('Failing to store a DataFrame')
async def _():
    with mock.patch('MLSheets.internals.dataframes', 1), raises(Exception):
        test_df = DataFrame()
        await store_dataframe(test_df, '2')

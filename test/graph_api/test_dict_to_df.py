from unittest import TestCase

from pandas import DataFrame

from src.graph_api.array_to_df import ArrayToDF


class TestDictToDF(TestCase):
    def setUp(self) -> None:
        self.testee = ArrayToDF

    def test_one(self):
        map = {'swaps': [{'amount0In': '0',
                          'amount0Out': '779.12696',
                          'amount1In': '0.5086133805565',
                          'amount1Out': '0',
                          'amountUSD': '836.1815423843687017892883570803941',
                          'id': '0xa8acbd079294d5dee1169e4bb81e6383c50eeed3fa2b1440616f713b18533378-0',
                          'pair': {'token0': {'symbol': 'POOL'},
                                   'token1': {'symbol': 'WETH'}},
                          'sender': '0x007933790a4f00000099e9001629d9fe7775b800',
                          'timestamp': '1674537623',
                          'to': '0x007933790a4f00000099e9001629d9fe7775b800',
                          'transaction': {'blockNumber': '16474541'}},
                         {'amount0In': '779.12695',
                          'amount0Out': '0',
                          'amount1In': '0',
                          'amount1Out': '0.5139397656159',
                          'amountUSD': '838.8954596982876314459081711998917',
                          'id': '0x9cdc0f7496db18c44dbb714d8f33a36d9bff82d9d49ff100ef324cc04b55fc9c-0',
                          'pair': {'token0': {'symbol': 'POOL'},
                                   'token1': {'symbol': 'WETH'}},
                          'sender': '0x007933790a4f00000099e9001629d9fe7775b800',
                          'timestamp': '1674537623',
                          'to': '0x007933790a4f00000099e9001629d9fe7775b800',
                          'transaction': {'blockNumber': '16474541'}}]}
        result = self.testee.convert_to_df(map['swaps'])

        print(result.to_markdown())

        self.assertTrue(isinstance(result, DataFrame))
        self.assertEqual(result.columns.values.tolist(),
                         ['amount0In',
                          'amount0Out',
                          'amount1In',
                          'amount1Out',
                          'amountUSD',
                          'id',
                          'sender',
                          'timestamp',
                          'to',
                          'pair.token0.symbol',
                          'pair.token1.symbol',
                          'transaction.blockNumber'])

import pprint
from unittest import TestCase

from src.graph_api.graph_query_template import Queries
from src.graph_api.uni_v2_graph_fetcher import UniV2GraphFetcher


class TestFetcher(TestCase):
    def setUp(self) -> None:
        self.fetcher = UniV2GraphFetcher()

    def test_get_swap(self):
        block = 0
        swap_count = 2
        result = self.fetcher.fetch(
            Queries.get_swaps_query_for_pair("0x85cb0bab616fe88a89a35080516a8928f38b518b", block, swap_count))
        pprint.pprint(result)
        self.assertEqual(len(result['swaps']), swap_count)
        self.assertEqual(set(result['swaps'][0]),
                         {'amount0In', 'amount0Out', 'amount1In', 'amount1Out', 'amountUSD', 'id', 'pair', 'sender',
                          'timestamp', 'to', 'transaction'})

    def test_get_mint(self):
        mint_count = 2
        result = self.fetcher.fetch(
            Queries.get_mint_query_for_pair("0x85cb0bab616fe88a89a35080516a8928f38b518b", mint_count))
        pprint.pprint(result)
        self.assertEqual(len(result['mints']), mint_count)

    def test_get_pair(self):
        result = self.fetcher.fetch(Queries.get_pair("0x85cb0bab616fe88a89a35080516a8928f38b518b"))
        pprint.pprint(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(set(result["pair"].keys()), {"reserve0", "reserve1", "createdAtBlockNumber"})

    def test_get_pair_by_block(self):

        result = self.fetcher.fetch(Queries.get_pair("0x85cb0bab616fe88a89a35080516a8928f38b518b",
                                                     11876500))
        pprint.pprint(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(set(result["pair"].keys()), {"reserve0", "reserve1", "createdAtBlockNumber"})

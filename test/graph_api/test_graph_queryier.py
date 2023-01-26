from decimal import getcontext
from unittest import TestCase

from pandas import DataFrame

from src.graph_api.graph_to_df import GraphToDF

getcontext().prec = 18


class TestGraphQuerier(TestCase):

    def test_store_to_pd(self):

        start = 16475000
        pair = "0x85cb0bab616fe88a89a35080516a8928f38b518b"
        graph_to_df = GraphToDF(pair)
        graph_to_df.run(starting_block=start)
        df = graph_to_df.get_df()
        self.assertTrue(isinstance(graph_to_df.get_df(), DataFrame))


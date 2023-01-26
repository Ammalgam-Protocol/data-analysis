import pprint
from decimal import Decimal
from logging import error

from gql.transport.exceptions import TransportQueryError
from pandas import DataFrame

from src.graph_api.array_to_df import ArrayToDF
from src.graph_api.graph_query_template import Queries
from src.graph_api.uni_v2_graph_fetcher import UniV2GraphFetcher


class GraphToDF:
    def __init__(self, pair):
        self.pair = pair
        self.df: DataFrame = None
        self.fetcher = UniV2GraphFetcher()

    def run(self, starting_block=0):
        result = self.fetcher.fetch(Queries.get_pair(self.pair, starting_block))
        pair = result["pair"]
        pprint.pprint("First Block:")
        pprint.pprint(pair)
        created_block = pair['createdAtBlockNumber']
        reserve0 = Decimal(pair["reserve0"])
        reserve1 = Decimal(pair["reserve1"])
        current_block = created_block if int(created_block) > starting_block else str(starting_block)
        swaps = []
        current_query = 0

        while True:
            skip = 1000 * current_query
            query = Queries.get_swaps_query_for_pair(self.pair, block=starting_block, skip=skip)

            try:
                result = self.fetcher.fetch(query)
            except TransportQueryError as e:
                error(f"Failed Query: {query}", e)
                result = []
            current_swaps = result['swaps']
            if len(current_swaps) == 0:
                break
            for s in current_swaps:
                if s["transaction"]["blockNumber"] != current_block:
                    current_block = s["transaction"]["blockNumber"]
                    result = self.fetcher.fetch(Queries.get_pair(self.pair, int(current_block) + 1))
                    pair = result["pair"]
                    if str(reserve0) != pair["reserve0"] or str(reserve1) != pair["reserve1"]:
                        error(f"Reserves don't match\n"
                              f"reserve0 is {reserve0}, should be {pair['reserve0']}"
                              f"reserve1 is {reserve1}, should be {pair['reserve1']}")
                        error(f"block: {current_block}")
                        reserve0 = Decimal(pair["reserve0"])
                        reserve1 = Decimal(pair["reserve1"])
                s["reserve0"] = reserve0
                s["reserve1"] = reserve1
                reserve0 += Decimal(s["amount0In"])
                reserve0 -= Decimal(s["amount0Out"])
                reserve1 += Decimal(s["amount1In"])
                reserve0 -= Decimal(s["amount1Out"])
                swaps.append(s)

            current_query += 1

        self.df = ArrayToDF.convert_to_df(swaps)

    def get_df(self):
        return self.df

    def store_df(self):
        self.df.to_pickle(f"./{self.pair}_df.pkl")
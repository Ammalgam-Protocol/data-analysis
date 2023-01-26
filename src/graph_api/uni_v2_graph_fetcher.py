from typing import Union, Dict, Any

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from graphql import ExecutionResult


class UniV2GraphFetcher:

    def __init__(self):
        transport = RequestsHTTPTransport(
            url="https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2",
            verify=True,
            retries=3,
        )

        self.client = Client(transport=transport)

    def fetch(self, query: str) -> Union[Dict[str, Any], ExecutionResult]:
        return self.client.execute(gql(query))



class Queries:
    @staticmethod
    def get_swaps_query_for_pair(pair, block=0, first=1000, skip=0, direction="asc"):
        transaction_filter = f"transaction_: {{ blockNumber_gt: {block} }}"
        if block == -1:
            transaction_filter = ''
        return f'''
            {{
              swaps(
                orderBy: timestamp, orderDirection: {direction},
                first: {first}
                skip: {skip}
                where: {{
                  pair: "{pair}"
                  {transaction_filter}
                }}
              ) {{
                id
                timestamp
                pair {{
                  token0 {{
                    symbol
                  }}
                  token1 {{
                    symbol
                  }}
                  reserve0 
                  reserve1 
                }}
                amount0In
                amount0Out
                amount1In
                amount1Out
                amountUSD
                sender 
                to
                transaction {{
                  id
                  blockNumber
                }}
            
              }}
            }}
        '''

    @staticmethod
    def get_last_swap(pair):
        return Queries.get_swaps_query_for_pair(pair, block=-1, first=1, direction="desc")


    @staticmethod
    def get_mint_query_for_pair(pair, mint_count):
        return f'''
        {{
            mints(first: {mint_count}, where: {{ pair: "{pair}" }}, orderBy: timestamp, orderDirection: desc) {{
                transaction {{
                    id
                    timestamp
                }}
                to
                liquidity
                amount0
                amount1
                amountUSD
            }}
        }}
        '''

    @staticmethod
    def get_pair(address, block=0):
        block_addition = ''
        if block is not None:
            block_addition = f", block: {{ number_gte: {block}}}"
        return f'''
            {{
                pair(id: "{address}" {block_addition}) {{
                  reserve0
                  reserve1
                  createdAtBlockNumber  
                }}
            }}
        '''

# Oracle Data Analysis

This code was used o better understand how different versions of oracles approximate a price of a
trading pair at a given time. For a first pass I looked at the Uniswap V2 ETH-POOL pair.

I looked at two methods of collecting data, pulling events from a [local node](src/local_node) and
using [The Graph](https://thegraph.com). Using a node to pull events was very slow, but it was able
to  complete prior to me wrapping up the code to pull indexed data from The Graph.

Much of main flow of code was hacked together in test files. More work is required to make this a 
finished production product.
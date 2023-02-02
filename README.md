# Oracle Data Analysis

This code was used o better understand how different versions of oracles approximate a price of a
trading pair at a given time. For a first pass I looked at the Uniswap V2 ETH-POOL pair.

I looked at two methods of collecting data, pulling events from a [local node](src/local_node) and
using [The Graph](https://thegraph.com). Using a node to pull events was very slow, but it was able
to  complete prior to me wrapping up the code to pull indexed data from The Graph.

Much of main flow of code was hacked together in test files. More work is required to make this a 
finished production product.

## Load Notebook

This repo uses [Poetry](https://python-poetry.org/) to manage dependencies within a python virtual
environment. You can install the dependencies and run [jupyter-lab](https://jupyter.org/) with the
comands.

```bash
poetry install
poetry run jupyter-lab
```

from jupyter-lab you can navigate to the [notebook](data-analysis.ipynb). 

## Constructing data for a new pair

Code to scrape data is not production quality, it was assembled quickly and a testing framework was
used to execute the process. Data can be recreated using the tests in 
[test_scanner_with_node.py](test/local_node/test_scanner_with_node.py). You will need to fill in
the node url, uniswap v2 pair address, and the block the pair was created (to save on time). 

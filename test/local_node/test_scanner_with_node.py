import logging
import sys
import unittest
from unittest import TestCase

from eth_typing import Address
from pandas import DataFrame
from web3 import Web3

from src.local_node.event_scanner import JSONifiedState
from src.local_node.process_state_to_df import ProcessStateToDF
from src.local_node.scanner_runner import ScannerRunner
from src.uniswap_v2_pair_abi import UNISWAP_V2_PAIR_ABI

this_log = logging.getLogger(__name__)
this_log.setLevel(logging.INFO)
this_log.addHandler(logging.StreamHandler(sys.stdout))


class TestScannerWithNode(TestCase, ScannerRunner):
    ETH_POOL_UNI_V2_CONTRACT_ADDRESS: Address = "0x85Cb0baB616Fe88a89A35080516a8928F38B518b"
    ABI = UNISWAP_V2_PAIR_ABI

    def testWeb3Sync(self):
        w3 = Web3(Web3.HTTPProvider("http://192.168.50.106:8545", request_kwargs={'timeout': 60}))
        self.assertTrue(w3.isConnected())

        contract = w3.eth.contract(address=self.ETH_POOL_UNI_V2_CONTRACT_ADDRESS, abi=self.ABI)

        print(contract)
        event_filter = contract.events.Sync.createFilter(fromBlock=16478475-1000, toBlock=16478475)
        # print(dir(event_filter))
        events = event_filter.get_all_entries()
        self.assertEqual(len(events), 2)
        self.assertEqual(set(events[0].keys()), {'address', 'args', 'blockHash', 'blockNumber', 'event', 'logIndex',
                                                 'transactionHash', 'transactionIndex'})
        self.assertEqual(events[0]["event"], 'Sync')
        self.assertEqual(set(events[0]["args"].keys()), {'reserve0', 'reserve1'})
        print(events[0]["args"])

        event_filter = contract.events.Swap.createFilter(fromBlock=16478475 - 1000, toBlock=16478475)
        swaps = event_filter.get_all_entries()
        print(len(swaps))
        print(swaps[0]["args"].keys())

    @unittest.skip("Using as a work space, runs in 12 hours for ETH-POOL pair")
    def test_scanner_runner(self):
        first_block = 11876000
        node_url = "http://192.168.50.106:8545"
        ScannerRunner.run_scanner(
            "test-state.json", first_block, node_url, self.ABI, self.ETH_POOL_UNI_V2_CONTRACT_ADDRESS)

    @unittest.skip("Using as a work space")
    def testReadJsonState(self):
        json_state = JSONifiedState("test-state.json")
        json_state.restore()
        state = json_state.state
        state_df = ProcessStateToDF.process_state(state["blocks"], self)

        self.assertTrue(isinstance(state_df, DataFrame))

        # store file as needed.
        state_df.to_csv("state/0x85Cb0baB616Fe88a89A35080516a8928F38B518b_df.csv")
        state_df.to_pickle("state/0x85Cb0baB616Fe88a89A35080516a8928F38B518b_df.pkl")

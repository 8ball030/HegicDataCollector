#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: 8baller
Authorised use only
"""
import pandas as pd
from web3 import Web3
import json

columns = [
    "option_state",
    "option_owner",
    "strike",
    "amount",
    "strikeAmount.mul(optionCollateralizationRatio).div(100).add(strikeFee)",
    "premium",
    "expiration_date",
    "optionType",
]


def collect_options(contract, market):
    results = []
    ix = 0
    while True:
        print(f"Collecting option {ix} {market}")
        try:
            results += [contract.functions.options(ix).call()]
            ix += 1
        except:
            print("Contract exhausted!")
            break
    results = pd.DataFrame(results, columns=columns)
    results['market'] = market
    return results


if __name__ == "__main__":

    w3 = Web3(
        Web3.HTTPProvider(
            "https://mainnet.infura.io/v3/f00f7b3ba0e848ddbdc8941c527447fe"))
    w3.isConnected()

    btc_address = "0x3961245DB602eD7c03eECcda33eA3846bD8723BD"
    eth_address = "0xEfC0eEAdC1132A12c9487d800112693bf49EcfA2"

    with open("./contracts_for_workbook//HegicWBTCOptions.json", "r") as f:
        c = json.loads(f.read())

    btc_option_contract = w3.eth.contract(address=btc_address, abi=c["abi"])

    with open("./contracts_for_workbook/HegicWBTCOptions.json", "r") as f:
        c = json.loads(f.read())

    eth_option_contract = w3.eth.contract(address=eth_address, abi=c["abi"])

    df = pd.concat([
        collect_options(eth_option_contract, "eth_options"),
        collect_options(btc_option_contract, "btc_options")
    ])
    df.to_csv("current_options.csv", index=False)
    print("Done!")

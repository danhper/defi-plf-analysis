import argparse
import csv
from os import path
import json
import logging

import pandas as pd
import requests

from compounds_research import settings


COLUMNS = [
    "id",
    "variableBorrowRate",
    "utilizationRate",
    "stableBorrowRate",
    "liquidityIndex",
    "liquidityRate",
    "totalLiquidity",
    "availableLiquidity",
    "totalBorrows",
    "totalBorrowsVariable",
    "totalBorrowsStable",
    "timestamp",
]
COLUMNS_STR = "\n".join(COLUMNS)

AAVE_RESERVES_PATH = path.join(settings.DATA_PATH, "aave/aave-reserves.csv")


logging.basicConfig(level=logging.INFO)


BATCH_SIZE = 1000
URL = "https://api.thegraph.com/subgraphs/name/aave/protocol"
RESERVE_HISTORY_QUERY = """{{
    reserve(id: "{id}") {{
        id
        symbol
        paramsHistory(first: {size} skip: {skip} orderBy: timestamp orderDirection: desc) {{
            {columns}
        }}
    }}
}}
"""

# depositHistory
# redeemUnderlyingHistory
HISTORY_QUERY = """{{
    reserve(id: "{id}") {{
        id
        symbol
        totalLiquidity
        {history_type}(first: {size} skip: {skip}) {{
            id
            user {{
                id
            }}
            amount
            timestamp
        }}
    }}
}}
"""



def fetch_reserve_history(market):
    symbol = market["symbol"]
    logging.info("fetching %s", symbol)
    with open(path.join(settings.DATA_PATH, "aave", f"{symbol}.csv"), "w") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        skip = 0
        while True:
            logging.info("done: %s", skip)
            query = RESERVE_HISTORY_QUERY.format(id=market["id"], columns=COLUMNS_STR, size=BATCH_SIZE, skip=skip)
            res = requests.post(URL, json=dict(query=query))
            items = res.json()["data"]["reserve"]["paramsHistory"]
            if not items:
                break
            for item in items:
                writer.writerow(item)
            skip += BATCH_SIZE


def fetch_market_deposits(market):
    symbol = market["symbol"]
    logging.info("fetching %s", symbol)
    total_liquidity = None

    result = dict(symbol=symbol, redeems=[], deposits=[])
    result_keys = {"deposits": "deposits",
                   "redeemUnderlyingHistory": "redeems"}

    for history_type, key in result_keys.items():
        skip = 0
        items = result[key]
        while True:
            query = HISTORY_QUERY.format(
                id=market["id"], size=BATCH_SIZE, skip=skip, history_type=history_type)
            res = requests.post(URL, json=dict(query=query))
            reserve = res.json()["data"]["reserve"]
            if total_liquidity is None:
                total_liquidity = reserve["totalLiquidity"]
            reserve_items = reserve[history_type]
            if not reserve_items:
                break
            for item in reserve_items:
                items.append(dict(item, user=item["user"]["id"]))
            skip += len(reserve_items)

    result["total_liquidity"] = total_liquidity

    with open(path.join(settings.DATA_PATH, "aave", f"{symbol}-deposits.json"), "w") as f:
        json.dump(result, f)


def fetch_reserves():
    query = """{
        reserves {
            id
            decimals
            symbol
        }
    }"""
    res = requests.post(URL, json=dict(query=query))
    df = pd.DataFrame(res.json()["data"]["reserves"])
    df.to_csv(AAVE_RESERVES_PATH, index=False, columns=["symbol", "id", "decimals"])


def get_reserves():
    with open(path.join(settings.DATA_PATH, "aave/aave-reserves.csv")) as f:
        return [d for d in csv.DictReader(f)]


def fetch_reserve_histories():
    for reserve in get_reserves():
        fetch_reserve_history(reserve)


def fetch_reserve_deposits():
    for reserve in get_reserves():
        fetch_market_deposits(reserve)


def main():
    parser = argparse.ArgumentParser(prog="fetch-aave")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("fetch-reserves")
    subparsers.add_parser("fetch-reserve-histories")
    subparsers.add_parser("fetch-reserve-deposits")
    args = parser.parse_args()

    if not args.command:
        parser.error("no command given")
    func = globals()[args.command.replace("-", "_")]
    func()


if __name__ == "__main__":
    main()

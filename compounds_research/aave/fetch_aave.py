import json
import logging

import requests


logging.basicConfig(level=logging.INFO)


BATCH_SIZE = 1000
URL = "https://api.thegraph.com/subgraphs/name/aave/protocol-raw"
GRAPHQL_QUERY = """{{
    reserveParamsHistoryItems(first: {size} skip: {skip} orderBy: timestamp orderDirection: desc) {{
        id
        reserve {{
            id
            symbol
        }}
        variableBorrowRate
        utilizationRate
        stableBorrowRate
        liquidityIndex
        liquidityRate
        totalLiquidity
        availableLiquidity
        totalBorrows
        totalBorrowsVariable
        totalBorrowsStable
        timestamp
    }}
}}
"""


with open("aave.jsonl", "w") as f:
    skip = 0
    while True:
        logging.info("done: %s", skip)
        res = requests.post(URL, json=dict(query=GRAPHQL_QUERY.format(size=BATCH_SIZE, skip=skip)))
        items = res.json()["data"]["reserveParamsHistoryItems"]
        if not items:
            break
        for line in items:
            print(json.dumps(line), file=f)
        skip += BATCH_SIZE

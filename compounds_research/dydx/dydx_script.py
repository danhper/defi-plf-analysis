import json
import csv
from web3.auto import w3
from web3.logs import STRICT, IGNORE, DISCARD, WARN
from eth_abi import decode_single, decode_abi


w3.HTTPProvider('http:satoshi.doc.ic.ac.uk:8545')
dydx_solo = '0x1E0447b19BB6EcFdAe1e4AE1694b0C3659614e4e'

with open('solo_abi.json') as json_file:
    solo_abi = json.load(json_file)

tokens = {
    'DAI': '0x6B175474E89094C44Da98b954EedeAC495271d0F',
    'WETH': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
    'SAI': '0x89d24A6b4CcB1B6fAA2625fE562bDD9a23260359',
    'USDC': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'
}

dydx_market_ids = {
    'DAI': 3,
    'WETH': 0,
    'SAI': 1,
    'USDC': 2
}


def getInterestRates(token, fromBlock=9000000, toBlock=w3.eth.blockNumber, file='market_dydx.csv'):
    assert fromBlock <= toBlock, 'Invalid block range specified.'
    dydx = w3.eth.contract(address=dydx_solo, abi=solo_abi['contracts']['contract.sol:Getters']['abi'])
    market_id = dydx_market_ids[token.upper()]
    token_address = tokens[token.upper()]
    height = fromBlock
    
    
    with open(token.lower()+'_'+file, 'w', newline='') as csvfile:
        fieldnames = ['block_height', 'token_address', 'interest_rate', 'borrow_amount', 'supply_amount', 'utilization']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    
        while height <= toBlock:
            market_info = dydx.functions.getMarketWithInfo(market_id).call(block_identifier=height)
            assert tokens[token] == market_info[0][0]
            interest_rate = market_info[3][0]
            borrow = market_info[0][1][0]
            supply = market_info[0][1][1]
            utilization = round(borrow/supply, 5) if supply != 0 else 0
            writer.writerow({
                'block_height': height, 
                'token_address': token_address, 
                'interest_rate': interest_rate,
                'borrow_amount': borrow,
                'supply_amount': supply,
                'utilization': utilization
            })
            #print(height, interest_rate, borrow, supply, utilization)
            height += 1

getInterestRates('USDC')

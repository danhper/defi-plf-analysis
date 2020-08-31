import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from os import path

from compounds_research import plotting
from compounds_research import settings
from compounds_research import utils


dydx_markets = ['dai', 'weth', 'usdc']

def load_dydx_market(market: str):
    if market not in dydx_markets:
        if market.lower() == 'eth':
            market = 'weth'
        else:
            print('Invalid market for dydx: ', market)
            return
    MARKET_FILEPATH = path.join(settings.DATA_PATH, 'dydx', market+'_market_dydx.csv.gz')
    df = pd.read_csv(MARKET_FILEPATH)
    df_block_times = pd.read_csv(path.join(settings.DATA_PATH, 'dydx', 'eth_block_times.csv.gz'))
    df = df.join(df_block_times.set_index('block_height'), on='block_height')
    df['borrow_amount'] = df.borrow_amount.apply(lambda v: int(v) / 1e6)
    df['supply_amount'] = df.supply_amount.apply(lambda v: int(v) / 1e6)
    df['interest_rate'] = df.interest_rate.apply(lambda v: int(v) / 1e18 * 3600 * 24 * 365)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df = df.set_index('timestamp')
    return df

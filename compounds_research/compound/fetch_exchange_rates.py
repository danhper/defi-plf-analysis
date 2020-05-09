import requests
import pandas as pd

URL = 'https://min-api.cryptocompare.com/data/v2/histoday'

def get_exchange_rates(base_symbol: str, quote_symbol: str, limit: int):
    '''
    :from_symbol: crypto from symbol.
    :to_symbol: crypto to symbol.
    :limit: number of data points to retrieve at most. 
    '''
    params = {'fsym': base_symbol,
            'tsym': quote_symbol,
            'limit': limit}

    response = requests.get(url=URL, params=params)
    if response.status_code != 200:
        print('Error while retrieving exchange rate data.')
    df = pd.DataFrame(response.json()['Data']['Data'])
    df['date'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('date', inplace=True)
    return df

def make_exchange_rate_df(quote_symbol: str, limit: int):
    '''
    :quote_symbol: the currency to use as the quote currency (the to symbol)
    :limit: number of data points to return, at most. 
    '''
    token_list = ['bat', 'dai', 'eth', 'rep', 'sai', 'usdc', 'wbtc', 'zrx']

    master_df = pd.DataFrame()
    for token in token_list:
        if quote_symbol == token:
            continue
        df = get_exchange_rates(token, quote_symbol, limit)
        close = df['close']
        close = close.rename(token)
        master_df = pd.concat([master_df, close], axis=1, join='outer')
    return master_df
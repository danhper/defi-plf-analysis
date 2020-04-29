import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib.ticker as ticker

import datetime as dt
import statsmodels.api as sm
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

token_addresses = {'cbat': '0x6c8c6b02e7b2be14d4fa6022dfd6d75921d90e4e',
                    'cdai': '0x5d3a536e4d6dbd6114cc1ead35777bab948e3643',
                    'ceth': '0x4ddc2d193948926d02f9b1fe9e1daa0718270ed5',
                    'crep': '0x158079ee67fce2f58472a96584a73c7ab9ac95c1',
                    'csai': '0xf5dce57282a584d2746faf1593d3121fcac444dc',
                    'cusdc': '0x39aa39c021dfbae8fac545936693ac917d5e7563',
                    'cwbtc': '0xc11b1268c1a384e55c48c2391d8d480264a3a7f4',
                    'czrx': '0xb3319f5d18bc0d84dd1b4825dcde5d5f7266d407'
                    }

variables = ['total_borrows_history', 'total_supply_history', 'utilization_ratio', 'spread', 'borrow_rates', 'supply_rates', 'exchange_rates']

url = 'https://api.compound.finance/api/v2/market_history/graph'

start_date = int(dt.datetime(2020, 1, 1).timestamp())
end_date = int(dt.datetime.now().timestamp())
num_buckets = 3000

def format_date(x, pos=None):
     return dates.num2date(x).strftime('%Y-%m-%d')

def make_dataframe(token: str):
    '''
    Build money-market dataframes. 
    '''
    params = {'asset': token_addresses[token],
            'min_block_timestamp': start_date,
            'max_block_timestamp': end_date,
            'num_buckets': num_buckets}

    response = requests.get(url = url, params=params)
    response = response.json()

    rate_variables = ['borrow_rates', 'exchange_rates', 'supply_rates']

    df = pd.DataFrame()

    for key in rate_variables:
        df_temp = pd.DataFrame(response[key])
        df_temp['date'] = pd.to_datetime(df_temp['block_timestamp'], unit='s')
        df_temp.set_index('date', inplace = True)
        df_temp = df_temp[['rate']]
        df_temp = df_temp.rename(columns={'rate': str(key)})
        df = pd.concat([df, df_temp], axis=1)

    stock_variables = ['total_borrows_history', 'total_supply_history']

    for key in stock_variables:
        df_temp = pd.DataFrame(response[key])
        df_temp['date'] = pd.to_datetime(df_temp['block_timestamp'], unit='s')
        df_temp.set_index('date', inplace = True)
        df_temp = df_temp[['total']]
        df_temp = pd.concat([df_temp.drop(['total'], axis=1), df_temp['total'].apply(pd.Series)], axis=1)
        df_temp = df_temp.rename(columns={'value': str(key)})
        df = pd.concat([df, df_temp], axis=1)

    df['total_borrows_history'] = pd.to_numeric(df['total_borrows_history'], downcast="float")
    df['total_supply_history'] = pd.to_numeric(df['total_supply_history'], downcast="float")

    df['utilization_ratio'] = df['total_borrows_history'] / df['total_supply_history']
    df['spread'] = df['borrow_rates']- df['supply_rates']

    return df

def plot_utilization_vs_rate(token: str):
    '''
    Scatter plot of utilization rate vs borrow or supply rate. 
    '''
    df = make_dataframe(token)
    fig, ax = plt.subplots()
    ax.scatter(df['supply_rates'], df['utilization_ratio'], label='Supply interest rate')
    ax.scatter(df['borrow_rates'], df['utilization_ratio'], label ='Borrow interest rate')
    ax.set_ylabel('Interest rate', fontsize = 18)
    ax.set_xlabel('Utilization ratio', fontsize = 18)    
    fig.suptitle(str(token).upper(), fontsize = 20)
    ax.tick_params(axis='both', which='major', labelsize=18)
    ax.legend()
    fig.savefig('../PhD/overleaf/5e6bad2e6490390001d3c466/images/' + str(token)+ '.pdf', bbox_inches='tight', dpi = 300)

def plot_relationship_evolution(token: str, elev, azim):
    '''
    Evolution of utilization ratio / interest rates through time. 
    '''
    df = make_dataframe(token)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    df['date'] = dates.date2num(df.index)
    ax.scatter(np.array(df['date']), df['borrow_rates'], df['utilization_ratio'])
    ax.set_ylabel('Borrowing interest rate', fontsize = 12, labelpad = 10)
    ax.set_zlabel('Utilization ratio', fontsize = 12, labelpad = 10)
    fig.suptitle(token.upper(), fontsize = 14)
    ax.view_init(elev, azim)
    ax.dist = 10
    ax.xaxis.set_ticks(df['date'])
    ax.xaxis.set_ticklabels(df.index)
    ax.xaxis.set_minor_locator(ticker.MaxNLocator(nbins=5, prune='lower'))
    plt.show()

def plot_raw_data(token: str, variable: str):
    '''
    Scatter plot of utilization rate vs borrow or supply rate. 
    '''
    df = make_dataframe(token)
    fig, ax = plt.subplots()
    ax = df[variable].plot()
    ax.set_ylabel(variable, fontsize = 18)
    ax.set_xlabel('Date', fontsize = 18)    
    fig.suptitle(str(token).upper() + ',' + variable, fontsize = 20)
    ax.tick_params(axis='both', which='major', labelsize=18)
    ax.legend()
    fig.savefig('../PhD/overleaf/5e6bad2e6490390001d3c466/images/' + str(token)+ str(variable)+'.pdf', bbox_inches='tight', dpi = 300)
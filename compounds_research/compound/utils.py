from os import path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from compounds_research import settings
from compounds_research.compound.fetch_exchange_rates import get_exchange_rates, make_exchange_rate_df
from compounds_research.compound.fetch_compound import make_dataframe
from simulator.engine.dai_rate_params import PARAM_REGIMES, PARAM_REGIME_NUMS

c_markets = {
    'cdai': 'dai',
    'ceth': 'eth',
    'cbat': 'bat',
    'czrx': 'zrx',
    'cusdc': 'usdc',
    'csai': 'sai',
    'crep': 'rep',
    'cwbtc': 'btc'
}

def make_original_df(token, resampling_frequency):
    '''
    Build dataframe from original pickle files. 
    :token: e.g. 'cdai'
    :resampling_frequency: e.g. 'D'
    '''
    df = pd.read_pickle(path.join(settings.DATA_PATH, 'compound', token + '.pkl'))

    df_regimes = pd.DataFrame(PARAM_REGIMES).transpose()
    df_regimes['regime'] = range(len(df_regimes))
    df_regimes['regime'] = df_regimes['regime']

    merged = pd.merge(df, df_regimes, how='outer', left_index=True, right_index=True) 
    merged['base_rate_per_block'] = merged['base_rate_per_block'].fillna(method='ffill')
    merged['multiplier_per_block'] = merged['multiplier_per_block'].fillna(method='ffill')
    merged['jump_multiplier_per_block'] = merged['jump_multiplier_per_block'].fillna(method='ffill')
    merged['kink'] = merged['kink'].fillna(method='ffill')
    merged['regime'] = merged['regime'].fillna(method='ffill')
    
    df_master = merged.resample(resampling_frequency).mean().dropna()
    
    return df_master

def make_rates_df(rate_type: str, frequency: str):
    '''
    Build dataframe of interest rates.
    :rate_type: 'borrow_rates', 'supply_rates' or 'exchange_rates'.
    :frequency: 'D', 'M', etc - resample frequency. 
    '''
    
    token_list = list(settings.COMPOUND_TOKEN_TRANSLATOR.keys())
    master_df = pd.DataFrame()
    for token in token_list:
        df = pd.read_pickle(path.join(settings.DATA_PATH, 'compound', token + '.pkl'))
        df = df.resample(frequency).mean()
        rates = df[rate_type]
        rates = rates.rename(token)
        master_df = pd.concat([master_df, rates], axis=1, join='outer')
    return master_df

def make_ex_rate_and_interest_rate_df(quote_token: str,
                                        base_token: str,
                                        rate_type: str, 
                                        frequency: str,    
                                        limit: int):
    '''
    For a token, return the final dataframe for the UIP analysis.
    :quote_token: e.g. 'eth'
    :base_token: e.g. 'rep'
    :rate_type: e.g. 'borrow_rates' or 'supply_rates'
    :frequency: e.g. 'D', 'W'
    :limit: number of data points to return
    '''
    interest_rates = make_rates_df(rate_type, frequency)
    interest_rates.rename(columns=settings.COMPOUND_TOKEN_TRANSLATOR, inplace=True)

    interest_rate_quote = interest_rates[quote_token]
    interest_rate_base = interest_rates[base_token]

    ex_rate = get_exchange_rates(base_symbol=base_token,
                                quote_symbol=quote_token,
                                limit=1000)['close']
    ex_rate.rename(str(base_token) + '_' + str(quote_token), inplace=True)

    master_df = pd.concat([ex_rate, interest_rate_quote, interest_rate_base], axis=1, join='outer')

    return master_df.dropna()


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

def plot_market_rates(frequency: str='d'):
    '''
    Plot the borrow and supply interest rates for a given compound market.
    '''
    df_borrow = make_rates_df('borrow_rates', frequency)
    df_supply = make_rates_df('supply_rates', frequency)
    for market in c_markets.keys():
        plt.clf()
        plt.plot(df_borrow[market], label='Borrow')
        plt.plot(df_supply[market], label='Supply')
        plt.legend()
        plt.title(c_markets[market])
        plt.ylabel('Interest Rate')
        plt.show()

def plot_market_util(token: str):
    '''
    Plot the utilization, total funds borrowed and supplied for a given compound market.
    '''
    CTOKEN_FILEPATH = path.join(settings.DATA_PATH, 'compound', token+'.pkl')
    df_market = pd.read_pickle(CTOKEN_FILEPATH)
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    lns1 = ax1.plot(df_market['total_supply_history'], label='Supply')
    lns2 = ax1.plot(df_market['total_borrows_history'], label='Borrow')
    ax1.set_ylabel(token)
    lns3 = ax2.plot(df_market['utilization_ratio'], label='Utilization', linestyle='--', linewidth=0.7, color='slategray', alpha=0.7)
    ax2.set_ylabel('Utilization')
    lns = lns1+lns2+lns3
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs)
    ax1.set_title(c_markets[token])

def clean_api_data(file: str):
    '''
    Corrects the 'total_supply_history' for an existing ctoken.pkl file.
    This correction is needed for data obtained from the compound API that has not been corrected yet.
    '''
    CTOKEN_FILEPATH = path.join(settings.DATA_PATH, "compound", file)
    df_ctoken = pd.read_pickle(CTOKEN_FILEPATH)
    df_ctoken['total_supply_history'] *= df_ctoken['exchange_rates']
    df_ctoken['total_supply_history'] = df_ctoken['total_supply_history'].astype('int64')
    df_ctoken['utilization_ratio'] = df_ctoken['total_borrows_history']/df_ctoken['total_supply_history']
    df_ctoken.to_pickle(path.join(settings.DATA_PATH, 'compound', file))

def get_comp_market(market: str):
    if market.lower() not in c_markets.keys():
        if 'c'+market.lower() in c_markets.keys():
            market = 'c'+market.lower()
        else:
            print('Invalid compound market: ', market)
            return
    CTOKEN_FILEPATH = path.join(settings.DATA_PATH, 'compound', market+'.pkl')
    return pd.read_pickle(CTOKEN_FILEPATH)
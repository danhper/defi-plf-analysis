from os import path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from compounds_research import settings
from compounds_research.compound.fetch_exchange_rates import get_exchange_rates, make_exchange_rate_df

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
    :token: e.g. 'eth'
    :other_token: e.g. 'rep'
    :rate_type: e.g. 'borrow_rates' or 'supply_rates'
    :frequency: e.g. 'D', 'W'
    :limit: number of data points to return
    '''
    interest_rates = make_rates_df(rate_type, frequency)
    interest_rates.rename(columns=settings.COMPOUND_TOKEN_TRANSLATOR, inplace=True)

    interest_rate_quote = interest_rates[quote_token]
    interest_rate_base = interest_rates[base_token]

    #FIX THIS LOGIC
    # ctoken_to_token_ex_rates = make_rates_df(rate_type='exchange_rates', frequency='D')
    # ctoken_to_token_ex_rates.rename(columns=settings.COMPOUND_TOKEN_TRANSLATOR, inplace=True)
    
    exchange_rates_quoted_in_token = make_exchange_rate_df(quote_token, limit)

    #FIX THIS LOGIC
    # ex_rates_final = ctoken_to_token_ex_rates.multiply(exchange_rates_quoted_in_token)

    exchange_rate_diffs = exchange_rates_quoted_in_token.diff()

    ex_rate_diff = exchange_rate_diffs[base_token]
    ex_rate_diff.rename('ex_rate_diff', inplace=True).shift(periods=-1)

    #CHECK ME : Is the shifting correct???
    interest_rate_diff = interest_rate_quote - interest_rate_base
    shifted_i_rate_diff = interest_rate_diff.rename('interest_rate_diff', inplace=True)

    master_df = pd.concat([ex_rate_diff, shifted_i_rate_diff], axis=1, join='outer')

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

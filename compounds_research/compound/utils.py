from os import path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from compounds_research import settings

def make_interest_rates_df(rate_type: str, frequency: str):
    '''
    Build dataframe of interest rates.
    :rate_type: 'borrow_rates' or 'supply_rates'.
    :frequency: 'D', 'M', etc - resample frequency. 
    '''
    token_list = ['cbat', 'cdai', 'ceth', 'crep', 'csai', 'cusdc', 'cwbtc', 'czrx']
    master_df = pd.DataFrame()
    for token in token_list:
        df = pd.read_pickle(path.join(settings.DATA_PATH, 'compound', token + '.pkl'))
        df = df.resample(frequency).mean()
        rates = df[rate_type]
        rates = rates.rename(token)
        master_df = pd.concat([master_df, rates], axis=1, join='outer')
    return master_df

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

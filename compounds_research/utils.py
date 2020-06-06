import re
import pandas as pd

from statsmodels.tsa.stattools import adfuller
from compounds_research.compound.utils import get_comp_market, c_markets, make_rates_df

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from compounds_research import settings

GRAY_INTENSITY = 0.5
GRAY = (GRAY_INTENSITY, GRAY_INTENSITY, GRAY_INTENSITY, 1)


def capitalize_camel_case(string: str) -> str:
    """Splits and capitalizes a camelCase string

    >>> capitalize_camel_case('stableBorrowRate')
    'Stable Borrow Rate'
    >>> capitalize_camel_case('liquidityRate')
    'Liquidity Rate'
    >>> capitalize_camel_case('currency')
    'Currency'
    """
    words = re.split("(?<=[a-z])(?=[A-Z])", string)
    return " ".join([word.capitalize() for word in words])


class StationarityTests:

    def __init__(self, significance=.05):
        self.SignificanceLevel = significance
        self.pValue = None
        self.isStationary = None

    def ADF_Stationarity_Test(self, timeseries, print_results = True):

        #Dickey-Fuller test:
        adf_test = adfuller(timeseries, autolag='AIC')
        
        self.pValue = adf_test[1]
        
        if (self.pValue < self.SignificanceLevel):
            self.isStationary = True
        else:
            self.isStationary = False
        
        if print_results:
            print(adf_test)
            df = pd.Series(adf_test[0:4], index=['ADF Test Statistic','P-Value','# Lags Used','# Observations Used'])
            #Add Critical Values
            for key, value in adf_test[4].items():
                df['Critical Value (%s)'%key] = value
            print('Augmented Dickey-Fuller Test Results:')
            print(df)
def get_token_usd_prices() -> pd.Series:
    return pd.Series(settings.USD_PRICES)


def amounts_to_usd(values: pd.Series) -> pd.Series:
    prices = get_token_usd_prices()
    result = values * prices
    return result[~result.isna()]

def get_market(market: str, platform: str) -> pd.DataFrame:
    '''
    Returns a data frame with info for a given market on a given platform.
    Columns: supply rate, borrow rate, total supply, total borrows, utilization
    '''
    if platform.lower() == 'compound':
        return get_comp_market(market)

def make_df_interest_rate_across_protocols():
    '''
    For a given token, build a dataframe for the interest rate across protocols.
    '''
    from compounds_research.aave.analyze_aave import load_data

    #Get compound rates
    df_compound = make_rates_df(rate_type= 'borrow_rates', frequency = 'D')
    df_compound = df_compound.rename(columns=settings.COMPOUND_TO_UPPER)
    df_compound = df_compound.add_prefix('C_')

    #Get Aave rates
    df_aave = load_data()
    df_aave = df_aave.set_index('Datetime')
    df_aave_grouped = df_aave.groupby('Currency').resample('D').mean()
    df_aave_pivoted = df_aave_grouped['Variable Borrow Rate'].unstack(level=-1).transpose()
    df_aave = df_aave_pivoted.add_prefix('A_')

    #Need to add dydx rates --> need dataframe

    df_master = pd.concat([df_compound, df_aave], axis=1)

    return df_master


def plot_cumulative_hist(locked_funds, skip_count=None, threshold=0.01, ticks_interval=None):
    locked_funds = sorted([v for v in locked_funds if v > 0])
    total = sum(locked_funds)
    cum_funds = []
    first_bucket = 0
    current_total = 0
    for fund in locked_funds:
        current_total += fund
        # only start adding at threshold (default = 1%) to avoid having to many data points
        if (skip_count is not None and first_bucket >= skip_count) or \
            (skip_count is None and current_total / total >= threshold):
            cum_funds.append(current_total)
        else:
            first_bucket += 1
    heights = [v / total for v in cum_funds]
    x = np.arange(first_bucket, first_bucket + len(heights))
    fig, ax = plt.subplots(figsize=(8, 4))
    plt.bar(x, heights, width=1.0, color=GRAY)

    if ticks_interval is None:
        ticks_interval = len(x) // 15
    ax.set_xticks(x[::ticks_interval])
    plt.xticks(rotation=45)
    ax.set_yticklabels(["{0}%".format(int(v * 100)) for v in ax.get_yticks()])
    ax.set_ylabel("Cumulative percentage of locked funds")
    ax.set_xlabel("Number of accounts")
    plt.tight_layout(w_pad=0.5)
    return ax

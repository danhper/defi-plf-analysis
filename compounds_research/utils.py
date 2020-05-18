import re
import pandas as pd

from statsmodels.tsa.stattools import adfuller
from compounds_research.compound.utils import get_comp_market, c_markets, make_rates_df

import pandas as pd

from compounds_research import settings
from compounds_research.aave.analyze_aave import load_data


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
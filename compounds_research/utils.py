import re
import pandas as pd

from statsmodels.tsa.stattools import adfuller


import pandas as pd

from compounds_research import settings


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

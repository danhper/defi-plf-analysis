import re

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


def get_token_usd_prices() -> pd.Series:
    return pd.Series(settings.USD_PRICES)


def amounts_to_usd(values: pd.Series) -> pd.Series:
    prices = get_token_usd_prices()
    result = values * prices
    return result[~result.isna()]

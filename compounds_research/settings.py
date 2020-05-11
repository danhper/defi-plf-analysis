from os import path


PROJECT_ROOT = path.dirname(path.dirname(__file__))
DATA_PATH = path.join(PROJECT_ROOT, "data")
FIGURES_PATH = path.join(PROJECT_ROOT, "figures")

# 2020-05-09 23:12
USD_PRICES = {
    "LINK": 4.09,
    "LEND": 0.064801,
    "TUSD": 1.00,
    "USDC": 0.999259,
    "DAI": 1.00,
    "SAI": 1.00,
    "BAT": 0.221774,
    "ETH": 211.83,
    "WETH": 211.83,
}

COMPOUND_TOKEN_TRANSLATOR = {'ceth': 'eth',
                            'cbat': 'bat',
                            'czrx': 'zrx',
                            'cusdc': 'usdc',
                            'cdai': 'dai',
                            'csai': 'sai',
                            'crep': 'rep',
                            'cwbtc': 'wbtc'}
import numpy as np

BLOCKS_PER_YEAR = 2102400

def utilization_rate(cash: int, borrows: int, reserves: int):
    '''
    In original function units, unmodified.
    :cash: cash, scaled up by 1e18. Cash = supply - borrows + reserves
    :borrows: borrows, scaled up by 1e18 (e.g. 1,000,000 DAI --> 1000000000000000000000000)
    :reserves: reserves, scaled up by 1e18.
    '''
    if borrows == 0 :
        return 0
    return int(borrows * 1e18 / (cash + borrows - reserves))

def get_borrow_rate(cash: int, borrows: int, reserves: int, regime_params):
    '''
    In original function units, unmodifed.
    :cash: cash, scaled up by 1e18.
    :borrows: scaled up by 1e18.
    :reserves: scaled up by 1e18.
    :regime_params: dictionary of governing regime params.
    '''
    if regime_params['model'] == 'dai_rate':
        util = utilization_rate(cash=cash, borrows=borrows, reserves=reserves)
        if util <= regime_params['kink']:
            return int(util * regime_params['multiplier_per_block'] / 1e18 + regime_params['base_rate_per_block'])
        else:
            normal_rate = regime_params['kink'] * regime_params['multiplier_per_block'] / 1e18 +  regime_params['base_rate_per_block']
            excess_util = util - regime_params['kink']
            return int(excess_util * regime_params['jump_multiplier_per_block'] / 1e18 + normal_rate)
    if regime_params['model'] == 'jump_rate':
        util = utilization_rate(cash=cash, borrows=borrows, reserves=reserves)
        if util <= regime_params['kink']:
            return int(util * regime_params['multiplier_per_block'] / 1e18 + regime_params['base_rate_per_block']) 
        else:
            normal_rate = regime_params['kink'] * regime_params['multiplier_per_block'] / 1e18 + regime_params['base_rate_per_block']
            excess_util = util - regime_params['kink']
            jump_multiplier = regime_params['multiplier_per_block'] * regime_params['jump']
            return int(excess_util * jump_multiplier / 1e18 + normal_rate)

def get_supply_rate(cash: int, borrows: int, reserves: int, regime_params):
    '''
    In original function units, unmodified. 
    :cash: scaled up by 1e18.
    :borrows: scaled up by 1e18.
    :reserves: scaled up by 1e18.
    '''
    one_minus_reserve_factor = 1e18 - regime_params['reserve_factor']
    borrow_rate = get_borrow_rate(cash=cash, borrows=borrows, reserves=reserves, regime_params=regime_params)
    rate_to_pool = borrow_rate * one_minus_reserve_factor / 1e18
    return int(utilization_rate(cash=cash, borrows=borrows, reserves=reserves) * rate_to_pool / 1e18)
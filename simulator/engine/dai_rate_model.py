import numpy as np

# Take a given market, e.g. for DAI, derrive the equations that govern the interest rates in each of the three markets
# Compound

# Contract 0x000000007675b5E1dA008f037A0800B309e0C493, 21 May 2020
# multiplierPerBlock = 10569930661
# baseRatePerBlock = 0
# kink = 900000000000000000
# jumpMultiplierPerBlock = 570776255707
# blocksPerYear = 2102400
# ReserveFactorMantissa = 50000000000000000


# function utilizationRate(uint cash, uint borrows, uint reserves) public pure returns (uint) {
#     // Utilization rate is 0 when there are no borrows
#     if (borrows == 0) {
#         return 0;
#     }

#     return borrows.mul(1e18).div(cash.add(borrows).sub(reserves));
# }

# function getBorrowRate(uint cash, uint borrows, uint reserves) public view returns (uint) {
#     uint util = utilizationRate(cash, borrows, reserves);

#     if (util <= kink) {
#         return util.mul(multiplierPerBlock).div(1e18).add(baseRatePerBlock);
#     } else {
#         uint normalRate = kink.mul(multiplierPerBlock).div(1e18).add(baseRatePerBlock);
#         uint excessUtil = util.sub(kink);
#         return excessUtil.mul(jumpMultiplierPerBlock).div(1e18).add(normalRate);
#     }
# }
# function getSupplyRate(uint cash, uint borrows, uint reserves, uint reserveFactorMantissa) public view returns (uint) {
#     uint oneMinusReserveFactor = uint(1e18).sub(reserveFactorMantissa);
#     uint borrowRate = getBorrowRate(cash, borrows, reserves);
#     uint rateToPool = borrowRate.mul(oneMinusReserveFactor).div(1e18);
#     return utilizationRate(cash, borrows, reserves).mul(rateToPool).div(1e18);
# }

#Recreate in Python
MULTIPLIER_PER_BLOCK = 10569930661
KINK = 900000000000000000
JUMP_MULTIPLIER_PER_BLOCK = 570776255707
BASE_RATE_PER_BLOCK = 0
RESERVE_FACTOR = 50000000000000000
BLOCKS_PER_YEAR = 2102400

# borrows = 12123057761032616257527258
# reserves = 172000131734217327575775
# cash = 6971699007994218847501026

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

def get_borrow_rate(cash: int, borrows: int, reserves: int):
    '''
    In original function units, unmodifed.
    :cash: cash, scaled up by 1e18.
    :borrows: scaled up by 1e18.
    :reserves: scaled up by 1e18.
    '''
    util = utilization_rate(cash=cash, borrows=borrows, reserves=reserves)
    if util <= KINK:
        return int(util * MULTIPLIER_PER_BLOCK / 1e18 + BASE_RATE_PER_BLOCK)
    else:
        normal_rate = KINK * MULTIPLIER_PER_BLOCK / 1e18 +  BASE_RATE_PER_BLOCK
        excess_util = util - KINK
        return int(excess_util * JUMP_MULTIPLIER_PER_BLOCK / 1e18 + normal_rate)

def get_supply_rate(cash: int, borrows:int, reserves: int, reserve_factor: int):
    '''
    In original function units, unmodified. 
    :cash: scaled up by 1e18.
    :borrows: scaled up by 1e18.
    :reserves: scaled up by 1e18.
    '''
    one_minus_reserve_factor = 1e18 - reserve_factor
    borrow_rate = get_borrow_rate(cash=cash, borrows=borrows, reserves=reserves)
    rate_to_pool = borrow_rate * one_minus_reserve_factor / 1e18
    return int(utilization_rate(cash=cash, borrows=borrows, reserves=reserves) * rate_to_pool / 1e18)
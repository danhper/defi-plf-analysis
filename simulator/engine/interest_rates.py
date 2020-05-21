from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm

import numpy as np

#if using a Jupyter notebook, include:
%matplotlib inline

#Take a given market, e.g. for DAI, derrive the equations that govern the interest rates in each of the three markets
#Compound

#Contract 0x000000007675b5E1dA008f037A0800B309e0C493, 21 May 2020
#multiplierPerBlock = 10569930661
#baseRatePerBlock = 0
#kink = 900000000000000000
#jumpMultiplierPerBlock = 570776255707
#blocksPerYear = 2102400
#ReserveFactorMantissa = 50000000000000000


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

def utilization_rate(cash: int, borrows: int, reserves: int):
    if borrows == 0 :
        return 0
    return int(borrows * 1e18 / (cash + borrows - reserves))

def get_borrow_rate(cash: int, borrows: int, reserves: int):
    util = utilization_rate(cash=cash, borrows=borrows, reserves=reserves)
    if util <= KINK:
        return int(util * MULTIPLIER_PER_BLOCK / 1e18 + BASE_RATE_PER_BLOCK)
    else:
        normal_rate = KINK * MULTIPLIER_PER_BLOCK / 1e18 +  BASE_RATE_PER_BLOCK
        excess_util = util - KINK
        return int(excess_util * JUMP_MULTIPLIER_PER_BLOCK / 1e18 + normal_rate)

def get_supply_rate(cash: int, borrows:int, reserves: int, reserve_factor: int):
    one_minus_reserve_factor = 1e18 - reserve_factor
    borrow_rate = get_borrow_rate(cash=cash, borrows=borrows, reserves=reserves)
    rate_to_pool = borrow_rate * one_minus_reserve_factor / 1e18
    return int(utilization_rate(cash=cash, borrows=borrows, reserves=reserves) * rate_to_pool / 1e18)

borrows = 12123057761032616257527258
reserves = 172000131734217327575775
cash = 6971699007994218847501026
blocks_per_year = 2102400

#Plot the function
%matplotlib inline
fig = plt.figure()
ax = fig.gca(projection='3d')

reserves = 0
supply = np.arange(0, 1000000, 10000)
borrows = np.arange(0, 1000000, 10000)
S, B = np.meshgrid(supply, borrows)

br_dict = {}
for s in supply:
    s_scaled = int(s)
    for b in borrows:
        b_scaled = int(b)
        cash = s - b
        if cash <= 0:
            br_dict[(s_scaled,b_scaled)] = 0
        if cash > 0:
            br = get_borrow_rate(cash=cash, borrows=b, reserves=reserves)
            br_scaled = int(br)
            br_dict[(s_scaled,b_scaled)] = br_scaled * blocks_per_year

Z = np.ones((100,100))

for key in br_dict:
    i = int(key[0] / 10000)-1
    j = int(key[1] / 10000)-1
    Z[i][j] = int(br_dict[key])

surf = ax.plot_surface(S, B, Z, rstride=1, cstride=1, cmap=cm.winter, linewidth=0, antialiased=True)
# ax.set_zlim(0, 900000)

plt.show()

#State the objective function for interest rates. what are we trying to maximize? Thing to include: stability, efficiency, responsiveness, economic security?
#Propose a new interest rate model that would maximize these factors, for each protocol given the supply and demand that was experienced, what would the interest rates look like? 
 # - Here, probably cannot make the assumption that supply and demand would remain the same, since these are endogenous to the original system parameters. However, could simulate the behaviour for random supply and demand, or normally distributed supply and demand?
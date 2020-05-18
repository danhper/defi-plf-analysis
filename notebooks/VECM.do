import delimited "/Users/zebeelou/PhD/compounds-research/data/stata/interest_rates.csv", encoding(ISO-8859-2)
gen date=date(v1,"YMD###")
tsset date

//Plots
twoway (line c_eth date) (line a_eth date)
twoway (line c_dai date) (line a_dai date)

//VECM fitting
varsoc c_dai a_dai //suggests to use 4 lags
vecrank c_dai a_dai // suggests 1 cointegrating equation

vec c_dai a_dai, lags(4)

//Specification testing
predict ce1, ce equ(#1)
twoway line ce1 date

// predict ce2, ce equ(#2)
// twoway line ce2 date

//Check whether we have correctly specified the number of cointegrating equations
vecstable, graph

//Check for serial correlation in the residuals
veclmar, mlag(4) // suggests autocorrelation. Increase number of lags to 6

vec c_dai a_dai, lags(6)
veclmar, mlag(6)

//Check that the errors are normally distributed
vecnorm // Strongly reject normality

//Generate IRF
irf create vec1, set(vecintro, replace) step(24)
irf graph oirf, impulse(c_dai) response(a_dai) yline(0)

irf graph oirf, impulse(a_dai) response(c_dai) yline(0)


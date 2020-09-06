clear
set scheme s1mono

//////////////////////////////DAI/////////////////////////////////////

import delimited "PhD/compounds-research/data/stata/interest_rates_dai.csv", encoding(ISO-8859-2)
gen date=date(v1,"YMD###")
format %tdDD/NN/CCYY date
tsset date

label variable c_dai `"Compound DAI"'
label variable a_dai `"Aave DAI"'
label variable d_dai `"dYdX DAI"'


//Plots
twoway (line c_dai date, lwidth(medium)) (line a_dai date, lpattern(shortdash) lwidth(medium)) (line d_dai date, lpattern(longdash) lwidth(medium)), ytitle("Borrow interest rate") xtitle("")
graph export PhD/overleaf/5e6bad2e6490390001d3c466/stata_outputs/DAI.pdf, replace

//Stationarity testing - levels

dfuller c_dai, regress //appropriate number of lags
// Non-stationary

dfuller a_dai, regress //appropriate number of lags
// Stationary

dfuller d_dai, lags (1) regress //appropriate number of lags
// Non-stationary

//Stationarity testing - differences

dfuller d.c_dai, lags (1) trend regress
// Stationary

dfuller d.a_dai, lags (1) trend regress
// Stationary

dfuller d.d_dai, lags (1) trend regress
// Stationary

//Lag selection
varsoc c_dai a_dai d_dai
//suggests to use 4 lags. However this results in some misspeccifation in later testing, so increase so 5. 

//Cointegrating equations
vecrank a_dai c_dai d_dai, lags(5) // suggests 1 cointegrating equations - Johansen test. Fail to reject null of at most 2 cointegrating equation. 

// VECM fitting
vec c_dai a_dai d_dai, rank(2) lags(5)
eststo: quietly vec c_dai a_dai d_dai, rank(2) lags(5)
esttab using PhD/overleaf/5e6bad2e6490390001d3c466/stata_outputs/stata_results_dai_original.tex, label replace booktabs

//Specification testing
predict ce, ce
twoway line ce date, lwidth(medium) xtitle("")
graph export PhD/overleaf/5e6bad2e6490390001d3c466/stata_outputs/DAI_CE_1.pdf, replace

//Check whether we have correctly specified the number of cointegrating equations
vecstable, graph
graph export PhD/overleaf/5e6bad2e6490390001d3c466/stata_outputs/DAI_vecstable.pdf, replace
//looks good

//Check for serial correlation in the residuals
veclmar, mlag(5) 
// looks good

//Check that the errors are normally distributed
vecnorm 
// Strongly reject normality

//Generate IRF
irf create vec1, set(vecintro, replace) step(24)
irf graph oirf, impulse(c_dai) response(a_dai) yline(0) xtitle("Steps from shock")
graph export PhD/overleaf/5e6bad2e6490390001d3c466/stata_outputs/I_CDAI_R_DAI.pdf, replace
// shock to cdai has a permanent effect on a_dai

irf graph oirf, impulse(a_dai) response(c_dai) yline(0) xtitle("Steps from shock")
graph export PhD/overleaf/5e6bad2e6490390001d3c466/stata_outputs/I_ADAI_R_CDAI.pdf, replace
// same, vice versa

irf graph oirf, impulse(d_dai) response(c_dai) yline(0) xtitle("Steps from shock")
graph export PhD/overleaf/5e6bad2e6490390001d3c466/stata_outputs/I_DDAI_R_CDAI.pdf, replace
// same

irf graph oirf, impulse(d_dai) response(a_dai) yline(0) xtitle("Steps from shock")
graph export PhD/overleaf/5e6bad2e6490390001d3c466/stata_outputs/I_DDAI_R_ADAI.pdf, replace
// same, strong

///////////////////////////USDC//////////////////////////////////////////

clear
import delimited "PhD/compounds-research/data/stata/interest_rates_usdc.csv", encoding(ISO-8859-2)
gen date=date(v1,"YMD###")
format %tdDD/NN/CCYY date
tsset date

label variable c_usdc `"Compound USDC"'
label variable a_usdc `"Aave USDC"'
label variable d_usdc `"dYdX USDC"'

//Plots
twoway (line c_usdc date, lwidth(medium)) (line a_usdc date, lpattern(shortdash) lwidth(medium)) (line d_usdc date, lpattern(longdash) lwidth(medium)), ytitle("Borrow interest rate") xtitle("")
graph export PhD/overleaf/5e6bad2e6490390001d3c466/stata_outputs/USDC.pdf, replace

//Stationarity testing - levels
dfuller c_usdc, lags (1) regress 
// unit root

dfuller a_usdc, lags (1)  regress
// Stationary
dfuller d_usdc, lags (1)  regress 
// unit root

//Stationarity testing - differences
dfuller d.c_usdc, lags (1) trend regress 
// Stationary

dfuller d.a_usdc, lags (1) trend regress 
// Stationary
dfuller d.d_usdc, lags (1) trend regress 
// Stationary

//Lag selection
varsoc c_usdc a_usdc d_usdc 
//suggests to use 2 lags. 

//Cointegrating equations
vecrank c_usdc a_usdc d_usdc, lags(2) levela 
// suggests 2 cointegrating equations - Johansen test. Fail to reject null of at most 2 cointegrating equations. 

//VECM fitting
vec c_usdc a_usdc d_usdc, rank(2) lags(2)

//Specification testing
predict ce1, ce equ(#1)
twoway line ce1 date, lwidth(medium) xtitle("")

predict ce2, ce equ(#2)
twoway line ce2 date, lwidth(medium) xtitle("")

//Check whether we have correctly specified the number of cointegrating equations
vecstable, graph //looks good

//Check for serial correlation in the residuals
veclmar, mlag(4) // looks like there's some SC. increase lags to 3

vecrank c_usdc a_usdc d_usdc, lags(3) levela  

//New Spec
vec c_usdc a_usdc d_usdc, rank(2) lags(3)
eststo clear
eststo: quietly vec c_usdc a_usdc d_usdc, rank(2) lags(3)
esttab using PhD/overleaf/5e6bad2e6490390001d3c466/stata_outputs/stata_results_usdc_original.tex, label replace booktabs

predict ce3, ce equ(#1)
twoway line ce3 date, lwidth(medium) xtitle("")
graph export PhD/overleaf/5e6bad2e6490390001d3c466/stata_outputs/USDC_CE_1.pdf, replace

predict ce4, ce equ(#2)
twoway line ce4 date, lwidth(medium) xtitle("")
graph export PhD/overleaf/5e6bad2e6490390001d3c466/stata_outputs/USDC_CE_2.pdf, replace

vecstable, graph //looks good
graph export PhD/overleaf/5e6bad2e6490390001d3c466/stata_outputs/USDC_vecstable.pdf, replace

veclmar, mlag(4) //looks good

//Check that the errors are normally distributed
vecnorm // Strongly reject normality

//Generate IRF
irf create vec1, set(vecintro, replace) step(24)

irf graph oirf, impulse(c_usdc d_usdc) response(a_usdc) yline(0) xtitle("Steps from shock")
graph export PhD/overleaf/5e6bad2e6490390001d3c466/stata_outputs/I_CUSDCDUSDC_R_AUSDC.pdf, replace

irf graph oirf, impulse(a_usdc d_usdc) response(c_usdc) yline(0) xtitle("Steps from shock") 
graph export PhD/overleaf/5e6bad2e6490390001d3c466/stata_outputs/I_AUSDCDUSDC_R_CUSDC.pdf, replace

irf graph oirf, impulse(c_usdc a_usdc) response(d_usdc) yline(0) xtitle("Steps from shock")
graph export PhD/overleaf/5e6bad2e6490390001d3c466/stata_outputs/I_AUSDCCUSDC_R_DUSDC.pdf, replace

irf graph oirf, impulse(c_usdc) response(a_usdc d_usdc) yline(0) xtitle("Steps from shock")
graph export PhD/overleaf/5e6bad2e6490390001d3c466/stata_outputs/I_CUSDC_R_DUSDCAUSDC.pdf, replace

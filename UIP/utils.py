#For compound, assemble dataframe per market of interest rate on each token and the exchange rate between them (3 columns, 4 indluding the index

from compounds_research.compound import utils, fetch_exchange_rates

borrow_rates = utils.make_interest_rates_df('borrow_rates', 'D')

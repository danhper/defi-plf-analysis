import argparse
import datetime as dt
import glob
import json
from os import path

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt


from compounds_research import plotting
from compounds_research import settings
from compounds_research import utils


FILEPATH = path.join(settings.DATA_PATH, "aave", "aave.jsonl")


BIGDECIMAL_COLUMNS = [
  'variableBorrowRate',
  'variableBorrowIndex',
  'utilizationRate',
  'stableBorrowRate',
  'liquidityIndex',
  'liquidityRate',
  'totalLiquidity',
  'availableLiquidity',
  'totalBorrows',
  'totalBorrowsVariable',
  'totalBorrowsStable',
]

BIGDECIMAL_NORMALIZED_COLUMNS = [
    'liquidityIndex',
    'liquidityRate',
    'stableBorrowRate',
    'variableBorrowRate',
]


def load_data(filepath=FILEPATH):
    df = pd.DataFrame()
    for filename in glob.glob(path.join(settings.DATA_PATH, "aave", "*.csv")):
        currency_df = pd.read_csv(filename)
        currency_name = path.splitext(path.basename(filename))[0]
        currency_df["symbol"] = currency_name
        df = df.append(currency_df)

    df["datetime"] = pd.to_datetime(df["timestamp"], unit="s")
    return df.rename(utils.capitalize_camel_case, axis="columns")


def filter_currencies(df, currencies):
    if not isinstance(currencies, list):
        currencies = [currencies]
    return df[df["Symbol"].isin(currencies)]


def unique_currencies(df):
    return df["Symbol"].unique()


def get_liquidity_median(df):
    column = "Total Liquidity"
    filtered = df[df[column] != 0]
    amounts = filtered.groupby("Symbol")[column].median() / 1e18
    return utils.amounts_to_usd(amounts).sort_values()


def plot_correlation(df, currency, output=None):
    filtered_df = filter_currencies(df, currency)
    _ax = plotting.plot_correlation(filtered_df.corr())
    plotting.output_plot(output)


def plot_time_series(df, currency, y, output=None):
    filtered_df = filter_currencies(df, currency)
    plotting.plot_time_series(filtered_df, x="Datetime", y=y)
    plotting.output_plot(output)


def plot_interest_utilization(df, currency, output=None):
    filtered_df = filter_currencies(df, currency)
    plotting.plot_interest_and_utilization_rates(
        filtered_df, x="Datetime", y_interest="Variable Borrow Rate", y_utilzation="Utilization Rate")
    plotting.output_plot(output)


parser = argparse.ArgumentParser(prog="parser")
subparsers = parser.add_subparsers(dest="command")

correlation_parser = subparsers.add_parser("plot-correlation")
correlation_parser.add_argument("currency", help="Currency to plot")
correlation_parser.add_argument("-o", "--output", help="Output file")

correlation_parser = subparsers.add_parser("plot-time-series")
correlation_parser.add_argument("currency", help="Currency to plot")
correlation_parser.add_argument("-o", "--output", help="Output file")
correlation_parser.add_argument("-y", help="Output file", required=True)

correlation_parser = subparsers.add_parser("plot-interest-utilization")
correlation_parser.add_argument("currency", help="Currency to plot")
correlation_parser.add_argument("-o", "--output", help="Output file")



def main():
    args = vars(parser.parse_args())
    command = args.pop("command", None)
    if not command:
        parser.error("no command given")
    func_name = command.replace("-", "_")
    func = globals()[func_name]
    df = load_data()
    func(df, **args)


if __name__ == "__main__":
    main()

# highest_variance_currencies = df.groupby(by="Currency")["rate"].std().sort_values(ascending=False).iloc[:5]

# highest_variance_currencies.index.values
# to_plot = df[df["reserve.symbol"].isin(highest_variance_currencies.index.values)]

# ax = sns.lineplot(x="datetime", y="utilizationRate", hue="Currency", data=to_plot)

# # currency = df[df["reserve.symbol"] == "SNX"]

# plt.figure(figsize=(15, 10))
# # ax = sns.lineplot(x="datetime", y="rate", data=currency)
# ax = sns.lineplot(x="datetime", y="variableBorrowRate", hue="Currency", data=to_plot)
# ax.set_xlabel("Date")
# ax.set_ylabel("Interest rate")
# plt.xticks(rotation=45)

# plt.tight_layout()
# plt.savefig("../tmp/interest-rates.pdf")

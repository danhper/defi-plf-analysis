import re

import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt

from compounds_research import utils


HEATMAP_COLORS = "YlGnBu"


matplotlib.rc("font", size=20)
matplotlib.rc("lines", linewidth=2)


def plot_correlation(corr, **kwargs):
    plt.figure(figsize=(15, 10))
    res = sns.heatmap(corr, annot=False, cmap=HEATMAP_COLORS, **kwargs)
    plt.tight_layout()
    return res


def plot_interest_and_utilization_rates(df, x, y_interest, y_utilzation, **kwargs):
    ax = plot_time_series(df, x, y_interest)
    plot_utilization_rate(df, x, y_utilzation, ax=ax)
    return ax


def plot_time_series(df, x, y, **kwargs):
    plt.figure(figsize=(15, 10))
    ax = sns.lineplot(x=x, y=y, data=df, **kwargs)
    ax.set_xlabel("Date")
    ax.set_ylabel(utils.capitalize_camel_case(y))
    plt.xticks(rotation=45)
    plt.tight_layout()
    return ax


def plot_utilization_rate(df, x, y, ax=None, **kwargs):
    if ax is None:
        plt.figure(figsize=(15, 10))
        ax = sns.lineplot(x=x, y=y, data=df)
    else:
        ax = ax.twinx()
        sns.lineplot(x=x, y=y, data=df, ax=ax, dashes=True)
    ax.set_xlabel("Date")
    ax.set_ylabel("Utilization rate")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return ax


def output_plot(output: str = None):
    if output is None:
        plt.show()
    else:
        plt.savefig(output)

def plot_kink_deltas(df_series, **kwargs):
    plt.figure(figsize=(15, 10))
    ax = sns.distplot(df_series, kde=False)
    ax.set_xlabel("(Actual Rate) - (Kink Rate) ")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return ax
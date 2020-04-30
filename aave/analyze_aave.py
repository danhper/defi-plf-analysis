import datetime as dt
import json

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt


matplotlib.rc("font", size=20)
matplotlib.rc("lines", linewidth=2)


with open("./aave.jsonl") as f:
    df = pd.DataFrame(pd.json_normalize([json.loads(line) for line in f]))


df["datetime"] = pd.to_datetime(df["timestamp"], unit="s")

df["rate"] = df["liquidityRate"].astype(float) / 1e26

df["utilization_rate"] = df.utilizationRate.astype(np.float)

# df = df[df["datetime"] >= dt.datetime(2020, 4, 1)]
df["Currency"] = df["reserve.symbol"]

highest_variance_currencies = df.groupby(by="Currency")["rate"].std().sort_values(ascending=False).iloc[:5]

highest_variance_currencies.index.values
to_plot = df[df["reserve.symbol"].isin(highest_variance_currencies.index.values)]

ax = sns.lineplot(x="datetime", y="utilization_rate", hue="Currency", data=to_plot)

# currency = df[df["reserve.symbol"] == "SNX"]

plt.figure(figsize=(15, 10))
# ax = sns.lineplot(x="datetime", y="rate", data=currency)
ax = sns.lineplot(x="datetime", y="rate", hue="Currency", data=to_plot)
ax.set_xlabel("Date")
ax.set_ylabel("Interest rate")
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig("../tmp/interest-rates.pdf")

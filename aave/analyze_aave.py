import datetime as dt
import json

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


with open("./aave.jsonl") as f:
    df = pd.DataFrame(pd.json_normalize([json.loads(line) for line in f]))


df["datetime"] = pd.to_datetime(df["timestamp"], unit="s")

df["rate"] = df["liquidityRate"].astype(float) / 1e26

df = df[df["datetime"] >= dt.datetime(2020, 4, 1)]

currency = df[df["reserve.symbol"] == "SNX"]

plt.figure(figsize=(15, 10))
g = sns.lineplot(x="datetime", y="rate", data=currency)
# g = sns.lineplot(x="datetime", y="rate", hue="reserve.symbol", data=df)
plt.xticks(rotation=45)

plt.savefig("interest-rates-april.png")

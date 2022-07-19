
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

ts = pd.read_csv('time_series.csv')

# Have a look at the time series
print(ts)
input("Press Enter to continue...")

# Have a look at the time series head
print(ts.head())
input("Press Enter to continue...")

# The time series index
print(ts.index)
input("Press Enter to continue...")

# Set the index of the data frame
ts.set_index('Date', inplace = True)
print(ts)
input("Press Enter to continue...")


# Filter , 'Euro Semi-Core 5-1'
filtered_ts = ts.filter(['Europe', 'US IG 3-5', 'Euro HY Corp', 'Euro IL'])
print(filtered_ts)
input("Press Enter to continue...")

# Normalize
filtered_ts_norm = 100 * filtered_ts / filtered_ts.iloc[0]
print(filtered_ts_norm)
input("Press Enter to continue...")


# Plot
filtered_ts_norm.plot()
plt.show()

# Compute the returns as percentange change and drop the undefined generated in the process
returns = filtered_ts_norm.pct_change().dropna()
print(returns)
input("Press Enter to continue...")

# Clip them between -0.1 and 0.1
clipped_returns = returns.clip(-0.1,0.1)
input("Press Enter to continue...")

# Plot
clipped_returns.plot.hist(bins=100, alpha=0.5)
plt.show()


# -*- coding: utf-8 -*-
from statsmodels import api as sm
from matplotlib import pyplot as plt

def plot_acf_and_pacf(series, lags=30):
    fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True, figsize=(14,12))
    sm.graphics.tsa.plot_acf(series, lags=lags, ax=ax1)
    sm.graphics.tsa.plot_pacf(series, lags=lags, ax=ax2)

    fig.show()
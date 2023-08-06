import matplotlib.pyplot as plt
import pandas as pd

def doble_line_plot(df, x_axis, column1, column2, xlim, ylabel = '', fontsize = 14):
    fig, ax1 = plt.subplots(figsize=(15, 8))
    ax2 = ax1.twinx()
    ax1.set_ylim(xlim)
    ax2.set_ylim(xlim)

    ax1.plot(df[x_axis], df[column2], color='red', lw=1)
    ax2.plot(df[x_axis], df[column1], color='blue', lw=1)

    ax1.set_xlabel("Date")
    ax1.set_ylabel(ylabel, fontsize=fontsize)
    ax1.tick_params(axis="y")

    ax2.set_ylabel(ylabel, fontsize=fontsize)
    ax2.tick_params(axis="y")
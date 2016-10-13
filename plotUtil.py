#!/usr/bin/env python

# This is a util for plotting

import matplotlib.pyplot as plt
import numpy as np

# plots numerical values
def timeSeries(values, title=None, xlabel='Time', ylabel='Value'):
    figure = plt.figure()
    ax = plt.subplot(111)
    if title:
        plt.title(title)
    axisNos = range(0, len(values));
    #axisTicks, labels = getAxisTicksDateLabels()
    # width = 1
    ax.bar(axisNos, values, 1, linewidth=0, color='red')
    #plt.xticks(axisTicks)
    # we want integers no the y axis, we want to have some space at the top, and we want 10 ticks
    _max = np.amax(values)
    ylim = int(_max  + np.maximum(_max*0.2, 1))
    stepSize = np.maximum(int(_max/10), 1)
    plt.yticks(np.arange(0, ylim, stepSize))
    #ax.set_xticklabels(labels, rotation=30)
    ax.set_xlim([axisNos[0], axisNos[-1]])
    ax.set_ylim([0, ylim])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()
    

import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
mokh_db = pd.read_csv('all_data/tables/mokh.csv', index_col=0)

statistics = {'None': 0}



for index, row in mokh_db.iterrows():
    print(index, row['gene'])
    if type(row['gene']) == float:
        statistics['None'] += 1
    elif row['gene'] == 'None':
        statistics['None'] += 1
    else:
        biotype = row['gene'].split(',')[1].split(':')[1]
        print(biotype)

        if biotype in statistics.keys():
            statistics[str(biotype)] += 1
        else:
            statistics[biotype] = 1
    print(statistics)
    print('\n')
    
sizes = list(statistics.values())

labels = list(statistics.keys())
labels2 = []

for i in labels:
    labels2.append(str(i) + ': ' + str(statistics[i]))
    
    
    
fig, ax = plt.subplots(figsize=(24, 12), subplot_kw=dict(aspect="equal"))

wedges, texts = ax.pie(sizes, wedgeprops=dict(width=0.5), startangle=-40)

bbox_props = dict(boxstyle="round,pad=0.3", fc="w", ec="k", lw=0.9)
kw = dict(arrowprops=dict(arrowstyle="-"),
          bbox=bbox_props, zorder=0, va="center", size=15)

for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1)/2. + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    ax.annotate(labels2[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                horizontalalignment=horizontalalignment, **kw)

ax.set_title("Eudicots-monocots dataset: functional annotation of Physcomitrella patens clusters", size=25)

plt.show()
plt.savefig('statistics.png')
import pandas as pd
import importlib
import tex
importlib.reload(tex)
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point
from matplotlib.patches import Polygon as MatplotlibPolygon

import namingroutine
importlib.reload(namingroutine)
names = namingroutine.Initialize()

dictfilters = names['dictfilters']
dictfiltermagnames = names['dictfiltermagnames']
colors = names['colors']

def pointstobeplottedHB(concatnew, parallelogram_vertices):

    x2 = concatnew['x2']
    y2 = concatnew['y2']
    IDhb = concatnew['ID']
    result = pd.concat([x2, y2, IDhb], axis=1) # made a df called result with 2 cols x2 and y2

    mask = result.apply(lambda row: point_inside_parallelogram(row.iloc[0], row.iloc[1], parallelogram_vertices), axis=1)
    points_inside_parallelogram = result[mask]

    yHB = points_inside_parallelogram.iloc[:,1]
    xHB = points_inside_parallelogram.iloc[:,0]
    IDHBsent = points_inside_parallelogram.iloc[:,2]

    return xHB, yHB, x2, y2, IDHBsent

def point_inside_parallelogram(x, y, parallelogram_vertices):
    parallelogram_shapely = Polygon(parallelogram_vertices)
    return Point(x, y).within(parallelogram_shapely)

def initialize(df, min_mag_hb, max_mag_hb, min_col_hb, max_col_hb, entries, save, save_plots_path, clustername):

    # print(entries)

    concatnew = pd.concat([(df['F275W'] ), (df['F275W'] - df['F336W']), df['ID']], axis=1)
    concatnew.columns = ['y2', 'x2', 'ID']    
    xHB, yHB, x2, y2, IDHB = pointstobeplottedHB(concatnew, entries)  
    concatnew = pd.concat([xHB, yHB, IDHB], axis = 1)

    print(f"Total HB Stars: {len(concatnew['x2'])}")

    plt.figure(figsize=(7, 5))
    plt.scatter(x2, y2, marker = 'o', s=2, edgecolors='none', color='black', rasterized=True)
    plt.scatter(xHB, yHB, marker = 's', s=2, edgecolors='none', color='brown', label = 'HB Manual Selection ' + str(len(xHB)), rasterized=True)
    parallelogram = MatplotlibPolygon(entries, edgecolor='black', facecolor='none', linestyle='solid', linewidth=1)
    plt.gca().add_patch(parallelogram)

    plt.legend() # , framealpha=0.5, bbox_to_anchor=(1, 0.2)
    plt.xlim(min_col_hb, max_col_hb)  #color
    plt.ylim(min_mag_hb, max_mag_hb)  #magnitude
    plt.gca().invert_yaxis() 
    plt.ylabel(dictfiltermagnames[0], labelpad=1, rotation='vertical')
    plt.xlabel(dictfiltermagnames[0] + ' - ' + dictfiltermagnames[1])
    plt.tight_layout()
    if save:
        plt.savefig(f'{save_plots_path}{clustername}_HB.pdf')
    plt.show()

    return IDHB
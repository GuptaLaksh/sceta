import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg for interactive window
import matplotlib.pyplot as plt
import importlib
from datetime import datetime
import pandas as pd
import tex
importlib.reload(tex)
import namingroutine
importlib.reload(namingroutine)
names = namingroutine.Initialize()

dictfilters = names['dictfilters']
dictfiltermagnames = names['dictfiltermagnames']
colors = names['colors']

def init(df, cnam, min_mag_hb_sel, max_mag_hb_sel, min_col_hb_sel, max_col_hb_sel):
    
    plt.close('all')  # Close any existing figures first
    
    fig, ax = plt.subplots(figsize=(5, 5))
    
    # Create scatter plot
    x_data = df['F275W'] - df['F336W']
    y_data = df['F275W']
    ax.scatter(x_data, y_data, marker='o', s=2, edgecolors='none', color='black')
    
    ax.set_xlim(min_col_hb_sel, max_col_hb_sel)  # color
    ax.set_ylim(min_mag_hb_sel, max_mag_hb_sel)  # magnitude
    ax.invert_yaxis()
    ax.set_ylabel(dictfiltermagnames[0], fontsize=20, labelpad=1, rotation='vertical')
    ax.set_xlabel(dictfiltermagnames[0] + ' - ' + dictfiltermagnames[1], fontsize=20)
    
    # Use ginput to interactively select points
    print("Click points on the plot. Press Enter or right-click when done.")
    selected_points = plt.ginput(n=-1, timeout=-1)
    
    plt.close(fig)
    
    # Save selected points to a file with today's date and time
    if selected_points:
        date_str = datetime.now().strftime('%m%d%y_%H%M')
        filename = f'{date_str}_{cnam}_Sel.txt'
        with open(filename, 'w') as f:
            for x, y in selected_points:
                f.write(f'{x:.6f} {y:.6f}\n')
        print(f'Selected points saved to {filename}')
    
    return selected_points

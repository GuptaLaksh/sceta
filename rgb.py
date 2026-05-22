from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import importlib
from scipy.interpolate import interp1d

import tex
importlib.reload(tex)

import namingroutine
importlib.reload(namingroutine)
names = namingroutine.Initialize()


def gaussian(x, amp, mean, sigma, const):
    return amp * np.exp(-((x - mean)**2) / (2 * sigma**2)) + const

def initialize(canonicalet, canonicaliso, df, save, save_plots_path, clustername, hb_id, maxcol, mincol, everynth, rgb_division, usewhich, col1_fil, col2_fil, mag_fil, sigma_cut):
    
    if usewhich == 'ET':
        usewhichmodel = canonicalet
    elif usewhich == 'Iso':
        usewhichmodel = canonicaliso
    
    # calculating time between 390 and rgb_division and rgb_division and 1189 to get the color limits for RGB selection.
    time_min = 10**usewhichmodel['log(age)'][390]
    time_max = 10**usewhichmodel['log(age)'][1189]
    idx = (usewhichmodel[mag_fil] - rgb_division).abs().idxmin()
    time_rgb_division = 10**usewhichmodel.loc[idx, 'log(age)']

    plt.rcParams['figure.dpi']=100
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 8), gridspec_kw={'width_ratios': [5, 2]})

    # LEFT PLOT: RGB Selection
    ax1.scatter(df[col1_fil] - df[col2_fil], df[mag_fil],
                marker = 'o', s=2, alpha=1, color='black', edgecolors='none', rasterized=True)

    maxmag = usewhichmodel[mag_fil][390]
    minmag = usewhichmodel[mag_fil][1189]
    print(f"Number of stars per bin: {everynth} - Set by me.\nSigma cut: {sigma_cut} - Set by me.\n")

    df_rgb_rough = df[(df[mag_fil] > minmag) & (df[mag_fil] < maxmag) & ((df[col1_fil] - df[col2_fil]) > mincol) & ((df[col1_fil] - df[col2_fil]) < maxcol)]

    mask = (df_rgb_rough['ID'].isin(hb_id))

    print(f"RGB rough selection: {len(df_rgb_rough)}")

    hb_in_rgb_sel = df_rgb_rough[mask]

    print(f"HB in RGB rough selection: {len(hb_in_rgb_sel)}")

    hb_in_rgb_sel_id = hb_in_rgb_sel['ID'].values

    ax1.plot(usewhichmodel[col1_fil] - usewhichmodel[col2_fil],
                usewhichmodel[mag_fil],
                color=names['colors'][0], lw=3, linestyle='-', markersize=0.1,
                marker='o', label='He-canonical Iso', rasterized=True)
    ax1.plot(canonicalet[col1_fil] - canonicalet[col2_fil],
                canonicalet[mag_fil],
                color=names['colors'][1], lw=3, linestyle='-', markersize=0.1,
                marker='o', label='He-canonical ET', rasterized=True)
    
    ax1.scatter(df_rgb_rough[col1_fil] - df_rgb_rough[col2_fil], df_rgb_rough[mag_fil],
                marker = 'o', s=2, alpha=1, color='red', edgecolors='none', label=f'Rough RGB Sel: {len(df_rgb_rough)} stars', rasterized=True)
    
    ax1.scatter(hb_in_rgb_sel[col1_fil] - hb_in_rgb_sel[col2_fil], hb_in_rgb_sel[mag_fil], marker='s', s=2, edgecolors='none', color='yellow', label=f'HB Stars in Rough RGB Sel: {len(hb_in_rgb_sel)}', rasterized=True)

    ax1.axhline(y=maxmag, color='green', linestyle='--', linewidth=1)
    ax1.axhline(y=minmag, color='green', linestyle='--', linewidth=1)
    ax1.axvline(x=mincol, color='orange', linestyle='--', linewidth=1)
    ax1.axvline(x=maxcol, color='orange', linestyle='--', linewidth=1)
    ax1.axvline(x=(usewhichmodel[col1_fil][390] - usewhichmodel[col2_fil][390]), color='green', linestyle='--', linewidth=1)
    ax1.axhline(y=rgb_division, color='orange', linestyle='--', linewidth=1)

    ax1.set_ylim(minmag-2, maxmag+2)
    ax1.set_xlim(mincol-0.5, maxcol+0.5)
    ax1.set_xticks([mincol, maxcol])
    ax1.set_yticks([minmag, maxmag, rgb_division])
    ax1.set_xlabel(f"$m_{{\\mathrm{{{col1_fil}}}}} - m_{{\\mathrm{{{col2_fil}}}}}$", fontsize=12)
    ax1.set_ylabel(f"$m_{{\\mathrm{{{mag_fil}}}}}$", fontsize=12)
    ax1.invert_yaxis()
    ax1.legend(fontsize=8)

    sorted_mags = np.sort(df_rgb_rough[mag_fil].values)  
    bins = sorted_mags[::everynth]  
    total_RGBs = 0
    df_rgb_straightened = []
    df_rgb_list = []  

    ref_color = usewhichmodel[col1_fil][390] - usewhichmodel[col2_fil][390]
    f_color = interp1d(usewhichmodel[mag_fil], usewhichmodel[col1_fil] - usewhichmodel[col2_fil], kind='linear', fill_value='extrapolate')

    if bins[-1] != sorted_mags[-1]:
        bins = np.append(bins, sorted_mags[-1])

    print(f"Number of bins {len(bins)-1}")
    for i in range(len(bins)-1):

        stars_in_bin = df_rgb_rough[(df_rgb_rough[mag_fil] >= bins[i]) & (df_rgb_rough[mag_fil] < bins[i+1])]

        mid_mag = (bins[i] + bins[i+1]) / 2
        color_mid_mag = f_color(mid_mag)

        color_diff = color_mid_mag - ref_color

        color_diff_stars = (stars_in_bin[col1_fil] - stars_in_bin[col2_fil]) - color_diff

        # print("Number of stars in this bin: ", len(stars_in_bin))
        total_RGBs = total_RGBs + len(stars_in_bin)
        ax2.scatter(color_diff_stars, stars_in_bin[mag_fil], marker='o', s=5, alpha=1, color='brown', edgecolors='none')
        
        df_bin = stars_in_bin.copy()
        df_bin['color_st'] = color_diff_stars
        df_bin['mag_st'] = stars_in_bin[mag_fil]
        
        df_rgb_list.append(df_bin)  # Append to list

    df_rgb_straightened = pd.concat(df_rgb_list, ignore_index=True)

    print(f"RGB stars straightened: {total_RGBs}.")

    df_rgb_hb_extracted = df_rgb_straightened[~df_rgb_straightened['ID'].isin(hb_in_rgb_sel_id)]

    print(f"RGB count after HB deletion: {len(df_rgb_hb_extracted)}")

    df_bottom = df_rgb_hb_extracted[df_rgb_hb_extracted['mag_st'] >= rgb_division]
    below_before_sigcut = len(df_bottom)

    mean_color_bottom = df_bottom['color_st'].mean()
    std_color_bottom = df_bottom['color_st'].std()
    lower_bound_bottom = mean_color_bottom - sigma_cut * std_color_bottom
    upper_bound_bottom = mean_color_bottom + sigma_cut * std_color_bottom

    df_bottom = df_bottom[(df_bottom['color_st'] >= lower_bound_bottom) & (df_bottom['color_st'] < upper_bound_bottom)]
    print(f"Below division: {below_before_sigcut}, {sigma_cut} sigma cut: {len(df_bottom)}, {(time_rgb_division - time_min)/(10**6):.2e} Myrs")

    df_upper = df_rgb_hb_extracted[df_rgb_hb_extracted['mag_st'] < rgb_division]
    above_before_sigcut = len(df_upper)
    mean_color_upper = df_upper['color_st'].mean()
    std_color_upper = df_upper['color_st'].std()
    lower_bound_upper = mean_color_upper - sigma_cut * std_color_upper
    upper_bound_upper = mean_color_upper + sigma_cut * std_color_upper
    df_upper = df_upper[(df_upper['color_st'] >= lower_bound_upper) & (df_upper['color_st'] < upper_bound_upper)]
    print(f"Above division: {above_before_sigcut}, {sigma_cut} sigma cut: {len(df_upper)}, {(time_max - time_rgb_division)/(10**6):.2e} Myrs")

    ax2.scatter(df_bottom['color_st'], df_bottom['mag_st'], marker='o', s=5, alpha=1, color='blue', edgecolors='none', label=f'RGB Bottom: {len(df_bottom)} stars', rasterized=True)
    ax2.scatter(df_upper['color_st'], df_upper['mag_st'], marker='o', s=5, alpha=1, color='green', edgecolors='none', label=f'RGB Upper: {len(df_upper)} stars', rasterized=True)

    ax2.set_ylim(minmag-2, maxmag+2)
    # ax2.set_xlim(mincol-0.5, maxcol+0.5)
    ax2.set_xlabel(f"$m_{{\\mathrm{{{col1_fil}}}}} - m_{{\\mathrm{{{col2_fil}}}}}$", fontsize=12)
    ax2.set_yticks([])  # Hide y-axis ticks
    # ax2.set_ylabel(f"{mag_fil}", fontsize=12)
    ax2.invert_yaxis()
    # ax2.set_title('Straightened RGB Stars', fontsize=12)
    # ax2.legend(fontsize=10)

    fig.tight_layout()
    # plt.savefig(f'/Users/lakshgupta/Downloads/Personal/P-NGC2808WD/All Clusters Analysis/Paper 2/RGB_Analysis.pdf', dpi=300)

    if save:
        fig.savefig(f'{save_plots_path}{clustername}_RGB.pdf')
    
    plt.show()
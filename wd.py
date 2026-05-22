import importlib
import pandas as pd
import numpy as np
import func_analysis
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

import tex
importlib.reload(tex)

import namingroutine
importlib.reload(namingroutine)
names = namingroutine.Initialize()

markersize_set = 'o'

def WDCrossingTime(dataiwishtosee, lowermag):
    # column_name = 'log(t)'
    # row_number_1 = (abs(dataiwishtosee['F275W'] - uppermag)).abs().idxmin()
    # row_number_2 = (abs(dataiwishtosee['F275W'] - lowermag)).abs().idxmin()

    # t1 = dataiwishtosee.loc[row_number_1, column_name]
    # t2 = dataiwishtosee.loc[row_number_2, column_name]

    # columns_of_interest = ['F275W', 'F336W', 'F438W']

    # combined_data = dataiwishtosee.loc[row_number_1, columns_of_interest].tolist() + dataiwishtosee.loc[row_number_2, columns_of_interest].tolist()

    # lifetimewd = ((10**(t2) - 10**(t1))/(10**6))
    # lifetimewd = round(lifetimewd, 3)
    # return lifetimewd, combined_data

    column_name = 'log(t)'
    # row_number_1 = (abs(dataiwishtosee['F275W'] - uppermag)).abs().idxmin()
    row_number_2 = (abs(dataiwishtosee['F275W'] - lowermag)).abs().idxmin()

    # t1 = dataiwishtosee.loc[row_number_1, column_name]
    t2 = dataiwishtosee.loc[row_number_2, column_name]

    columns_of_interest = ['F275W', 'F336W', 'F438W']

    combined_data = dataiwishtosee.loc[row_number_2, columns_of_interest].tolist()
    # combined_data = "nothing"

    lifetimewd = ((10**(t2))/(10**6))
    lifetimewd = round(lifetimewd, 3)
    return lifetimewd, combined_data

def WDLFNew(dfWDCounts):
    tobeprintedcorr = dfWDCounts['Combined Count Compl'].sum()
    dfWDCounts['bin_edges']  = dfWDCounts['Bin Center']
    dfWDCounts['cumulative_counts_ncorrsum'] = dfWDCounts['Combined Count Compl'].cumsum()
    dfWDCounts['cumulative_counts_ncorrsum_norm'] = (dfWDCounts['cumulative_counts_ncorrsum'])/(tobeprintedcorr)
    
    dfWDCounts['error terms_num'] = dfWDCounts['cumulative_counts_ncorrsum'] + (dfWDCounts['cumulative_counts_ncorrsum'].sum())
    dfWDCounts['error terms_den'] = dfWDCounts['cumulative_counts_ncorrsum']*(dfWDCounts['cumulative_counts_ncorrsum'].sum())
    
    # dfWDCounts['error terms_num'] = dfWDCounts['Combined Count Compl'] + (dfWDCounts['Combined Count Compl'].sum())
    # dfWDCounts['error terms_den'] = dfWDCounts['Combined Count Compl']*(dfWDCounts['Combined Count Compl'].sum())
    dfWDCounts['error term'] = np.sqrt((dfWDCounts['error terms_num'])/(dfWDCounts['error terms_den']))
    dfWDCounts['error_cum_counts_norm'] = dfWDCounts['cumulative_counts_ncorrsum_norm']*dfWDCounts['error term']
    return dfWDCounts, tobeprintedcorr

def initialize(merged_df, 
               wdmodel, clustername, save_plots_path, save,
               max_allowed_mag, min_allowed_mag, 
               binsize, 
               division,
               min_mag, max_mag, min_col, max2,
               wdcolmin, wdcolmax, wdcolminbri, wdcolmaxbri,
               briwdstart,
               wantlegend, Completeness):

    print("WD Analysis being run for " + str(clustername) +".")

    dictfilters = names['dictfilters']
    dictwdmasses = names['dictwdmasses']

    a = 1

    plt.figure(figsize=(10,8))
    plt.subplots_adjust(wspace = 0.2)

    i = 0
    j = 1

    f1 = dictfilters[i]
    f2 = dictfilters[j]

    y2 = merged_df['F' + f1 +'W'] 
    x2 = merged_df['F' + f1 +'W'] - merged_df['F' + f2 +'W']

    holdthese = {'y2': y2, 'x2': x2, 'ID': merged_df['ID']}
    dfplot = pd.DataFrame(holdthese)

    # selecting WDs internal

    dfwdcal = dfplot
    dfwdcalbright = dfplot

    dfwdcal = dfwdcal[dfwdcal['y2'] <= max_allowed_mag]
    dfwdcal = dfwdcal[dfwdcal['y2'] >= min_allowed_mag]
    dfwdcal = dfwdcal[dfwdcal['x2'] >= wdcolmin]
    dfwdcal = dfwdcal[dfwdcal['x2'] <= wdcolmax]
    print("For the potential WDs, the color selection: " + str(wdcolmin) + " to " + str(wdcolmax))

    dfwdcalbright = dfwdcalbright[dfwdcalbright['y2'] <= min_allowed_mag]
    dfwdcalbright = dfwdcalbright[dfwdcalbright['y2'] >= briwdstart]
    dfwdcalbright = dfwdcalbright[dfwdcalbright['x2'] <= wdcolminbri]
    dfwdcalbright = dfwdcalbright[dfwdcalbright['x2'] >= wdcolmaxbri] 
    print("For the ``bright'' WDs, the color selection: " + str(wdcolminbri) + " to " + str(wdcolmaxbri))
    print("Bright WDs start from: " + str(briwdstart))
    dflf336intbri, bins, hist = func_analysis.CreatingHistograms(dfwdcalbright['y2'], min_allowed_mag, binsize)
    dflf336int, bins, hist = func_analysis.CreatingHistograms(dfwdcal['y2'], min_allowed_mag, binsize)

    completenessholder = []

    if Completeness:
        for abc in range(0, len(dflf336int['Bin Lower'])):
            complcorrected_values = CompCor(bins[abc], bins[abc + 1], hist[abc], 6)
            completenessholder.append(round(complcorrected_values, 3))
        dflf336int['Count Compl'] = completenessholder
    else:
        print("No completeness function was read. `0+0=0' below denotes that there are no completeness corrected counts.")
        dflf336int['Count Compl'] = 0

    # Plotting now

    plt.subplot(1,2,a)

    plt.scatter(dfplot['x2'], dfplot['y2'], marker = markersize_set, s=10, edgecolors='none', color='black', label = str(len(dfplot)), rasterized=True)
    plt.scatter(dfwdcalbright['x2'], dfwdcalbright['y2'], marker = '*', s=100, edgecolors='none', color='teal', label = str(len(dfwdcalbright['y2'])) + ' "Bright"', rasterized=True)

    # division = np.float64(division)
    plt.axhline(y=division, color='red', linestyle='--', linewidth=2, label = str(division), rasterized=True)
    plt.axhline(y=max_allowed_mag, color='red', linestyle='--', linewidth=2, label = str(max_allowed_mag), rasterized=True)

    bin1 = pd.DataFrame()
    bin2 = pd.DataFrame()
    bin1 = dfwdcal[dfwdcal['y2'] <= division]
    bin2 = dfwdcal[dfwdcal['y2'] > division]
    plt.scatter(bin1['x2'], bin1['y2'], marker = '^', s=100, edgecolors='none', color='dodgerblue', label = str(len(bin1)) + ' Upper', rasterized=True)
    plt.scatter(bin2['x2'], bin2['y2'], marker = '^', s=100, edgecolors='none', color='red', label = str(len(bin2)) + ' Lower', rasterized=True)

    # Plotting WD Cooling Models

    wdlifetimecomb, pointscomb = WDCrossingTime(wdmodel, division)
    plt.scatter((pointscomb[0] - pointscomb[1]), pointscomb[0], marker = '^', s=500, edgecolors='none', color='black', label = wdlifetimecomb, zorder = 3, rasterized=True)
    print('Upper lifetime - ' + str(wdlifetimecomb) + " Myrs")
    WDCTup = wdlifetimecomb

    wdlifetimecomb, pointscomb = WDCrossingTime(wdmodel, max_allowed_mag)
    plt.scatter((pointscomb[0] - pointscomb[1]), pointscomb[0], marker = '^', s=500, edgecolors='none', color='black', label = wdlifetimecomb, zorder = 3, rasterized=True)
    print('Lower lifetime - ' + str(wdlifetimecomb) + " Myrs")
    WDCTlo = wdlifetimecomb

    plt.plot((wdmodel['F' + f1 + 'W'] - wdmodel['F' + f2 + 'W']), (wdmodel['F' + f1 + 'W']), marker = markersize_set, markersize=0.1, linestyle='-', markeredgecolor='none', lw = 4, c ='hotpink', label = 'CO/H (' + dictwdmasses[0] + ' \(M_\odot\))', rasterized=True) #  + ' INT - ' + str(wdlifetimeintCOH) + ' EXT - ' + str(wdlifetimeextCOH)

    if wantlegend:
        plt.legend(fontsize=15, loc = 'upper left')
    
    plt.xlim(min_col, max2)  #color
    plt.ylim(min_mag, max_mag)  #magnitude
    plt.gca().invert_yaxis() 
    plt.ylabel("\(m_{F275W} \)", fontsize = 20, labelpad=1)
    plt.xlabel("\( m_{F275W} - m_{F336W} \)", fontsize = 20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20) 
    a = a + 1    

    # Observed White Dwarf Luminosity Functions 
    row_index = round(((division-min_allowed_mag)/binsize)-1, 0)
    # print(row_index)
    sum_values_upper_ncorr = round(dflf336int.loc[0:row_index, 'NCount Compl'].sum(), 1)
    sum_values_lower_ncorr = round(dflf336int.loc[row_index+1:, 'NCount Compl'].sum(), 1)
    sum_values_upper_corr = round(dflf336int.loc[0:row_index, 'Count Compl'].sum(), 1)
    sum_values_lower_corr = round(dflf336int.loc[row_index+1:, 'Count Compl'].sum(), 1)
    # print(sum_values_lower_corr)

    plt.subplot(1,2,a)

    bin_centers = (dflf336int['Bin Lower'] + dflf336int['Bin Upper']) / 2
    plt.step(bin_centers, dflf336int['NCount Compl'], linestyle = '-', linewidth = 3,  marker='o', markersize = 3, color = 'teal', label = str(sum_values_upper_ncorr) + '+' + str (sum_values_lower_ncorr) + '=' + str(round(sum_values_upper_ncorr + sum_values_lower_ncorr, 1)), rasterized=True)
    plt.step(bin_centers, dflf336int['Count Compl'], linestyle = '-', linewidth = 3,  marker='o', markersize = 3, color = 'crimson', label = str(sum_values_upper_corr) + '+' + str (sum_values_lower_corr) + '=' + str(round(sum_values_upper_corr + sum_values_lower_corr, 1)), rasterized=True)
    # print(dflf336int)

    plt.legend(loc='upper left', fontsize=15)
    plt.xlabel('\( m_{F275W} \)', fontsize = 20)
    plt.ylabel('Number of WDs', fontsize = 20)
    plt.yticks(fontsize=20) 
    plt.xticks(fontsize=20)
    a = a + 1

    # Printing Normalized WDLFs

    if Completeness:

        merged_df = pd.merge(dflf336int, dflf336intbri, on='Bin Center', how='outer')
        merged_df = merged_df.fillna(0).astype(float)
        # print(merged_df)
        merged_df['Combined Count Compl'] = merged_df['Count Compl'] + merged_df['NCount Compl_y']
        columns_to_keep = ['Bin Center', 'Combined Count Compl']
        df_selected = merged_df[columns_to_keep]
        concatnew36finalWDcountONLYINT = df_selected
        print(concatnew36finalWDcountONLYINT)

        plt.subplot(1,2,a)

        titlestore = 'INT Observed'
        dfWDCounts = concatnew36finalWDcountONLYINT
        dfWDCounts, tobeprintedcorr = WDLFNew(dfWDCounts)
        cumulative_counts_ncorr_norm = dfWDCounts['cumulative_counts_ncorrsum_norm']
        bin_edges = dfWDCounts['bin_edges']
        error_norm_counts = dfWDCounts['error_cum_counts_norm']
        # plt.step(bin_edges[:], cumulative_counts_ncorr_norm[:], where='mid', color='dodgerblue', linestyle='-.', label = titlestore + ' - ' + str(round(tobeprintedcorr, 0)))
        plt.step(bin_edges[:], cumulative_counts_ncorr_norm[:], where='mid', color='dodgerblue', linestyle='-.', label = titlestore, rasterized=True)
        plt.errorbar(bin_edges[:], cumulative_counts_ncorr_norm[:], yerr=error_norm_counts[:], fmt='o', color='red', capsize = 0.5, label='Error Bars', rasterized=True)
        plt.ylabel('Normalized Number of WDs', fontsize = 20)
        plt.xlabel('\( m_{F275W} \)', fontsize = 20)
        plt.xticks(fontsize = 20)
        plt.yticks(fontsize = 20)
        plt.xlim(21.3, 26)
        # plt.legend(fontsize = 15, loc = 'lower right')
        formatter = FuncFormatter(lambda x, pos: f'{x:.0f}')
        plt.gca().xaxis.set_major_formatter(formatter)
        a = a + 2

    plt.tight_layout()
    if save:
        plt.savefig(f'{save_plots_path}{clustername}_WD.pdf')
    plt.show()

    return locals()

import tex
import importlib
import pandas as pd
import numpy as np
from shapely.geometry import Polygon, Point
import matplotlib.pyplot as plt

import func_other

import namingroutine
importlib.reload(namingroutine)
names = namingroutine.Initialize()

markersize_set = 'o'

def initialize(df1,
               keyiso, keyet, key3_st, key4_st,
               c_iso, c_et, a_et1, a_et2, 
               clustername, wantabund, Completeness, save_plots_path,
               delalpholder,
               g,
               bluelimit, redlimit, sigmacut,
               wantcsv, wantlegend, save):
    
    print("MSTO Analysis being run for " + str(clustername) +".")

    dictfilters = names['dictfilters']
    dictfiltermagnames = names['dictfiltermagnames']

    def MSTOCrossingTime(bluestIsochronepointRow, et, f1, f2, f3, uppermagupper, lowermagupper, lowermaglower, df_part1, leftcol, rightcol, timecolstring):

        dataframeusingevoltrack = et
        # print(dataframeusingevoltrack)
        
        y1 = dataframeusingevoltrack['F' + f3 + 'W'] 
        x1 = dataframeusingevoltrack['F' + f1 + 'W'] - dataframeusingevoltrack['F' + f2 + 'W']
        lifetime = dataframeusingevoltrack[timecolstring]
        result3 = pd.concat([y1, x1, lifetime], axis=1) # made a df called result with 2 cols x2 and y2 
        
        dfusing = result3[(result3.iloc[:,1] >= (df_part1.iloc[:, 0].iloc[-1] - leftcol)) & (result3.iloc[:,1] <= (df_part1.iloc[:, 0].iloc[-1] + rightcol)) & (result3.iloc[:,0] >= (bluestIsochronepointRow[0]-0.5)) & (result3.iloc[:,0] <= (bluestIsochronepointRow[0]+0.5))]
        # print(df_part1.iloc[:, 0].iloc[-1])
        # print(dfusing) 

        nearest_value_min = (dfusing.iloc[:, 0] - uppermagupper).abs().idxmin()
        nearest_value_center = (dfusing.iloc[:, 0] - lowermagupper).abs().idxmin()
        nearest_value_max = (dfusing.iloc[:, 0] - lowermaglower).abs().idxmin()   

        rowstobekept = dataframeusingevoltrack.index.get_indexer([nearest_value_min, nearest_value_center, nearest_value_max])
        dfworth = dataframeusingevoltrack.iloc[rowstobekept]

        # rowstobekept = [nearest_value_min, nearest_value_center, nearest_value_max]
        # dfworth = dataframeusingevoltrack.iloc[rowstobekept]

        value1 = float(dfworth.iloc[1, 0])
        value2 = float(dfworth.iloc[0, 0])
        value3 = float(dfworth.iloc[2, 0])

        brightestpointmag = dataframeusingevoltrack.loc[nearest_value_min, 'F' + f3 + 'W']
        brightestpointcol = dataframeusingevoltrack.loc[nearest_value_min, 'F' + f1 + 'W'] - dataframeusingevoltrack.loc[nearest_value_min, 'F' + f2 + 'W']

        faintestpointmag = dataframeusingevoltrack.loc[nearest_value_max, 'F' + f3 + 'W']
        faintestpointcol = dataframeusingevoltrack.loc[nearest_value_max, 'F' + f1 + 'W'] - dataframeusingevoltrack.loc[nearest_value_max, 'F' + f2 + 'W']

        centerpointmag = dataframeusingevoltrack.loc[nearest_value_center, 'F' + f3 + 'W']
        centerpointcol = dataframeusingevoltrack.loc[nearest_value_center, 'F' + f1 + 'W'] - dataframeusingevoltrack.loc[nearest_value_center, 'F' + f2 + 'W']    

        return round(((10**value3 - 10**value1) / (10**6)), 2), round(((10**value1 - 10**value2) / (10**6)), 2), brightestpointmag, brightestpointcol, faintestpointmag, faintestpointcol, centerpointmag, centerpointcol

    def GivenRectanglePoints(x2, y2, IDs, parallelogram_vertices):
        parallelogram_shapely = Polygon(parallelogram_vertices)
        result4 = pd.concat([x2, y2, IDs], axis=1) # made a df called result with 2 cols x2 and y2 
        mask = result4.apply(lambda row: Point(row.iloc[0], row.iloc[1]).within(parallelogram_shapely), axis=1)
        points_inside_parallelogram = result4[mask]

        return points_inside_parallelogram.iloc[:,0], points_inside_parallelogram.iloc[:,1], points_inside_parallelogram.iloc[:,2]

    # OLD BaSTI Models
    whichmass = '(M/Mo)' # '(M/Mo)in'
    timecolstring = 'log(age)'

    dfstoringcsv = pd.DataFrame()
    dfstoringcsvfinal = pd.DataFrame()

    if wantcsv:
        plots = False
    else:
        plots = True

    colorsheabund = {0: 'red', 1: 'gray'}

    for delalp in range (0, len(delalpholder)):
        deltaalpha = round(delalpholder[delalp], 6)
        # print("------------------------------")
        print("delta M = " + str(deltaalpha) + ". Following numbers are for this.")
        colorthis = 'black'

        a = 1
        h = 2
        w = 2

        i = 0
        j = 1
        k = 0

        f1 = dictfilters[0]
        f2 = dictfilters[1]
        f3 = dictfilters[0]

        x2 = df1['F' + f1 +'W'] - df1['F' + f2 +'W']
        y2 = df1['F' + f3 +'W'] 
        IDs = df1['ID']

        concatnew = pd.concat([y2, x2], axis=1)
        concatnew.columns = ['y2', 'x2']    

        # print(c_iso)
        row_number_of_maximum = np.argmax(c_iso['logTe'])
        value_at_nth_entry = c_iso[whichmass].iloc[row_number_of_maximum]
        result = pd.concat([c_iso[whichmass], c_iso['F275W'], c_iso['F336W'], c_iso['logTe']], axis=1) # made a df called result with 2 cols x2 and y2 
        
        # df with isochrone points within delta alpha
        dfusingisoini = result[(result.iloc[:,0] > (value_at_nth_entry - deltaalpha)) & (result.iloc[:,0] < (value_at_nth_entry + deltaalpha))]

        max_logTe_row = c_iso.iloc[(c_iso['logTe'].idxmax()), :]
        selected_columns = ['F275W', 'F336W', 'logTe']
        bluestIsochronepointRow = max_logTe_row[selected_columns]
        teff = bluestIsochronepointRow[2]

        min_mag = bluestIsochronepointRow[0] - 0.85
        max_mag = bluestIsochronepointRow[0] + 0.85
        min_col = bluestIsochronepointRow[0] - bluestIsochronepointRow[1] - 0.25
        max2 = bluestIsochronepointRow[0] - bluestIsochronepointRow[1] + 0.35

        # if plots:
            
        #     plt.tight_layout()
        #     plt.rcParams['figure.dpi']=dpi
        #     fig = plt.figure(figsize=(10, 10)) 
        #     plt.subplots_adjust(wspace = 0.20)

        #     plt.subplot(h,w,a)
        #     plt.scatter(x2, y2, marker = markersize_set, s=15, edgecolors='none', color=colorthis, alpha = 0.15)
        #     plt.plot(c_iso['F275W'] - c_iso['F336W'], c_iso['F275W'], color = 'dodgerblue', lw = 5, linestyle = '-', markersize = 0.1, marker = markersize_set)
        #     plt.scatter(dfusingisoini['F275W'] - dfusingisoini['F336W'], dfusingisoini['F275W'], marker = markersize_set, s=200, edgecolors='none', color='dodgerblue', label = 'Isoch. Age: ' + str(keyiso) + " Myr")
        #     plt.scatter(bluestIsochronepointRow[0] - bluestIsochronepointRow[1], bluestIsochronepointRow[0], marker = '*', s = 500, edgecolors='black', color='gold', label = "Theoritical MSTO", zorder = 3)
        #     plt.xlim(min_col, max2)  #color
        #     plt.ylim(min_mag, max_mag)  #magnitude
        #     plt.xticks(fontsize=10)
        #     plt.yticks(fontsize=10) 
        #     plt.gca().invert_yaxis()
        #     if wantlegend:
        #         plt.legend(fontsize = 10)
        #     plt.ylabel(dictfiltermagnames[k], fontsize=10, labelpad=1)
        #     plt.xlabel(dictfiltermagnames[i] + ' - ' + dictfiltermagnames[j], fontsize=10) 
        #     # plt.show()
        #     a = a + 1

        # rough selection of MSTO stars (in color)
        # - first bifurcate to get points
        # - then 2sig

        result1 = pd.concat(((dfusingisoini['F' + f1 +'W'] - dfusingisoini['F' + f2 +'W']), dfusingisoini['F' + f3 +'W']), axis=1)
        result1.sort_values(by=result1.columns[1], ascending=True, inplace=True)
        matching_rows = result1.loc[result1.iloc[:, 1] == bluestIsochronepointRow.iloc[0]].index
        
        df_part1 = result1.loc[:matching_rows[0]]
        df_part2 = result1.loc[matching_rows[0]:]

        # upper bin
        uppermagupper = df_part1.iloc[:, 1].iloc[0] 
        lowermagupper = df_part1.iloc[:, 1].iloc[-1]
        uppercolupper = df_part1.iloc[:, 0].iloc[-1] 
        lowercolupper = df_part1.iloc[:, 0].iloc[-1] 
        parallelogram_vertices1 = [(lowercolupper, uppermagupper), (lowercolupper, lowermagupper), (uppercolupper, lowermagupper), (uppercolupper, uppermagupper)]
        # print(parallelogram_vertices1)

        # lower bin
        uppermaglower = df_part2.iloc[:, 1].iloc[0] 
        lowermaglower = df_part2.iloc[:, 1].iloc[-1] 
        uppercollower = df_part2.iloc[:, 0].iloc[0] 
        lowercollower = df_part2.iloc[:, 0].iloc[0] 
        parallelogram_vertices2 = [(lowercollower, uppermaglower), (lowercollower, lowermaglower), (uppercollower, lowermaglower), (uppercollower, uppermaglower)]
        # print(parallelogram_vertices2)

        concatnew = concatnew[concatnew['y2'] >= uppermagupper]
        concatnew = concatnew[concatnew['y2'] <= lowermaglower]
        concatnew = concatnew[concatnew['x2'] <= redlimit]
        concatnew = concatnew[concatnew['x2'] >= bluelimit]

        # histogram 

        data = concatnew['x2']
        # print(str(len(data)))
        hist, bin_edges = np.histogram(concatnew['x2'], bins=50)  
        highest_peak_index = np.argmax(hist)
        peak_value = (bin_edges[highest_peak_index] + bin_edges[highest_peak_index + 1]) / 2
        first_mode_values = concatnew['x2'] 
        mean_first_mode = np.mean(first_mode_values)
        std_dev_first_mode = np.std(first_mode_values)
        plus_3_sigma = mean_first_mode + (sigmacut * std_dev_first_mode)
        minus_3_sigma = mean_first_mode - (sigmacut * std_dev_first_mode)

        leftcol = minus_3_sigma
        rightcol = plus_3_sigma

        print(leftcol, rightcol)
        # print(rightcol)

        if (leftcol<(concatnew['x2'].min())):
            leftcol = concatnew['x2'].min()
        
        if (rightcol>(concatnew['x2'].max())):
            rightcol = concatnew['x2'].max()

        print(leftcol, rightcol)
        # print(rightcol)
        print("If the two pairs above are identical then the bluelimit, redlimit and sigmacut are correctly set.")

        # upper bin
        uppermagupper = df_part1.iloc[:, 1].iloc[0] 
        lowermagupper = df_part1.iloc[:, 1].iloc[-1]
        uppercolupper = df_part1.iloc[:, 0].iloc[-1] + rightcol
        lowercolupper = df_part1.iloc[:, 0].iloc[-1] - leftcol
        parallelogram_vertices1 = [(lowercolupper, uppermagupper), (lowercolupper, lowermagupper), (uppercolupper, lowermagupper), (uppercolupper, uppermagupper)]

        # lower bin
        uppermaglower = df_part2.iloc[:, 1].iloc[0] 
        lowermaglower = df_part2.iloc[:, 1].iloc[-1] 
        uppercollower = df_part2.iloc[:, 0].iloc[0] + rightcol
        lowercollower = df_part2.iloc[:, 0].iloc[0] - leftcol
        parallelogram_vertices2 = [(lowercollower, uppermaglower), (lowercollower, lowermaglower), (uppercollower, lowermaglower), (uppercollower, uppermaglower)]
        
        x3, y3, IDsUpper = GivenRectanglePoints(x2, y2, IDs, parallelogram_vertices1) # 1st rectangle
        x4, y4, IDsLower = GivenRectanglePoints(x2, y2, IDs, parallelogram_vertices2) # 2nd rectangle

        print("Magnitude Range: " + (str(round(uppermagupper, 3)) + ' - ' + str(round(lowermaglower, 3))) + " = " + str(abs(round(uppermagupper - lowermaglower, 3))) + " and Color Range: " + (str(round(uppercolupper, 3)) + ' - ' + str(round(lowercollower, 3))) + " = " + (str(abs(round(uppercolupper - lowercollower, 3)))))

        if plots:
            plt.figure(figsize=(25, 20), dpi=100) 
            plt.subplots_adjust(wspace = 0.20)

            plt.subplot(h,w,a)
            plt.scatter(x2, y2, marker = markersize_set, s=15, edgecolors='none', color=colorthis, alpha = 0.15, rasterized=True)
            plt.scatter(concatnew['x2'], concatnew['y2'], marker = markersize_set, s=40, edgecolors='none', color='darkgreen', label = "Rough MSTO sel", rasterized=True)
            print("Rough MSTO Selection Star Count (in darkgreen): " + str(len(concatnew)))
            plt.plot(c_iso['F275W'] - c_iso['F336W'], c_iso['F275W'], color = 'dodgerblue', lw = 5, linestyle = '-', markersize = 0.1, marker = markersize_set, rasterized=True)
            plt.scatter(dfusingisoini['F275W'] - dfusingisoini['F336W'], dfusingisoini['F275W'], marker = markersize_set, s=200, edgecolors='none', color='dodgerblue', label = "Isochr. Age: " + str(keyiso) + " Myrs", rasterized=True)
            plt.scatter(bluestIsochronepointRow[0] - bluestIsochronepointRow[1], bluestIsochronepointRow[0], marker = '*', s = 500, edgecolors='black', color='gold', label = "Theoritical MSTO", zorder = 3, rasterized=True)
            print("T-MSTO point: " + str(round(bluestIsochronepointRow[0] - bluestIsochronepointRow[1], 2)) + ', ' + str(round(bluestIsochronepointRow[0], 2)))
            plt.xlim(min_col, max2)  #color
            plt.ylim(min_mag, max_mag)  #magnitude
            plt.xticks(fontsize=30)
            plt.yticks(fontsize=30) 
            plt.gca().invert_yaxis()
            if wantlegend:
                plt.legend(fontsize = 30)
            plt.ylabel(dictfiltermagnames[k], fontsize=30, labelpad=1)
            plt.xlabel(dictfiltermagnames[i] + ' - ' + dictfiltermagnames[j], fontsize=30) 
            a = a + 1

        if plots:
            plt.subplot(h,w,a)
            plt.hist(concatnew['x2'], bins=50, color='blue', edgecolor='black', rasterized=True)
            plt.hist(first_mode_values, bins=50, color='pink', edgecolor='black', rasterized=True)
            plt.axvline(x=plus_3_sigma, color='red', linestyle='--')
            plt.axvline(x=minus_3_sigma, color='red', linestyle='--')
            plt.axvline(x=leftcol, color='dodgerblue', linestyle='--')
            plt.axvline(x=rightcol, color='dodgerblue', linestyle='--')
            plt.xticks(fontsize=30)
            plt.yticks(fontsize=30) 
            plt.xlabel(dictfiltermagnames[i] + ' - ' + dictfiltermagnames[j], fontsize=30) 
            plt.ylabel('Number of Stars', fontsize=30)
            a = a + 1

        # cleaned MSTO stars in the two bins

        concatnewupper = pd.concat([y3, x3, IDsUpper], axis=1)
        concatnewupper.columns = ['y3', 'x3', 'ID']
        concatnewupper = concatnewupper[concatnewupper['x3'] >= leftcol]
        concatnewupper = concatnewupper[concatnewupper['x3'] <= rightcol]

        concatnewlower = pd.concat([y4, x4, IDsLower], axis=1)
        concatnewlower.columns = ['y4', 'x4', 'ID']
        concatnewlower = concatnewlower[concatnewlower['x4'] >= leftcol]
        concatnewlower = concatnewlower[concatnewlower['x4'] <= rightcol]

        # running this here to get points for CompCor
        lowbin, highbin, brightestpointmag, brightestpointcol, faintestpointmag, faintestpointcol, centerpointmag, centerpointcol = MSTOCrossingTime(bluestIsochronepointRow, c_et, f1, f2, f3, uppermagupper, lowermagupper, lowermaglower, df_part1, leftcol, rightcol, timecolstring) # finding lifetime ratios
        
        # print(len(forspatialplotUpperMS))
        # print(len(forspatialplotLowerMS))

        if Completeness:
            print("Following include completeness corrected counts.")
            # finalcountupper = CompCor((abs(round(brightestpointmag, 2))), (abs(round(centerpointmag, 2))), (len(concatnewupper['x3'])), 0)
            # finalcountlower = CompCor((abs(round(faintestpointmag, 2))), (abs(round(centerpointmag, 2))), (len(concatnewlower['x4'])), 0)
        else:
            print("Following counts are not completeness corrected (indicated as '0' below).")
            finalcountupper = 000
            finalcountlower = 000

        if plots:
            plt.subplot(h,w,a)
            plt.scatter(x2, y2, marker = markersize_set, s=15, edgecolors='none', color=colorthis, alpha = 0.15)
            plt.scatter(concatnew['x2'], concatnew['y2'], marker = markersize_set, s=40, edgecolors='none', color='darkgreen')
            # printing the parallelogram
            plt.scatter(concatnewupper['x3'], concatnewupper['y3'], marker = '*', s=250, edgecolors='none', color='deeppink', label = str(len(concatnewupper)) + ' / ' + str(finalcountupper), rasterized=True)
            plt.scatter(concatnewlower['x4'], concatnewlower['y4'], marker = '*', s=250, edgecolors='none', color='indigo', label = str(len(concatnewlower)) + ' / ' + str(finalcountlower), rasterized=True)
            plt.plot(c_iso['F275W'] - c_iso['F336W'], c_iso['F275W'], color = 'dodgerblue', lw = 5, linestyle = '-', markersize = 0.1, marker = markersize_set, rasterized=True)
            plt.scatter(dfusingisoini['F275W'] - dfusingisoini['F336W'], dfusingisoini['F275W'], marker = markersize_set, s=200, edgecolors='none', color='dodgerblue', rasterized=True)
            plt.scatter(bluestIsochronepointRow[0] - bluestIsochronepointRow[1], bluestIsochronepointRow[0], marker = '*', s = 500, edgecolors='black', color='gold', zorder = 3, rasterized=True)
            plt.xlim(min_col, max2)  #color
            plt.ylim(min_mag, max_mag)  #magnitude
            plt.xticks(fontsize=30)
            plt.yticks(fontsize=30) 
            plt.gca().invert_yaxis()
            plt.ylabel(dictfiltermagnames[k], fontsize=30, labelpad=1)
            plt.xlabel(dictfiltermagnames[i] + ' - ' + dictfiltermagnames[j], fontsize=30) 
            a = a + 1

        if plots:

            min_mag += 0.55
            max_mag -= 0.55
            min_col -= 0.1
            max2 += 0.2

            plt.subplot(h,w,a)
            plt.scatter(x2, y2, marker = markersize_set, s=15, edgecolors='none', color=colorthis, alpha = 0.15, rasterized=True)

            plt.plot(c_iso['F275W'] - c_iso['F336W'], c_iso['F275W'], color = 'dodgerblue', lw = 5, linestyle = '-', markersize = 0.1, marker = markersize_set, rasterized=True)
            plt.scatter(dfusingisoini['F275W'] - dfusingisoini['F336W'], dfusingisoini['F275W'], marker = markersize_set, s=200, edgecolors='none', color='dodgerblue', rasterized=True)
            plt.scatter(bluestIsochronepointRow[0] - bluestIsochronepointRow[1], bluestIsochronepointRow[0], marker = '*', s = 500, edgecolors='black', color='gold', zorder = 3, rasterized=True)
            plt.plot(c_et['F275W'] - c_et['F336W'], c_et['F275W'], marker = markersize_set, markersize=0.1, linestyle = '-', lw = 5, color='orange', label = 'ET of .' + str(keyet) + ' \(M_\odot\)', rasterized=True)
            
            plt.scatter(concatnewupper['x3'], concatnewupper['y3'], marker = '*', s=250, edgecolors='none', color='deeppink', label = str(len(concatnewupper)) + ' / ' + str(finalcountupper) + " Upper Bin [LF - " + str(abs(highbin)) + "]", rasterized=True)
            plt.scatter(concatnewlower['x4'], concatnewlower['y4'], marker = '*', s=250, edgecolors='none', color='indigo', label = str(len(concatnewlower)) + ' / ' + str(finalcountlower) + " Lower Bin [LF - " + str(abs(lowbin)) + "]", rasterized=True)
            
            MSSC_c = concatnewupper + concatnewlower
            MSSC_c_comp = finalcountupper + finalcountlower 
            MSCT_c = highbin + lowbin

            print("SC/CT (He-Can): UB (pink): (" + str(len(concatnewupper)) + ', ' + str(finalcountupper) + ') / ' + str(abs(highbin)) + ", LB (purple): (" + str(len(concatnewlower)) + ', ' + str(finalcountlower) + ') / ' + str(abs(lowbin)))

            print("Total: " + str(len(MSSC_c)) + '/' + str(abs(MSCT_c)))
            if Completeness:
                print("Total CompCorr: " + str(len(MSSC_c_comp)) + '/' + str(abs(MSCT_c)))

            plt.scatter(brightestpointcol, brightestpointmag, marker = '^', s=500, edgecolors='none', color='black', zorder = 3, rasterized=True)
            plt.scatter(faintestpointcol, faintestpointmag, marker = '^', s=500, edgecolors='none', color='black', zorder = 3, rasterized=True)
            plt.scatter(centerpointcol, centerpointmag, marker = '^', s=500, edgecolors='none', color='black', zorder = 3, rasterized=True)

            plt.xlim(min_col, max2)  #color
            plt.ylim(min_mag, max_mag)  #magnitude
            plt.xticks(fontsize=30)
            plt.yticks(fontsize=30) 
            plt.gca().invert_yaxis()
            plt.ylabel(dictfiltermagnames[k], fontsize=30, labelpad=1)
            plt.xlabel(dictfiltermagnames[i] + ' - ' + dictfiltermagnames[j], fontsize=30) 
            a = a + 1
            plt.tight_layout()
            if save:
                plt.savefig(f'{save_plots_path}{clustername}_MSTO_DeltaM{deltaalpha}.pdf')
            plt.show()
        
        # He-enhanced CTs

        if plots:
            fig = plt.figure(figsize=(15, 15), dpi=100) 
            # plt.subplots_adjust(wspace = 0.20)

            min_mag -= 0.05
            max_mag += 0.05
            min_col += 0.25
            max2 -= 0.4

            # min_mag = 20.55
            # max_mag = 21.1
            # min_col = 0.6
            # max2 = 1.1

            plt.subplot(1,1,1)
            plt.scatter(x2, y2, marker = markersize_set, s=15, edgecolors='none', color=colorthis, alpha = 0.15)

            plt.plot(c_iso['F275W'] - c_iso['F336W'], c_iso['F275W'], color = 'dodgerblue', lw = 5, linestyle = '-', markersize = 0.1, marker = markersize_set)
            plt.scatter(dfusingisoini['F275W'] - dfusingisoini['F336W'], dfusingisoini['F275W'], marker = markersize_set, s=200, edgecolors='none', color='dodgerblue')
            plt.scatter(bluestIsochronepointRow[0] - bluestIsochronepointRow[1], bluestIsochronepointRow[0], marker = '*', s = 500, edgecolors='black', color='gold', zorder = 3)
            plt.plot(c_et['F275W'] - c_et['F336W'], c_et['F275W'], marker = markersize_set, markersize=0.1, linestyle = '-', lw = 5, color='orange', label = 'ET of .' + str(keyet) + ' \(M_\odot\)')
            
            plt.scatter(concatnewupper['x3'], concatnewupper['y3'], marker = '*', s=250, edgecolors='none', color='deeppink', label = str(len(concatnewupper)) + ' / ' + str(finalcountupper) + " Upper Bin [LF - " + str(abs(highbin)) + "]")
            plt.scatter(concatnewlower['x4'], concatnewlower['y4'], marker = '*', s=250, edgecolors='none', color='indigo', label = str(len(concatnewlower)) + ' / ' + str(finalcountlower) + " Lower Bin [LF - " + str(abs(lowbin)) + "]")
            plt.scatter(brightestpointcol, brightestpointmag, marker = '^', s=500, edgecolors='none', color='black', zorder = 3)
            plt.scatter(faintestpointcol, faintestpointmag, marker = '^', s=500, edgecolors='none', color='black', zorder = 3)
            plt.scatter(centerpointcol, centerpointmag, marker = '^', s=500, edgecolors='none', color='black', zorder = 3)


            if wantabund:
                plt.plot((a_et1['F' + f1 + 'W'] - a_et1['F' + f2 + 'W']), (a_et1['F' + f1 + 'W']), marker = markersize_set, markersize=0.1, linestyle='-', markeredgecolor='none', lw = 5, color=colorsheabund[0], label = 'ET of .' + (key3_st) + ' \(M_\odot\)')
                plt.plot((a_et2['F' + f1 + 'W'] - a_et2['F' + f2 + 'W']), (a_et2['F' + f1 + 'W']), marker = markersize_set, markersize=0.1, linestyle='-', markeredgecolor='none', lw = 5, color=colorsheabund[1], label = 'ET of .' + (key4_st) + ' \(M_\odot\)')
                # z = 2

                # Crossing Times MSTO
                for l in range(0, 2):
                    etmodelholder = {0: a_et1, 1: a_et2}
                    lowbin, highbin, brightestpointmag, brightestpointcol, faintestpointmag, faintestpointcol, centerpointmag, centerpointcol = MSTOCrossingTime(bluestIsochronepointRow, etmodelholder[l], f1, f2, f3, uppermagupper, lowermagupper, lowermaglower, df_part1, leftcol, rightcol, timecolstring) # finding lifetime ratios
                    
                    # print(str(l) + ": Crossing time of upper bin: " + str(highbin))
                    # print(str(l) + ": Crossing time of lower bin: " + str(lowbin))
                    
                    plt.scatter(brightestpointcol, brightestpointmag, marker = '^', s=500, edgecolors='none', color=colorsheabund[l], zorder = 3, rasterized=True)
                    plt.scatter(faintestpointcol, faintestpointmag, marker = '^', s=500, edgecolors='none', color=colorsheabund[l], zorder = 3, rasterized=True)
                    plt.scatter(centerpointcol, centerpointmag, marker = '^', s=500, edgecolors='none', color=colorsheabund[l], zorder = 3, rasterized=True)

                    # print(l)
                
            plt.xlim(min_col, max2)  #color
            plt.ylim(min_mag, max_mag)  #magnitude
            plt.xticks(fontsize=50)
            plt.yticks(fontsize=50) 
            plt.gca().invert_yaxis()
            if wantlegend:
                plt.legend(fontsize = 24, bbox_to_anchor=(1.1, 0.5))
            plt.ylabel(dictfiltermagnames[k], fontsize=50, labelpad=1)
            plt.xlabel(dictfiltermagnames[i] + ' - ' + dictfiltermagnames[j], fontsize=50)

        if wantabund:

            plt.figure(figsize=(15, 15), dpi=100) 
            # plt.subplots_adjust(wspace = 0.20)

            min_mag -= 0.05
            max_mag += 0.05
            min_col += 0.25
            max2 -= 0.4

            
            plt.scatter(x2, y2, marker = markersize_set, s=15, edgecolors='none', color=colorthis, alpha = 0.15, rasterized=True)

            plt.plot(c_iso['F275W'] - c_iso['F336W'], c_iso['F275W'], color = 'dodgerblue', lw = 5, linestyle = '-', markersize = 0.1, marker = markersize_set, rasterized=True)
            plt.scatter(dfusingisoini['F275W'] - dfusingisoini['F336W'], dfusingisoini['F275W'], marker = markersize_set, s=200, edgecolors='none', color='dodgerblue', rasterized=True)
            plt.scatter(bluestIsochronepointRow[0] - bluestIsochronepointRow[1], bluestIsochronepointRow[0], marker = '*', s = 500, edgecolors='black', color='gold', zorder = 3, rasterized=True)
            plt.plot(c_et['F275W'] - c_et['F336W'], c_et['F275W'], marker = markersize_set, markersize=0.1, linestyle = '-', lw = 5, color='orange', label = 'ET of .' + str(keyet) + ' \(M_\odot\)', rasterized=True)
            
            plt.scatter(concatnewupper['x3'], concatnewupper['y3'], marker = '*', s=250, edgecolors='none', color='deeppink', label = str(len(concatnewupper)) + ' / ' + str(finalcountupper), rasterized=True)
            plt.scatter(concatnewlower['x4'], concatnewlower['y4'], marker = '*', s=250, edgecolors='none', color='indigo', label = str(len(concatnewlower)) + ' / ' + str(finalcountlower), rasterized=True)
            plt.scatter(brightestpointcol, brightestpointmag, marker = '^', s=500, edgecolors='none', color='teal', zorder = 3, rasterized=True)
            plt.scatter(faintestpointcol, faintestpointmag, marker = '^', s=500, edgecolors='none', color='teal', zorder = 3, rasterized=True)
            plt.scatter(centerpointcol, centerpointmag, marker = '^', s=500, edgecolors='none', color='teal', zorder = 3, rasterized=True)

            plt.plot((a_et1['F' + f1 + 'W'] - a_et1['F' + f2 + 'W']), (a_et1['F' + f1 + 'W']), marker = markersize_set, markersize=0.1, linestyle='-', markeredgecolor='none', lw = 5, color=colorsheabund[0], label = 'ET of .' + (key3_st) + ' \(M_\odot\)', rasterized=True)
            plt.plot((a_et2['F' + f1 + 'W'] - a_et2['F' + f2 + 'W']), (a_et2['F' + f1 + 'W']), marker = markersize_set, markersize=0.1, linestyle='-', markeredgecolor='none', lw = 5, color=colorsheabund[1], label = 'ET of .' + (key4_st) + ' \(M_\odot\)', rasterized=True)
            # z = 2

            print("He-abundant crossing times below (0 means abund1 and 1 means abund2 below).")

            # Crossing Times MSTO
            for l in range(0, 2):
                etmodelholder = {0: a_et1, 1: a_et2}
                lowbin, highbin, brightestpointmag, brightestpointcol, faintestpointmag, faintestpointcol, centerpointmag, centerpointcol = MSTOCrossingTime(bluestIsochronepointRow, etmodelholder[l], f1, f2, f3, uppermagupper, lowermagupper, lowermaglower, df_part1, leftcol, rightcol, timecolstring) # finding lifetime ratios
                
                print(str(l) + " - Crossing time of upper bin: " + str(abs(round(highbin, 2))) + str(l) + " and Crossing time of lower bin: " + str(abs(round(lowbin, 2))))
                MSCT_a = abs(round(highbin, 2)) + abs(round(lowbin, 2))
                if l == 0:
                    MSCT_a1 = MSCT_a
                else:
                    MSCT_a2 = MSCT_a
                print(str(l) + " - Total CT for this: " + str(MSCT_a))

                plt.scatter(brightestpointcol, brightestpointmag, marker = '^', s=500, edgecolors='none', color=colorsheabund[l], zorder = 3)
                plt.scatter(faintestpointcol, faintestpointmag, marker = '^', s=500, edgecolors='none', color=colorsheabund[l], zorder = 3)
                plt.scatter(centerpointcol, centerpointmag, marker = '^', s=500, edgecolors='none', color=colorsheabund[l], zorder = 3)

                # print(l)
                
            plt.xlim(min_col, max2)  #color
            plt.ylim(min_mag, max_mag)  #magnitude
            plt.xticks(fontsize=30)
            plt.yticks(fontsize=30) 
            plt.gca().invert_yaxis()
            if wantlegend:
                plt.legend(fontsize = 24, bbox_to_anchor=(1.1, 0.5))
            plt.ylabel(dictfiltermagnames[k], fontsize=30, labelpad=1)
            plt.xlabel(dictfiltermagnames[i] + ' - ' + dictfiltermagnames[j], fontsize=30) 

        plt.tight_layout()
        if save:
            plt.savefig(f'{save_plots_path}{clustername}_MSTOHeAbund_DeltaM{deltaalpha}.pdf')
        plt.show()
        
        if wantcsv:
            # dfstoringcsv.loc[g, 'CMD'] = f
            dfstoringcsv.loc[g, 'iso'] = keyiso
            # dfstoringcsv.loc[g, 'pm cut'] = pm
            dfstoringcsv.loc[g, 'del_alp'] = deltaalpha
            dfstoringcsv.loc[g, 'UB SC'] = len(concatnewupper)
            dfstoringcsv.loc[g, 'UB SC F'] = round(finalcountupper, 0)
            dfstoringcsv.loc[g, 'UB L (Myrs)'] = abs(round(highbin, 1))
            dfstoringcsv.loc[g, 'LB SC'] = len(concatnewlower)
            dfstoringcsv.loc[g, 'LB SC F'] = round(finalcountlower, 0)
            dfstoringcsv.loc[g, 'LB L (Myrs)'] = abs(round(lowbin, 1))
            dfstoringcsv.loc[g, 'T L (Myrs)'] = abs(round(highbin, 1)) + abs(round(lowbin, 1))
            dfstoringcsv.loc[g, 'mag_wid'] = abs(round(uppermagupper - lowermagupper, 2))
            dfstoringcsv.loc[g, 'col_wid'] = round(uppercolupper - lowercolupper, 2)
            dfstoringcsvfinal = pd.concat([dfstoringcsvfinal, dfstoringcsv], ignore_index=True)
            dfstoringcsv = pd.DataFrame()
            g = g + 1
            # print(g)

    if wantcsv:
        dfstoringcsvfinal = dfstoringcsvfinal.drop_duplicates()
        dfstoringcsvfinal.to_csv(str(func_other.TimeStampFunc()) +  ' msto.csv', index=False)
        print(dfstoringcsvfinal)

    return locals()
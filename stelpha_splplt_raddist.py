import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import func_analysis

def initialize(dfspatial, 
               dfspatialcopy,
               racluster, deccluster, 
               forspatialplotUpperMS, forspatialplotLowerMS,
               bin1SP, bin2SP, dfwdcalbrightSP, 
               hbspatialplotint,
               singlecolor, hb,
               dpi):

    forspatialplotUpperMS = pd.merge(dfspatial, forspatialplotUpperMS, on='ID', how='inner')
    forspatialplotUpperMS = forspatialplotUpperMS.drop_duplicates()
    
    forspatialplotLowerMS = pd.merge(dfspatial, forspatialplotLowerMS, on='ID', how='inner')
    forspatialplotLowerMS = forspatialplotLowerMS.drop_duplicates()
    
    bin1SP = pd.merge(dfspatial, bin1SP, on='ID', how='inner')
    bin1SP = bin1SP.drop_duplicates()

    bin2SP = pd.merge(dfspatial, bin2SP, on='ID', how='inner')
    bin2SP = bin2SP.drop_duplicates()

    dfwdcalbrightSP = pd.merge(dfspatial, dfwdcalbrightSP, on='ID', how='inner')
    dfwdcalbrightSP = dfwdcalbrightSP.drop_duplicates()

    print("Number of MSTO Upper Stars: " + str(len(forspatialplotUpperMS)))
    print("Number of MSTO Lower Stars: " + str(len(forspatialplotLowerMS)))
    print("Number of WD Upper Stars: " + str(len(bin1SP)))
    print("Number of WD Lower Stars: " + str(len(bin2SP)))
    print("Number of WD `Bright' Stars: " + str(len(dfwdcalbrightSP)))

    markersize_set = 'o'

    if singlecolor:
        colors = ['brown', 'brown', 'brown', 'brown', 'brown', 'brown', 'brown']
        colors2 = ['green', 'green', 'green', 'green', 'green', 'green']
        colors3 = ['dodgerblue', 'dodgerblue', 'dodgerblue', 'dodgerblue']
    else:
        colors2 = ['dodgerblue', 'red' , 'teal', 'dodgerblue', 'b', 'teal']
        colors3 = ['deeppink', 'purple', 'deeppink', 'purple']

    plt.rcParams['figure.dpi'] = dpi
    plt.tight_layout()
    fig = plt.figure(figsize=(20, 23))
    plt.subplots_adjust(wspace = 0.2)

    # dfspatialcopy = dfspatial[(dfspatial['F275W'] > 12) & (dfspatial['F275W'] < 28) & (dfspatial['F336W'] < 28) & (dfspatial['F336W'] > 12)].copy()
    # dfspatialcopy = dfspatial.copy()
    
    plt.subplot(2,2,1)
    plt.scatter(dfspatialcopy['RA'], dfspatialcopy['DEC'], marker = markersize_set, s=0.7, edgecolors='none', color='black', label = 'Number of Objects - ' + str(len(dfspatialcopy['RA'])))
    
    plt.subplot(2,2,2)
    plt.scatter(dfspatialcopy['RA'], dfspatialcopy['DEC'], marker = markersize_set, s=0.7, edgecolors='none', color='black', label = 'Number of Objects - ' + str(len(dfspatialcopy['RA'])))
    
    index_list_combined = [forspatialplotUpperMS, forspatialplotLowerMS]
    for i in range (len(index_list_combined)):
        newRA, newDEC = index_list_combined[i]['RA'], index_list_combined[i]['DEC']
        plt.subplot(2,2,1)
        plt.scatter(newRA, newDEC, marker = 'o', s=25, edgecolors='none', color=colors3[i], label = 'Number of Objects - ' + str(len(newRA))) 

    plt.subplot(2,2,1)
    plt.xlabel(r'RA (degrees)', fontsize = 20)
    plt.ylabel(r'DEC (degrees)', fontsize = 20)
    # plt.legend()
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20) 
    plt.gca().invert_xaxis()

    index_list_combined_WD = [bin1SP, bin2SP] 
    for i in range (len(index_list_combined_WD)):
        newRA, newDEC = index_list_combined_WD[i]['RA'], index_list_combined_WD[i]['DEC']
        plt.subplot(2,2,2)
        plt.scatter(newRA, newDEC, marker = 'o', s=45, edgecolors='none', color=colors2[i], label = 'Number of Objects - ' + str(len(newRA))) 

    index_list_combined_WD = [dfwdcalbrightSP] 
    for i in range (len(index_list_combined_WD)):
        newRA, newDEC = index_list_combined_WD[i]['RA'], index_list_combined_WD[i]['DEC']
        plt.subplot(2,2,2)
        plt.scatter(newRA, newDEC, marker = '*', s=500, edgecolors='black', color='teal', label = 'Number of Objects - ' + str(len(newRA)))

    plt.subplot(2,2,2)
    plt.xlabel(r'RA (degrees)', fontsize = 20)
    plt.ylabel(r'DEC (degrees)', fontsize = 20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20) 
    # plt.legend()
    plt.gca().invert_xaxis()

    print("Blue Radial Dist is for MSTO, Green for WD and Brown for HB")

    if hb:
        hbspatialplotint = pd.merge(dfspatial, hbspatialplotint, on='ID', how='inner')
        hbspatialplotint = hbspatialplotint.drop_duplicates()

        print("Number of HB Stars: " + str(len(hbspatialplotint)))

        plt.subplot(2,2,3)
        plt.scatter(dfspatialcopy['RA'], dfspatialcopy['DEC'], marker = markersize_set, s=0.3, edgecolors='none', color='black', label = 'Number of Objects - ' + str(len(dfspatialcopy['RA'])))
        
        index_list_combined_HB = [hbspatialplotint]

        for i in range (len(index_list_combined_HB)):
            if (i == 1):
                for j in range(len(hbspatialplotint)):
                    newRA, newDEC = index_list_combined_HB[i]['RA'], index_list_combined_HB[i]['DEC']
                    plt.subplot(2,2,3)
                    plt.scatter(newRA, newDEC, marker = 'o', s=15, edgecolors='none', color=colors[j], label = 'Number of Objects - ' + str(len(newRA))) 
        
        plt.subplot(2,2,3)
        plt.xlabel(r'RA (degrees)', fontsize = 20)
        plt.ylabel(r'DEC (degrees)', fontsize = 20)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.gca().invert_xaxis()

        # Radial Plot 

        index_list_combined = [bin1SP, bin2SP, dfwdcalbrightSP,
                            forspatialplotUpperMS, forspatialplotLowerMS, 
                            hbspatialplotint]

        holdRadDist_list = []
        for i in range(0, 3):
            holdRadDist = func_analysis.RadDistFunc(index_list_combined[i], racluster, deccluster)
            holdRadDist_list.append(holdRadDist)
        merged_holdRadDist_WD = pd.concat(holdRadDist_list, ignore_index=True)

        holdRadDist_list = []
        for i in range(3, 5):
            holdRadDist = func_analysis.RadDistFunc(index_list_combined[i], racluster, deccluster)
            holdRadDist_list.append(holdRadDist)
        merged_holdRadDist_MS = pd.concat(holdRadDist_list, ignore_index=True)

        holdRadDist_list = []
        for i in range(5, 6):
            for j in range(len(index_list_combined[i])):
                hbholder = index_list_combined[i][j]
                holdRadDist = func_analysis.RadDistFunc(hbholder, racluster, deccluster)
            holdRadDist_list.append(holdRadDist)
        merged_holdRadDist_HB = pd.concat(holdRadDist_list, ignore_index=True)

        plt.subplot(2,2,4)

        counts, bin_edges = np.histogram(merged_holdRadDist_WD['dist'], bins=10)
        plt.step(bin_edges[:-1], counts/(sum(counts)), where='mid',
                color='green', label='WD ' + str(sum(counts)), linestyle='-.', linewidth=2.5)

        counts, bin_edges = np.histogram(merged_holdRadDist_MS['dist'], bins=10)
        plt.step(bin_edges[:-1], counts/(sum(counts)), where='mid',
                color='dodgerblue', label='MSTO ' + str(sum(counts)), linestyle='--', linewidth=2.5)

        counts, bin_edges = np.histogram(merged_holdRadDist_HB['dist'], bins=10)
        plt.step(bin_edges[:-1], counts/(sum(counts)), where='mid',
                color='brown', label='HB ' + str(sum(counts)), linestyle='-', linewidth=1.5)

        # plt.legend(fontsize=20)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20) 
        plt.ylabel(r'Number of Stars (normalized to total count)', fontsize = 20)
        plt.xlabel(r'Distance [arcmin]', fontsize = 20)
        plt.show()

    else:
        index_list_combined = [bin1SP, bin2SP, dfwdcalbrightSP,
                            forspatialplotUpperMS, forspatialplotLowerMS]

        holdRadDist_list = []
        for i in range(0, 3):
            holdRadDist = func_analysis.RadDistFunc(index_list_combined[i], racluster, deccluster)
            holdRadDist_list.append(holdRadDist)
        merged_holdRadDist_WD = pd.concat(holdRadDist_list, ignore_index=True)

        holdRadDist_list = []
        for i in range(3, 5):
            holdRadDist = func_analysis.RadDistFunc(index_list_combined[i], racluster, deccluster)
            holdRadDist_list.append(holdRadDist)
        merged_holdRadDist_MS = pd.concat(holdRadDist_list, ignore_index=True)

        plt.subplot(2,2,4)

        counts, bin_edges = np.histogram(merged_holdRadDist_WD['dist'], bins=10)
        plt.step(bin_edges[:-1], counts/(sum(counts)), where='mid',
                color='green', label='WD ' + str(sum(counts)), linestyle='-.', linewidth=2.5)

        counts, bin_edges = np.histogram(merged_holdRadDist_MS['dist'], bins=10)
        plt.step(bin_edges[:-1], counts/(sum(counts)), where='mid',
                color='dodgerblue', label='MSTO ' + str(sum(counts)), linestyle='--', linewidth=2.5)

        # plt.legend(fontsize=20)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20) 
        plt.ylabel(r'Number of Stars (normalized to total count)', fontsize = 20)
        plt.xlabel(r'Distance [arcmin]', fontsize = 20)
        plt.show()

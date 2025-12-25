import pandas as pd
import matplotlib.pyplot as plt
import math 
import copy
markersize_set = 'o'

def fewclusters(cleandata, dfparams, dictfilters, list, dpi, pmholder, legend):

    plt.rcParams['figure.dpi']=dpi
    plt.tight_layout()
    n = len(list)
    print("CMD of " + str(n) + " being printed:")
    print("Name Reddening DM aDM Dist")
    w = math.ceil(math.sqrt(n))
    h = math.ceil(n / w)
    fig = plt.figure(figsize=(w * 5, h * 5))      
    plt.subplots_adjust(wspace=0.35)

    i, j, a = 0, 1, 1

    for m, (key, df) in enumerate(list.items()):

        reddening = round(dfparams['dfparams'].loc[dfparams['dfparams']['ID'] == key, "E(B-V)"].values[0], 2)
        DM = dfparams['dfparams'].loc[dfparams['dfparams']['ID'] == key, "(m-M)V"].values[0]
        aDM = round(DM - 3.1*reddening, 2)
        d = round(10 * (10 ** ((aDM) / 5)) - (3.1 * (reddening)), 2)

        for k in range(len(pmholder)):
            df_cleaned = cleandata(df, pmholder[k])

            min_mag = 11
            max_mag = 31
            min_col = -3
            max_col = 6

            f1 = dictfilters[i]
            f2 = dictfilters[j]

            mag = df_cleaned['F' + f1 +'W'] 
            col = df_cleaned['F' + f1 +'W'] - df_cleaned['F' + f2 +'W']
            
            holdthese = {'mag': mag, 'col': col}
            df_plot = pd.DataFrame(holdthese)
            df_plot = df_plot[df_plot['mag'] <= max_mag]
            df_plot = df_plot[df_plot['mag'] >= min_mag]
            df_plot = df_plot[df_plot['col'] <= max_col]
            df_plot = df_plot[df_plot['col'] >= min_col]

            plt.subplot(h, w, a)
            plt.scatter(df_plot['col'], df_plot['mag'], marker = markersize_set, s=5, alpha=0.5, edgecolors='none', color='black', label = str(key) + " " + str(reddening) + " " + str(DM) + " " + str(aDM) + " " + str(d)) #, label = str(len(df_plot))            
            plt.xlim(min_col, max_col)  #color
            plt.ylim(min_mag, max_mag)  #magnitude

            # plt.text(0,)

            if legend:
                plt.legend(fontsize = 10)
            
            plt.gca().invert_yaxis() 
            plt.xticks(fontsize = 20)
            plt.yticks(fontsize = 20)
            plt.tick_params(axis='y', which='both')
            plt.tick_params(axis='x', which='both')
            # plt.title('F' + f1 +'W' + '-' + 'F' + f2 +'W' + ' vs. ' + 'F' + f1 +'W' + ' (' + clusterandmethname + ')')
            # plt.ylabel("\(m_{F275W} \)", fontsize=20, labelpad=1, rotation='vertical')
            # plt.xlabel("\( m_{F275W} - m_{F336W} \)", fontsize=20)
            a = a + 1
    plt.show()

def allclusters(cleandata, dfparams, dictfilters, dfclusters, dpi, pmholder, legend):

    plt.rcParams['figure.dpi']=dpi
    plt.tight_layout()
    n = len(dfclusters)
    print("CMD of all " + str(n) + " being printed:")
    w = math.ceil(math.sqrt(n))
    h = math.ceil(n / w)
    fig = plt.figure(figsize=(w * 5, h * 5))      
    plt.subplots_adjust(wspace=0.35)

    i, j, a = 0, 1, 1
    list = dfclusters

    for m, (key, df) in enumerate(list.items()):

        reddening = round(dfparams['dfparams'].loc[dfparams['dfparams']['ID'] == key, "E(B-V)"].values[0], 2)
        DM = dfparams['dfparams'].loc[dfparams['dfparams']['ID'] == key, "(m-M)V"].values[0]
        aDM = round(DM - 3.1*reddening, 2)
        d = round(10 * (10 ** ((aDM) / 5)) - (3.1 * (reddening)), 2)

        for k in range(len(pmholder)):
            df_cleaned = cleandata(df, pmholder[k])

            min_mag = 11
            max_mag = 30
            min_col = -3
            max_col = 4

            f1 = dictfilters[i]
            f2 = dictfilters[j]

            mag = df_cleaned['F' + f1 +'W'] 
            col = df_cleaned['F' + f1 +'W'] - df_cleaned['F' + f2 +'W']
            
            holdthese = {'mag': mag, 'col': col}
            df_plot = pd.DataFrame(holdthese)
            df_plot = df_plot[df_plot['mag'] <= max_mag]
            df_plot = df_plot[df_plot['mag'] >= min_mag]
            df_plot = df_plot[df_plot['col'] <= max_col]
            df_plot = df_plot[df_plot['col'] >= min_col]

            plt.subplot(h, w, a)
            plt.scatter(df_plot['col'], df_plot['mag'], marker = markersize_set, s=5, alpha=1, edgecolors='none', color='black', label = str(key) + " " + str(reddening) + " " + str(DM) + " " + str(aDM) + " " + str(d)) #, label = str(len(df_plot))            
            plt.xlim(min_col, max_col)  #color
            plt.ylim(min_mag, max_mag)  #magnitude

            if legend:
                plt.legend(fontsize = 10)
            
            plt.gca().invert_yaxis() 
            plt.xticks(fontsize = 20)
            plt.yticks(fontsize = 20)
            plt.tick_params(axis='y', which='both')
            plt.tick_params(axis='x', which='both')
            # plt.title('F' + f1 +'W' + '-' + 'F' + f2 +'W' + ' vs. ' + 'F' + f1 +'W' + ' (' + clusterandmethname + ')')

            # plt.ylabel("\(m_{F275W} \)", fontsize=20, labelpad=1, rotation='vertical')
            # plt.xlabel("\( m_{F275W} - m_{F336W} \)", fontsize=20)
            a = a + 1
    plt.show()
import matplotlib.pyplot as plt
import math 
import copy

markersize_set = 'o'

def fewclusters(list, dpi, legend, afterhowmany):

    plt.rcParams['figure.dpi'] = dpi 
    plt.tight_layout()
    n = len(list)
    print("Spatial plot of " + str(n) + " being printed.")
    w = math.ceil(math.sqrt(n))
    h = math.ceil(n / w)
    fig = plt.figure(figsize=(w * 6, h * 6))      
    plt.subplots_adjust(wspace=0.35)

    for i, (key, df) in enumerate(list.items()):
        plt.subplot(h, w, i + 1)
        df = df.copy()
        df = df.iloc[::afterhowmany]
        # df['RA'] = df['RA'].round(2)
        # df['DEC'] = df['DEC'].round(2)
        # df = df[(df['F275W'] > 12) & (df['F275W'] < 28) & (df['F336W'] < 28) & (df['F336W'] > 12)].copy()
        plt.scatter(df['RA'], df['DEC'], marker=markersize_set, s=0.3,
                    edgecolors='none', color='black',
                    label=key.replace("ngc", "") + ' Objs - ' + str(len(df['RA'])))
        if legend:
            plt.legend(fontsize=10)
        plt.xlabel(r'RA (degrees)', fontsize=12)
        plt.ylabel(r'DEC (degrees)', fontsize=12)
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10) 
        plt.gca().invert_xaxis()
    
    plt.show() 
    
def allclusters(dfclusters, dpi, legend, afterhowmany):

    # suffixes = [key.replace("ngc", "") for key in list.keys()] str(suffixes[i]) + 
    list = dfclusters
    
    plt.rcParams['figure.dpi'] = dpi 
    plt.tight_layout()
    n = len(list)
    print("Spatial plot of all entered clusters being printed.")
    w = math.ceil(math.sqrt(n))
    h = math.ceil(n / w)
    fig = plt.figure(figsize=(w * 4, h * 4))      
    plt.subplots_adjust(wspace=0.35)

    for i, (key, df) in enumerate(list.items()):
        plt.subplot(h, w, i + 1)
        df = df.copy()
        df = df.iloc[::afterhowmany]
        # df['RA'] = df['RA'].round(2)
        # df['DEC'] = df['DEC'].round(2)
        # df = df[(df['F275W'] > 12) & (df['F275W'] < 28) & (df['F336W'] < 28) & (df['F336W'] > 12)].copy()
        plt.scatter(df['RA'], df['DEC'], marker=markersize_set, s=0.3,
                    edgecolors='none', color='black',
                    label=key.replace("ngc", "") + ' Objs - ' + str(len(df['RA'])))
        if legend:
            plt.legend(fontsize=10)
        plt.xlabel(r'RA (degrees)', fontsize=12)
        plt.ylabel(r'DEC (degrees)', fontsize=12)
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10) 
        plt.gca().invert_xaxis()

    plt.show()
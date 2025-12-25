from shapely.geometry import Polygon, Point
import pandas as pd
import numpy as np
import math
import copy

def ra_to_deg(hours, minutes, seconds):
    return 15 * (hours + minutes / 60 + seconds / 3600)

def dec_to_deg(degrees, arcminutes, arcseconds):
    sign = -1 if degrees < 0 else 1
    return (sign * (abs(float(degrees)) + float(arcminutes) / 60 + float(arcseconds) / 3600))
    # return 15 * (float(h) + float(m)/60 + float(s)/3600)

def combine_and_convert_ra(row):
    return ra_to_deg(row['RA1'], row['RA2'], row['RA3'])

def combine_and_convert_dec(row):
    return dec_to_deg(row['DEC1'], row['DEC2'], row['DEC3'])

def corrections(dist, colorex, df):
  distISO = dist
  colorexcess = colorex

  copydataframesdf = copy.deepcopy(df)

  d = 10 * (10 ** (distISO / 5))

  A_VISO = colorexcess * 3.1  # (color excess) times 3.1
  A_275 = 1.799 * A_VISO
  A_336 = 1.643 * A_VISO
  A_438 = 1.352 * A_VISO
  A_606 = 0.92 * A_VISO
  A_814 = 0.55 * A_VISO

  for sub_dict in copydataframesdf.values():
    sub_dict['F275W'] += 5 * math.log10(d) + A_275 - 5
    sub_dict['F336W'] += 5 * math.log10(d) + A_336 - 5
    sub_dict['F438W'] += 5 * math.log10(d) + A_438 - 5
    sub_dict['F606W'] += 5 * math.log10(d) + A_606 - 5
    sub_dict['F814W'] += 5 * math.log10(d) + A_814 - 5

  return copydataframesdf

def cleandata(df, problimit):
    dfpm = pd.DataFrame()
    for start in range(0, len(df), 100000):
        end = start + 100000
        chunk = df[start:end]
        condition11 = chunk['memb'] >= problimit
        filtered_chunk = chunk[condition11]
        dfpm = pd.concat([dfpm, filtered_chunk])
    
    return dfpm

def sigma_clip(data, sigma, max_iter):
    for _ in range(max_iter):
        mean = np.mean(data.iloc[:, 0].values)
        std = np.std(data.iloc[:, 0].values)
        mask = (np.abs(data.iloc[:, 0].values - mean)) < (sigma * std)
        data1 = data[mask]  
        data = data1

    return data1

def parameters(onex, oney, twox, twoy): 
    slope = (oney - twoy) / (onex - twox)
    x_point = onex
    y_point = oney  
    intercept = y_point - slope * x_point
    return slope, intercept

def CreatingHistograms(data, lower_bin_edge, bin_width):
    min_val = np.min(data)
    max_val = np.max(data)
    bins = np.arange(lower_bin_edge, max_val + bin_width, bin_width)
    hist, bins = np.histogram(data, bins=bins)

    histogram_df = pd.DataFrame({
        'Bin Lower': bins[:-1],
        'Bin Upper': bins[1:],
        'Bin Center': (bins[:-1] + bins[1:])/2,
        'NCount Compl': hist
    })
    
    return histogram_df, bins, hist

def CreatingHistograms2(data, lower_bin_edge, bin_width):
    min_val = np.min(data)
    max_val = np.max(data)
    bins = np.arange(lower_bin_edge, max_val + bin_width, bin_width)
    hist, bins = np.histogram(data, bins=bins)

    histogram_df = pd.DataFrame({
        'Bin Lower': bins[:-1],
        'Bin Upper': bins[1:],
        'Bin Center': (bins[:-1] + bins[1:])/2,
        'Combined Count Compl': hist
    })
    
    return histogram_df, bins, hist

def point_inside_parallelogram(x, y, parallelogram_vertices):
    parallelogram_shapely = Polygon(parallelogram_vertices)
    return Point(x, y).within(parallelogram_shapely)

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

def RadDistFunc(dfp, racluster, deccluster):
    dfp_copy = dfp.copy()
    
    # for calculating distance: 
    # (RA of star * cos (DEC of star)) - (RA of centre of GC * cos (DEC of centre of GC))
    # DEC of star - DEC of centre of GC

    dfp_copy['RAOG'] = dfp_copy['RA']
    dfp_copy['DECOG'] = dfp_copy['DEC']

    dfp_copy['dist'] = np.sqrt(((np.radians(dfp_copy['RA']))*(np.cos(np.radians(dfp_copy['DEC']))) - np.radians(racluster)*(np.cos(np.radians(deccluster))))**2 + ((np.radians(dfp_copy['DEC'])) - np.radians(deccluster))**2)*((60*180)/(np.pi))
    
    # for plotting
    # RA of star * cos (DEC of star)
    # DEC of star

    dfp_copy['RA'] = (np.radians(dfp_copy['RA']))*(np.cos(np.radians(dfp_copy['DEC'])))
    dfp_copy['DEC'] = (np.radians(dfp_copy['DEC'])) 
    
    return dfp_copy

# Importing libraries

import os
import csv
import math
import copy
import time
import requests
from io import StringIO
from functools import reduce

import numpy as np
import pandas as pd
import seaborn as sns
from astropy.io import fits
import plotly.graph_objects as go
from shapely.geometry import Polygon, Point

from scipy.stats import norm
from scipy.stats import sigmaclip
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
from scipy.stats import gaussian_kde
from scipy.interpolate import interp1d
from scipy.spatial import distance_matrix

import mplcursors
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import MultipleLocator
from matplotlib.patches import Polygon as MatplotlibPolygon
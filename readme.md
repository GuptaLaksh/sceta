Welcome to ?!

gscetno py ~ sct

rgcscetatpnuvop
sceta
scet
scetapy
stcet
discrepy
scintally

resolved globular clusters STar Count-Evolutionary Time analysis technique in PYthon with near-ultraviolent and optical photometric data

These routine were written as part of my (Laksh Gupta) undergraduate thesis. These routines essentially perform star count-crossing time analysis for Globular Cluster on F275W-F336W vs F275W Color Magnitude plane. The MSTO and WD routine are now working. The HB routine is still under work.

- If you are working with a cluster for the first time, 
    - make sure to have downloaded and stored the model files in a folder and have that path in theoreticalmodels.initialize(). 
    - make sure to have the model loaded in func_input.ReadingModels().
    - make sure that your cluster data is loaded.

- For input models:
    - For ETs, input only the neccesary parts or one would encounter error. 

- For MSTO routine:
    - Advisable to not play around sigma cut must. Only when you understand it's relation to bluelimit and redlimit, do that.
    - mag and col ranges must be changed for different clsuters. 

- For WD routine:
    - 'division' and the following 5 params must be changed for cluster to cluster. 
    - Completeness=False, unless a 'CompCor' function is input.

- For Radial Distribution and Spatial Plot of Stellar Phases:
    - if 'singlecolor=False', colors of the stars in previous figures and this will be the same. 
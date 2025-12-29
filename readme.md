Welcome! ``sceta`` stands for Star Count Evolutionary Time Analysis.

Using this pipeline, one can counts stars and the corresponding evolutionary times on the color-magnitude plane of resolved globular clusters. Currently, it works only for HUGS. It is entirely written in Python. 

These routine were written as part of my (Laksh Gupta) undergraduate thesis. The MSTO and WD routine are now working. The HB routine is still under work.

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

Contact me at lakshgupta.phy@gmail.com
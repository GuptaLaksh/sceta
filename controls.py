def Controls(whichcluster, wantDiffRed, wantWDLFSep):

    clustername = whichcluster

    DiffRed = wantDiffRed # must be 'True' only if you want Main Seqeunce Differential Reddening Numbers
    WDLFSep = wantWDLFSep # must be 'True' only if you want WDLF seperately 

    return clustername, DiffRed, WDLFSep

    #2808 - reddening - 14.9, color excess - 0.22
    #0104 - reddening - 13.37, color excess - 0.04
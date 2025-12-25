def Initialize(load_all_clusters_fast, pathstartswith, names):
    # names = [
    #     "0104", "2808", "5272", "6397", "5904", 
    #     "6752", "6656", "6541", "6254", "6205", "6218",
    #     "6093", "4833", "6341", "0362",
    #     "7078", "6715", "6441", "6388", "5986", "5286", "6934", "5024"
    # ]
    # names = [clustername]

    folder = pathstartswith + "CleanedHUGSFiles"

    dfclusters = load_all_clusters_fast(
        namesofclusters=names,
        input_folder=folder,
        extension=".txt",      # or ".clean" or whatever you used
        save_feather=False     # turn True to save feather copies
    )
    return locals()
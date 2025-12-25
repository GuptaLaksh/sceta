import pandas as pd
import numpy as np
import os
import csv
import time

def Remove(txtfile, txtfile0, removal): # Function removes everything before 'removal'.
    with open(txtfile, 'r') as txtfile:
        content = txtfile.read()

    if content.startswith(removal):
        newtext = content[len(removal):]
    else:
        newtext = content

    with open(txtfile0, 'w') as txtfile:
        txtfile.write(newtext)

def InputFile(removal, txtfile): # to input files 
    nameofthefile = 'redundant'
    txtfile0 = nameofthefile + '.txt'

    Remove(txtfile, txtfile0, removal)
    txtfile1 = nameofthefile + '.txt'
    csvfile1 = nameofthefile + '.csv'
    
    with open(txtfile1, 'r') as txt_file:
        lines = txt_file.readlines()

    data = []

    for line in lines:
        entries = line.strip().split()
        data.append(entries)

    with open(csvfile1, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for row in data:
            csv_writer.writerow(row)
    
    df = pd.read_csv(nameofthefile + '.csv')

    if os.path.exists(nameofthefile + '.csv'):
        os.remove(nameofthefile + '.csv')
    
    if os.path.exists(nameofthefile + '.txt'):
        os.remove(nameofthefile + '.txt')

    return df 

def FetchFilesInFolder(path):
    files_list = []
    names_list = []

    for root, dirs, files in os.walk(path):
        files_in_dir = [os.path.join(root, file) for file in files if file != '.DS_Store']
        files_list.extend(files_in_dir)

        # Extract filenames with extensions
        names_in_dir = [file for file in files if file != '.DS_Store']
        names_list.extend(names_in_dir)

    # Sort both lists in ascending order
    files_list.sort()
    names_list.sort()

    return files_list, names_list

def ReadingModels(folder_path, file_end_names, specific_text, specified_text_2, type): 

    dataframes = {}
    files_list, names_list = FetchFilesInFolder(folder_path)
    # print(names_list)

    for i in range(0, len(files_list)):
        # print(files_list[i])
        txt_file = files_list[i]

        with open(txt_file, 'r') as file:
            file_contents = file.read()

        position = file_contents.find(specific_text)

        if (type):
            if position != -1:
                modified_contents = file_contents[position:]
                position_2 = modified_contents.find(specified_text_2)

                if position_2 != -1:
                    modified_contents = modified_contents.replace(specified_text_2, '')

                output_file_path = 'redundant' + str(i) + '.txt'
                with open(output_file_path, 'w') as output_file:
                    output_file.write(modified_contents)
        
        else:
            if position != -1:
                modified_contents = file_contents[position:]
                
                output_file_path = 'redundant' + str(i) + '.txt'
                with open(output_file_path, 'w') as output_file:
                    output_file.write(modified_contents)

        txtfile1 = 'redundant' + str(i) + '.txt'
        csvfile1 = 'redundant' + str(i) + '.csv'
        # print(txtfile1)

        with open(txtfile1, 'r') as txt_file:
            lines = txt_file.readlines()

        data = []
        for line in lines:
            entries = line.strip().split()
            data.append(entries)

        with open(csvfile1, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            for row in data:
                csv_writer.writerow(row)

        data = pd.read_csv("redundant" + str(i) + ".csv")
        var_name = file_end_names[i]
        dataframes[var_name] = pd.DataFrame(data)

        if os.path.exists("redundant" + str(i) + ".csv"):
            os.remove("redundant" + str(i) + ".csv")

        if os.path.exists("redundant" + str(i) + ".txt"):
            os.remove("redundant" + str(i) + ".txt")

    return dataframes

def LoadClusters(
    namesofclusters,
    input_folder,
    extension=".txt",
    save_feather=False
):

    dfclusters = {}
    t0 = time.time()

    for name in namesofclusters:
        cluster_id = f"ngc{name}"
        filepath = os.path.join(input_folder, f"{cluster_id}{extension}")

        if not os.path.exists(filepath):
            print(f"Skipped: {cluster_id} (file not found)")
            continue

        try:
            df = pd.read_csv(
                filepath,
                sep=r"\s+",
                header=0,
                comment="#",
                engine="c"
            )
            dfclusters[cluster_id] = df

            if save_feather:
                feather_path = os.path.join(input_folder, f"{cluster_id}.feather")
                df.to_feather(feather_path)

            # print(f"{cluster_id} ({df.shape[0]} rows)")

        except Exception as e:
            print(f"Failed to load {cluster_id}: {e}")

    return dfclusters

import os
import sys
import json
import numpy as np
import pandas as pd

def get_tsv(path):
    """
    :param path:
    :return:
    """
    label_list = []
    vec_list = []
    with open(path, encoding="utf-8") as file:
        for line in file.readlines():
            line = line.strip()
            line = line.split(',')
            label_list.append(line[0])
            vec_list.append(list(map(float, line[1].strip().split())))

    label_array = np.array(label_list)
    vec_array = np.array(vec_list)

    label_df = pd.DataFrame(label_array)
    vec_df = pd.DataFrame(vec_array)

    label_path = "./label.tsv"
    if os.path.exists(label_path):
        os.remove(label_path)
    with open(label_path, 'w') as write_tsv:
        write_tsv.write(label_df.to_csv(sep='\t', index=False, header=False))

    vec_path = "./vector.tsv"
    if os.path.exists(vec_path):
        os.remove(vec_path)
    with open(vec_path, 'w') as write_tsv:
        write_tsv.write(vec_df.to_csv(sep='\t', index=False, header=False))
    print("Finished.")


if __name__ == "__main__":

    path = "./embedding.txt"
    get_tsv(path)

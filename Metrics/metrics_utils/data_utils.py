import os
import csv
import pandas as pd
import numpy as np

def get_absolute_path(dir_type):
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    parent_dir = os.path.dirname(script_dir)
    return os.path.join(parent_dir, dir_type)


def load_exp_rep(csvs_path):
    participants_exp_rep = {}

    for filename in os.listdir(csvs_path):
        if filename.endswith('.csv') and os.path.splitext(filename)[0] != "coupling":
            file_path = os.path.join(csvs_path, filename)
            key = os.path.splitext(filename)[0]
            participants_exp_rep[key] = pd.read_csv(file_path, header=None).values

    return participants_exp_rep


def get_all_exp_rep_and_label(participants_exp_rep):
    labels = []
    data_list = []

    for label, array in participants_exp_rep.items():
        labels.extend([label] * len(array))
        data_list.extend(array)

    data = np.array(data_list)
    labels = np.array(labels)
    return data, labels


def get_couple_exp_rep_and_label(participants_exp_rep, part1, part2):
    labels = []
    data_list = []

    array = participants_exp_rep[str(part1)]
    labels.extend([part1] * len(array))
    data_list.extend(array)

    array = participants_exp_rep[str(part2)]
    labels.extend([part2] * len(array))
    data_list.extend(array)

    data = np.array(data_list)
    labels = np.array(labels)
    return data, labels


def get_couples(coupling_path):
    couples = []
    with open(coupling_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            couples.append(row)
    # df = pd.read_csv(coupling_path, header=None, names=['user_id_1', 'user_id_2'])
    # couples = [tuple(row) for row in df.values]
    return couples


def get_strangers(original_couples):
    len_couples = len(original_couples)
    return [(original_couples[i][0], original_couples[(i + 1) % len_couples][1]) for i in range(len_couples)]


def get_all_participants(original_couples):
    res = []
    for couple in original_couples:
        res.append(couple[0])
        res.append(couple[1])
    return res


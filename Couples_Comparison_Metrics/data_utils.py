import os
import pandas as pd

def get_absolute_path(dir_type):
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    parent_dir = os.path.dirname(script_dir)
    return os.path.join(parent_dir, dir_type)


def load_exp_rep(csvs_path):
    participants_exp_rep = {}

    for filename in os.listdir(csvs_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(csvs_path, filename)
            key = os.path.splitext(filename)[0]
            participants_exp_rep[key] = pd.read_csv(file_path)

    return participants_exp_rep


def get_couples(coupling_path):
    pass







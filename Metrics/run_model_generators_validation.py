import os
import pandas as pd
import numpy as np
import csv

CURR_DATA_PATH = "spectre"


class GenValidate:
    @staticmethod
    def calc_mean_std_all(smile1_file, smile2_file, oh1_file, oh2_file, output_path):
        print("-" * 150)
        print("Calculating input mean and std\n")

        smile1 = pd.read_csv(smile1_file, header=None).to_numpy()
        smile2 = pd.read_csv(smile2_file, header=None).to_numpy()
        oh1 = pd.read_csv(oh1_file, header=None).to_numpy()
        oh2 = pd.read_csv(oh2_file, header=None).to_numpy()

        smile1_mean = np.mean(smile1, axis=0)
        smile1_std = np.std(smile1, axis=0)
        smile2_mean = np.mean(smile2, axis=0)
        smile2_std = np.std(smile2, axis=0)
        oh1_mean = np.mean(oh1, axis=0)
        oh1_std = np.std(oh1, axis=0)
        oh2_mean = np.mean(oh2, axis=0)
        oh2_std = np.std(oh2, axis=0)

        smile1_std_mean = np.mean(np.std(smile1, axis=0))
        smile2_std_mean = np.mean(np.std(smile2, axis=0))
        oh1_std_mean = np.mean(np.std(oh1, axis=0))
        oh2_std_mean = np.mean(np.std(oh2, axis=0))

        print("Smile1_std_mean = ", smile1_std_mean)
        print("Smile2_std_mean = ", smile2_std_mean)
        print("oh1_std_mean = ", oh1_std_mean)
        print("oh2_std_mean = ", oh2_std_mean)

        # Open the CSV file in write mode and create a CSV writer
        with open(output_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([f"Calculating {CURR_DATA_PATH} input mean and std:"])
            writer.writerow([f"smile1_mean: {smile1_mean}"])
            writer.writerow([f"smile1_std: {smile1_std}"])
            writer.writerow([f"smile2_mean: {smile2_mean}"])
            writer.writerow([f"smile2_std: {smile2_std}"])
            writer.writerow([f"oh1_mean: {oh1_mean}"])
            writer.writerow([f"oh1_std: {oh1_std}"])
            writer.writerow([f"oh2_mean: {oh2_mean}"])
            writer.writerow([f"oh2_std: {oh2_std}\n"])

            writer.writerow([f"Smile1_std_mean = {smile1_std_mean}"])
            writer.writerow([f"Smile2_std_mean = {smile2_std_mean}"])
            writer.writerow([f"oh1_std_mean = {oh1_std_mean}"])
            writer.writerow([f"oh2_std_mean = {oh2_std_mean}\n"])

        return [smile1_mean, smile2_mean, oh1_mean, oh2_mean]

    @staticmethod
    def calc_dist_pairs(smile1_mean, smile2_mean, oh1_mean, oh2_mean, output_path):
        print("-" * 150)
        print("Distance between smiles = ", np.linalg.norm(smile1_mean - smile2_mean))
        print("Distance between ohs = ", np.linalg.norm(oh1_mean - oh2_mean))
        print("Distance between smiles to ohs =")
        print(np.linalg.norm(smile1_mean - oh1_mean))
        print(np.linalg.norm(smile2_mean - oh1_mean))
        print(np.linalg.norm(smile1_mean - oh2_mean))
        print(np.linalg.norm(smile2_mean - oh2_mean))

        with open(output_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([f"Distance between smiles = {np.linalg.norm(smile1_mean - smile2_mean)}"])
            writer.writerow([f"Distance between ohs = {np.linalg.norm(oh1_mean - oh2_mean)}"])
            writer.writerow([f"Distance between smiles to ohs = {np.linalg.norm(smile1_mean - oh1_mean)}, {np.linalg.norm(smile2_mean - oh1_mean)}, {np.linalg.norm(smile1_mean - oh2_mean)}, {np.linalg.norm(smile2_mean - oh2_mean)}"])


def get_absolute_path(dir_type):
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    parent_dir = os.path.dirname(script_dir)
    return os.path.join(parent_dir, dir_type)


def main():
    parent_dir = os.path.join("Results", "static_videos")
    results_dir = os.path.join(get_absolute_path(parent_dir), CURR_DATA_PATH)

    # create a result folder
    result_path = os.path.join(parent_dir, "model_generators_validation_results")
    os.makedirs(result_path, exist_ok=True)

    smile1_path = os.path.join(results_dir, 'smile1.csv')
    smile2_path = os.path.join(results_dir, 'smile2.csv')
    oh1_path = os.path.join(results_dir, 'oh1.csv')
    oh2_path = os.path.join(results_dir, 'oh2.csv')

    output_path = os.path.join(result_path, CURR_DATA_PATH + ".csv")

    [smile1_mean, smile2_mean, oh1_mean, oh2_mean] = GenValidate.calc_mean_std_all(smile1_path, smile2_path, oh1_path, oh2_path, output_path)
    GenValidate.calc_dist_pairs(smile1_mean, smile2_mean, oh1_mean, oh2_mean, output_path)


if __name__ == '__main__':
    main()

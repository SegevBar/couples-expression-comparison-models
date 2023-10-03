import os
import numpy as np
import torch

from Metrics.metrics_utils.data_visualization.generate_histogram import generate_double_histogram
from Metrics.metrics_utils.metrics_utils import find_min_dist, find_min_dist_cuda
from Metrics.metrics_utils.statistical_tests import perform_mannwhitneyu_test


# CUDA device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def _run_metric_couple(part1, part2, threshold=1):
    part1 = torch.tensor(part1, dtype=torch.float64, device=device)
    part2 = torch.tensor(part2, dtype=torch.float64, device=device)

    if torch.cuda.is_available():
        min_distances = find_min_dist_cuda(part1, part2)
    else:
        min_distances = torch.zeros(len(part1), dtype=torch.float64, device=device)
        for i, vector in enumerate(part1):
            min_distances[i] = find_min_dist(vector, part2)

    return min_distances


def _get_mean_by_threshold(min_distances, threshold=1.0):
    sorted_values, sorted_indices = torch.sort(min_distances)
    num_to_keep = int(len(sorted_values) * threshold)

    return torch.mean(sorted_values[:num_to_keep])


def _create_histogram(results1, results2, output_path, output_title):
    generate_double_histogram(results1, results2, output_title, output_path)


class AvgMinDist:
    @staticmethod
    def run_metric(coupling, strangers, participants_exp_rep, result_path, thresholds=(0.9)):
        print("-" * 150)
        print("\nRunning Average Minimal Distance Metric")

        couples_results = np.zeros((1, len(coupling)))
        strangers_results = np.zeros((1, len(strangers)))
        for i in range(len(coupling)):
            print("calculating couple", coupling[i])
            res = _run_metric_couple(participants_exp_rep[str(coupling[i][0])],
                                     participants_exp_rep[str(coupling[i][1])])
            for j in range(1):
                couples_results[j][i] = _get_mean_by_threshold(res, 0.9)

        for i in range(len(strangers)):
            print("calculating strangers", strangers[i])
            res = _run_metric_couple(participants_exp_rep[str(strangers[i][0])],
                                     participants_exp_rep[str(strangers[i][1])])
            for j in range(1):
                strangers_results[j][i] = _get_mean_by_threshold(res, 0.9)

        print("\nCalculate statistics:")
        for i in range(1):
            print(f"Case threshold = 0.9:")
            couple_res = couples_results[i]
            strangers_res = strangers_results[i]
            perform_mannwhitneyu_test("Couples", couple_res, "Strangers", strangers_res)

            print("Creating Histogram")
            _create_histogram(couple_res, strangers_res, f"Average {0.9 * 100}% Minimal Distance Histogram",
                              os.path.join(result_path, f"hist_avg_min_dist_{0.9 * 100}.png"))


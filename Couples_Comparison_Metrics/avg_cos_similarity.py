import os
import torch
import numpy as np
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Metrics.metrics_utils.metrics_utils import find_cos_similarity_cuda, find_cos_similarity
from Metrics.metrics_utils.data_visualization.generate_histogram import generate_double_histogram
from Metrics.metrics_utils.statistical_tests import perform_mannwhitneyu_test

# CUDA device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def _run_metric_couple(part1, part2):
    part1 = torch.tensor(part1, dtype=torch.float64, device=device)
    part2 = torch.tensor(part2, dtype=torch.float64, device=device)

    if torch.cuda.is_available():
        cos_similarities = find_cos_similarity_cuda(part1, part2)
    else:
        cos_similarities = torch.zeros(len(part1), dtype=torch.float64, device=device)
        for i, vector in enumerate(part1):
            cos_similarities[i] = find_cos_similarity(vector, part2)
    return cos_similarities


def _get_mean_by_threshold(cos_similarities, threshold):
    sorted_values, sorted_indices = torch.sort(cos_similarities, descending=True)
    num_to_keep = int(len(sorted_values) * threshold)

    return torch.mean(sorted_values[:num_to_keep])


def _create_histogram(results1, results2, output_title, output_path):
    generate_double_histogram(results1, results2, output_title, output_path)


class AvgCosSim:
    @staticmethod
    def run_metric(coupling, strangers, participants_exp_rep, result_path, threshold):
        print("-" * 150)
        print("\nRunning Average Minimal Cosine Similarity Metric\n")

        couples_results = np.zeros((len(coupling)))
        strangers_results = np.zeros((len(strangers)))
        for i in range(len(coupling)):
            print("calculating couple", coupling[i])
            res = _run_metric_couple(participants_exp_rep[str(coupling[i][0])],
                                                         participants_exp_rep[str(coupling[i][1])])
            couples_results[i] = _get_mean_by_threshold(res, threshold)

        for i in range(len(strangers)):
            print("calculating strangers", strangers[i])
            res = _run_metric_couple(participants_exp_rep[str(strangers[i][0])],
                                                           participants_exp_rep[str(strangers[i][1])])
            strangers_results[i] = _get_mean_by_threshold(res, threshold)

        print("\nCalculate statistics:")
        print(f"Case threshold = {threshold}:")
        perform_mannwhitneyu_test("Couples", couples_results, "Strangers", strangers_results)

        print("Creating Histogram")
        _create_histogram(couples_results, strangers_results, f"Average {threshold * 100}% Cosine Similarity Histogram",
                          os.path.join(result_path, f"hist_avg_cos_sim_{str(threshold * 100)}.png"))


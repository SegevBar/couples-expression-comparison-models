import os
import torch
import numpy as np

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


def _get_mean_by_threshold(cos_similarities, threshold=1.0):
    sorted_values, sorted_indices = torch.sort(cos_similarities, descending=True)
    num_to_keep = int(len(sorted_values) * threshold)

    return torch.mean(sorted_values[:num_to_keep])


def _create_histogram(results1, results2, output_path, output_title):
    generate_double_histogram(results1, results2, output_title, output_path)


class AvgCosSim:
    @staticmethod
    def run_metric(coupling, strangers, participants_exp_rep, result_path, thresholds=(0.9)):
        print("-" * 150)
        print("Running Average Minimal Cosine Similarity Metric\n")

        couples_results = np.zeros((len(thresholds), len(coupling)))
        strangers_results = np.zeros((len(thresholds), len(strangers)))
        for i in range(coupling):
            print("calculating couple", coupling[i])
            res = _run_metric_couple(participants_exp_rep[str(coupling[i][0])],
                                                         participants_exp_rep[str(coupling[i][1])])
            for j in range(len(thresholds)):
                couples_results[j][i] = _get_mean_by_threshold(res, thresholds[j])

        for i in range(strangers):
            print("calculating strangers", strangers[i])
            res = _run_metric_couple(participants_exp_rep[str(strangers[i][0])],
                                                           participants_exp_rep[str(strangers[i][1])])
            for j in range(len(thresholds)):
                strangers_results[j][i] = _get_mean_by_threshold(res, thresholds[j])

        print("\nCalculate statistics:")
        for i in range(len(thresholds)):
            print(f"Case threshold = {thresholds[i]}:")
            couple_res = couples_results[i]
            strangers_res = strangers_results[i]
            perform_mannwhitneyu_test("Couples", couple_res, "Strangers", strangers_res)

            print("Creating Histogram")
            _create_histogram(couple_res, strangers_res, f"Average {thresholds[i] * 100}% Cosine Similarity Histogram",
                              os.path.join(result_path, f"hist_avg_cos_sim_{thresholds[i] * 100}.png"))


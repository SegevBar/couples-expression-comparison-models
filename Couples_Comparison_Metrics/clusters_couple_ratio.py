import os
import torch
import numpy as np

from Metrics.metrics_utils.data_visualization.generate_histogram import generate_double_histogram
from Metrics.metrics_utils.statistical_tests import perform_mannwhitneyu_test
from Metrics.metrics_utils.metrics_utils import perform_dbscan_clustering

# CUDA device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def _run_metric_couple(part1, part2, eps):
    original_sets = [part1, part2]
    combined_data = np.vstack((part1, part2))
    cluster_labels = perform_dbscan_clustering(combined_data, eps)

    cluster_count = [_cluster_count(cluster_labels, cluster_idx, original_sets, combined_data) for cluster_idx in
                      np.unique(cluster_labels)]
    cluster_ratio = np.array([min(set1_count/total_count, set2_count/total_count) for set1_count, set2_count, total_count in cluster_count])
    return np.mean(cluster_ratio)


def _cluster_count(labels, cluster_idx, original_sets, combined_data):
    cluster_elements = combined_data[labels == cluster_idx]
    set1_count = len(set(map(tuple, cluster_elements.tolist())) & set(map(tuple, original_sets[0].tolist())))
    set2_count = len(set(map(tuple, cluster_elements.tolist())) & set(map(tuple, original_sets[1].tolist())))
    total_count = len(cluster_elements)
    return set1_count, set2_count, total_count


def _cluster_centroid(labels, cluster_idx, combined_data):
    cluster_elements = combined_data[labels == cluster_idx]
    centroid = np.mean(cluster_elements, axis=0)
    return centroid


def _create_histogram(results1, results2, output_title, output_path):
    generate_double_histogram(results1, results2, output_title, output_path)


class AvgClusterRatio:
    @staticmethod
    def run_metric(coupling, strangers, participants_exp_rep, result_path, eps):
        print("-" * 150)
        print("\nRunning Cluster Couple Ratio Metric\n")

        couples_results = np.zeros((len(coupling)))
        strangers_results = np.zeros((len(strangers)))

        for i in range(len(coupling)):
            print("calculating couple", coupling[i])
            couples_results[i] = _run_metric_couple(participants_exp_rep[str(coupling[i][0])], participants_exp_rep[str(coupling[i][1])], eps)

        for i in range(len(strangers)):
            print("calculating strangers", strangers[i])
            strangers_results[i] = _run_metric_couple(participants_exp_rep[str(strangers[i][0])], participants_exp_rep[str(strangers[i][1])], eps)

        print("\nCalculate statistics:")
        perform_mannwhitneyu_test("Couples", couples_results, "Strangers", strangers_results)

        print("Creating Histogram")
        _create_histogram(couples_results, strangers_results, "Average eps=2 Cluster Couple Ratio Histogram",
                          os.path.join(result_path, "hist_cluster_ratio_2.png"))



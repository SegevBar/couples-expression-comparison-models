import os
import torch
import numpy as np

from metrics_utils.metrics_utils import find_cos_similarity_cuda, find_cos_similarity
from metrics_utils.data_visualization.generate_histogram import generate_double_histogram
from metrics_utils.statistical_tests import perform_mannwhitneyu_test

# CUDA device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def _pairwise_dbscan_cluster_ratio(part1, part2):
    original_sets = [part1, part2]
    combined_data = np.vstack((part1, part2))
    cluster_labels = perform_dbscan_clustering(combined_data)
    cluster_count = [_cluster_count(cluster_labels, cluster_idx, original_sets, combined_data) for cluster_idx in
                      np.unique(cluster_labels)]
    cluster_ratio = np.array([min(set1_count/total_count, set2_count/total_count) for set1_count, set2_count, total_count in cluster_count])
    # weights = np.array([total_count for set1_count, set2_count, total_count in cluster_count])
    # return np.average(cluster_ratio, weights=weights)
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


def _get_mean_by_threshold(cos_similarities, threshold=1.0):
    sorted_values, sorted_indices = torch.sort(cos_similarities, descending=True)
    num_to_keep = int(len(sorted_values) * threshold)

    return torch.mean(sorted_values[:num_to_keep])


def _create_histogram(results1, results2, output_path, output_title):
    generate_double_histogram(results1, results2, output_title, output_path)


class AvgClusterRatio:
    @staticmethod
    def run_metric(coupling, strangers, participants_exp_rep, result_path, thresholds=(1.0, 0.9, 0.5)):
        print("-" * 150)
        print("Running Cluster Couple Ratio Metric\n")

        couples_results = np.zeros((len(thresholds), len(coupling)))
        strangers_results = np.zeros((len(thresholds), len(strangers)))
        for i in range(coupling):
            print("calculating couple", coupling[i])
            res = _run_metric_couple(participants_exp_rep[str(coupling[i][0])],
                                                         participants_exp_rep[str(coupling[i][1])])
            for j in range(len(thresholds)):
                couples_results[i][j] = _get_mean_by_threshold(res, thresholds[j])

        for i in range(strangers):
            print("calculating strangers", strangers[i])
            res = _run_metric_couple(participants_exp_rep[str(strangers[i][0])],
                                                           participants_exp_rep[str(strangers[i][1])])
            for j in range(len(thresholds)):
                strangers_results[i][j] = _get_mean_by_threshold(res, thresholds[j])

        print("\nCalculate statistics:")
        for i in range(len(thresholds)):
            print(f"Case threshold = {thresholds[i]}:")
            couple_res = couples_results[i]
            strangers_res = strangers_results[i]
            perform_mannwhitneyu_test("Couples", couple_res, "Strangers", strangers_res)

            print("Creating Histogram")
            _create_histogram(couple_res, strangers_res, f"Average {thresholds[i] * 100}% Cosine Similarity Histogram",
                              os.path.join(result_path, f"hist_avg_cos_sim_{thresholds[i] * 100}.png"))




def _run_metric_couple(part1, part2):
    result = {}
    original_sets = [part1, part2]

    combined_data = _combine_couple_datasets(part1, part2)
    cluster_labels = _apply_dbscan_clustering_to_combined_dataset(combined_data)
    cluster_ratios = [_cluster_ratio(cluster_labels, cluster_idx, original_sets) for cluster_idx in
                      np.unique(cluster_labels)]

    cluster_size_to_print = 100
    for i, (set1_ratio, set2_ratio, total_count) in enumerate(cluster_ratios):
        result[i] = {
            "centroid": _cluster_centroid(cluster_labels, i),
            "Set1_ratio": set1_ratio / total_count,
            "Set2_ratio": set2_ratio / total_count,
            "num_of_points": total_count
        }
    return result


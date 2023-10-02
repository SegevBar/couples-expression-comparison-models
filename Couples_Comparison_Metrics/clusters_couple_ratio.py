import os
import torch
import numpy as np

from Metrics.metrics_utils.data_visualization.generate_histogram import generate_double_histogram
from Metrics.metrics_utils.statistical_tests import perform_mannwhitneyu_test
from Metrics.model_validation.pairwise_avg_min_dist import pairwise_distances
from Metrics.metrics_utils.metrics_utils import perform_dbscan_clustering
from Metrics.metrics_utils.data_utils import get_all_participants

# CUDA device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def _run_metric_couple(part1, part2, eps=1.0):
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


def _create_histogram(results1, results2, output_path, output_title):
    generate_double_histogram(results1, results2, output_title, output_path)


def _find_eps(all_part, participants_exp_rep):
    print("Calculating DBSCAN epsilon")
    n = len(all_part)
    res = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i == j:
                all_data = participants_exp_rep[str(all_part[i])]
                tmp = pairwise_distances(all_data[:len(all_data) // 2], all_data[len(all_data) // 2:])
            else:
                tmp = pairwise_distances(participants_exp_rep[str(all_part[i])],
                                          participants_exp_rep[str(all_part[j])])
            res[i][j] = torch.mean(tmp)
    return float(np.mean(res))


class AvgClusterRatio:
    @staticmethod
    def run_metric(coupling, strangers, participants_exp_rep, result_path, factor=(1.0, 10.0)):
        print("-" * 150)
        print("Running Cluster Couple Ratio Metric\n")
        eps = _find_eps(get_all_participants(coupling), participants_exp_rep)

        couples_results = np.zeros((len(factor), len(coupling)))
        strangers_results = np.zeros((len(factor), len(strangers)))

        for i in range(len(factor)):
            epsilon = eps*factor[i]
            for j in range(coupling):
                print("calculating couple", coupling[i])
                couples_results[i][j] = _run_metric_couple(participants_exp_rep[str(coupling[j][0])], participants_exp_rep[str(coupling[j][1])], epsilon)

            for j in range(strangers):
                print("calculating strangers", strangers[i])
                strangers_results[i][j] = _run_metric_couple(participants_exp_rep[str(strangers[j][0])], participants_exp_rep[str(strangers[j][1])], epsilon)

        print("\nCalculate statistics:")
        for i in range(len(factor)):
            print(f"Case eps*{factor[i]}:")
            couple_res = couples_results[i]
            strangers_res = strangers_results[i]
            perform_mannwhitneyu_test("Couples", couple_res, "Strangers", strangers_res)

            print("Creating Histogram")
            _create_histogram(couple_res, strangers_res, f"Average eps*{factor[i]} Cosine Similarity Histogram",
                              os.path.join(result_path, f"hist_avg_cos_sim_eps{factor[i]}.png"))



import os
import numpy as np
from metrics_utils.metrics_utils import perform_dbscan_clustering
from metrics_utils.data_visualization.generate_heatmap import generate_heatmap


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


class DbscanCluster:
    @staticmethod
    def run_metric(all_part, participants_exp_rep, result_path):
        print("-" * 150)
        print("Running dbscan clustering couples ratio metric\n")

        n = len(all_part)
        results = np.zeros((n, n))

        count = 0
        for i in range(n):
            for j in range(n):
                count += 1
                print(f"calculating pair {count}/{n ** 2}: {all_part[i]} - {all_part[j]}")

                if i == j:
                    all_data = participants_exp_rep[str(all_part[i])]
                    res = _pairwise_dbscan_cluster_ratio(all_data[:len(all_data) // 2], all_data[len(all_data) // 2:])
                else:
                    res = _pairwise_dbscan_cluster_ratio(participants_exp_rep[str(all_part[i])],
                                           participants_exp_rep[str(all_part[j])])
                results[i][j] = res

        print("Creating DBSCAN Clustering Couples Ratio Heatmaps")
        generate_heatmap(results, "DBSCAN Clustering Couples Ratio Heatmap", os.path.join(result_path, "heatmap_dbscan_cluster_ratio.png"))


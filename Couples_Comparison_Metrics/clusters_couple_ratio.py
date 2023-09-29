import numpy as np
from sklearn.cluster import DBSCAN
import pandas as pd
import matplotlib.pyplot as plt


# Step 1: Combine the two sets of vectors into a single dataset
def _combine_couple_datasets(set_path1, set_path2):
    # Extract columns for set1 and set2
    set1 = set_path1.values
    set2 = set_path2.values
    combined_data = np.vstack((set1, set2))
    print("Size of combined_data:", combined_data.shape)
    return combined_data


# Step 2: Apply DBSCAN clustering to the combined dataset
def _apply_dbscan_clustering_to_combined_dataset(combined_data):
    print("Clustering")
    eps = 1.0  # Maximum distance between points in the same cluster
    min_samples = 10  # Minimum number of samples in a cluster
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    cluster_labels = dbscan.fit_predict(combined_data)
    return cluster_labels


# Step 3: Calculate the ratio of data points from each original set within each cluster
def _cluster_ratio(labels, cluster_idx, original_sets, combined_data):
    cluster_elements = combined_data[labels == cluster_idx]
    set1_count = len(set(map(tuple, cluster_elements.tolist())) & set(map(tuple, original_sets[0].tolist())))
    set2_count = len(set(map(tuple, cluster_elements.tolist())) & set(map(tuple, original_sets[1].tolist())))
    total_count = len(cluster_elements)
    return set1_count, set2_count, total_count


# Step 4: Calculate the centroid of each cluster for clusters larger than 50
def _cluster_centroid(labels, cluster_idx, combined_data):
    cluster_elements = combined_data[labels == cluster_idx]
    centroid = np.mean(cluster_elements, axis=0)
    return centroid


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

class ClusterCoupleRatio:
    @staticmethod
    def run_metric(coupling, strangers, participants_exp_rep):
        print("Running Cluster Couple Ratio Metric")

        couples_results = {}
        strangers_results = {}
        for couple in coupling:
            couples_results[couple] = _run_metric_couple(participants_exp_rep[couple[0]], participants_exp_rep[couple[1]])
        for couple in strangers:
            strangers_results.update(
                {couple: {(_run_metric_couple(participants_exp_rep[couple[0]], participants_exp_rep[couple[1]]))}})



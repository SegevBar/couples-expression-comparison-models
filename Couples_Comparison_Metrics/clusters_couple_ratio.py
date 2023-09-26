import numpy as np
from sklearn.cluster import DBSCAN
import pandas as pd





# Step 1: Combine the two sets of vectors into a single dataset
def _combineCoupleDatasets(set_path1, set_path2):

    df_set1 = pd.read_csv(set_path1, header=None)
    df_set2 = pd.read_csv(set_path2, header=None)

    # Extract columns for set1 and set2
    set1 = df_set1.values
    set2 = df_set2.values
    combined_data = np.vstack((set1, set2))
    print("Size of combined_data:", combined_data.shape)

# Step 2: Apply DBSCAN clustering to the combined dataset
def _applyDBSCANclusteringToCombinedDataset():
    print("Clustering")
    eps = 1.0  # Maximum distance between points in the same cluster
    min_samples = 10  # Minimum number of samples in a cluster
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    cluster_labels = dbscan.fit_predict(combined_data)

# Step 3: Calculate the ratio of data points from each original set within each cluster
def _cluster_ratio(labels, cluster_idx, original_sets):
    cluster_elements = combined_data[labels == cluster_idx]
    set1_count = len(set(map(tuple, cluster_elements.tolist())) & set(map(tuple, original_sets[0].tolist())))
    set2_count = len(set(map(tuple, cluster_elements.tolist())) & set(map(tuple, original_sets[1].tolist())))
    total_count = len(cluster_elements)
    return set1_count, set2_count, total_count

# Step 4: Calculate the centroid of each cluster for clusters larger than 50
def _cluster_centroid(labels, cluster_idx):
    cluster_elements = combined_data[labels == cluster_idx]
    centroid = np.mean(cluster_elements, axis=0)
    return centroid

def run_metric(coupling):
    # Print label and ratios for clusters smaller than 50
    original_sets = [set1, set2]
    cluster_ratios = [cluster_ratio(cluster_labels, cluster_idx, original_sets) for cluster_idx in np.unique(cluster_labels)]


    cluster_size_to_print = 100
    for i, (set1_ratio, set2_ratio, total_count) in enumerate(cluster_ratios):
        if total_count > cluster_size_to_print:
            centroid = cluster_centroid(cluster_labels, i)
            print(f"Cluster {i}: Set1 ratio: {set1_ratio / total_count:.4f}, Set2 ratio: {set2_ratio / total_count:.4f}, Number of Points: {total_count}")
            print(f"Cluster {i}: Centroid: {centroid}")
        else:
            print(f"Cluster {i}: Set1 ratio: {set1_ratio/total_count:.4f}, Set2 ratio: {set2_ratio/total_count:.4f}, Number of Points: {total_count}")

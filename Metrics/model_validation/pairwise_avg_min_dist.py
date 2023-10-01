import os

import torch
import numpy as np

from metrics_utils.data_visualization.generate_heatmap import generate_heatmap
from metrics_utils.metrics_utils import find_min_dist_cuda, find_min_dist


# CUDA device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def _pairwise_distances(part1, part2):
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


def _create_heatmap(results, output_path, output_title):
    generate_heatmap(results, output_title, output_path)


class PairwiseAvgMinDist:
    @staticmethod
    def run_metric(all_part, participants_exp_rep, result_path):
        print("-" * 150)
        print("\nRunning pairwise average minimal distance metric")

        n = len(all_part)
        results_100 = np.zeros((n, n))
        results_50 = np.zeros((n, n))
        results_10 = np.zeros((n, n))

        count = 0
        for i in range(n):
            for j in range(n):
                count += 1
                print(f"calculating pair {count}/{n ** 2}: {all_part[i]} - {all_part[j]}")
                if i == j:
                    all_data = participants_exp_rep[str(all_part[i])]
                    res = _pairwise_distances(all_data[:len(all_data)//2], all_data[len(all_data)//2:])
                else:
                    res = _pairwise_distances(participants_exp_rep[str(all_part[i])], participants_exp_rep[str(all_part[j])])
                results_100[i][j] = _get_mean_by_threshold(res, 1.0)
                results_50[i][j] = _get_mean_by_threshold(res, 0.5)
                results_10[i][j] = _get_mean_by_threshold(res, 0.1)

        print("Creating Heatmaps")
        _create_heatmap(results_100, os.path.join(result_path, "heatmap_avg_min_dist_100.png"),
                        "Average All Minimal Distance Heatmap")
        _create_heatmap(results_50, os.path.join(result_path, "heatmap_avg_min_dist_50.png"),
                        "Average 50% Minimal Distance Heatmap")
        _create_heatmap(results_10, os.path.join(result_path, "heatmap_avg_min_dist_10.png"),
                        "Average 10% Minimal Distance Heatmap")


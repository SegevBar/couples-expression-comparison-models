
import os

import torch
import numpy as np

from metrics_utils.data_visualization.generate_heatmap import generate_heatmap
from metrics_utils.metrics_utils import find_min_cosine


# CUDA device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def pairwise_distances(part1, part2, threshold=1):
    part1 = torch.tensor(part1, dtype=torch.float64, device=device)
    part2 = torch.tensor(part2, dtype=torch.float64, device=device)

    min_distances = torch.zeros(len(part1), dtype=torch.float64, device=device)
    for i, vector in enumerate(part1):
        min_distances[i] = find_min_cosine(vector, part2)

    sorted_values, sorted_indices = torch.sort(min_distances)
    num_to_keep = int(len(sorted_values) * threshold)

    return torch.mean(sorted_values[:num_to_keep])


class PairwiseAvgMinCos:
    @staticmethod
    def run_metric(all_part, participants_exp_rep, result_path):
        print("\nRunning pairwise average minimal cosine similarity metric")

        n = len(all_part)
        results = np.zeros((n, n))

        for i in range(n):
            for j in range(n):
                print(f"calculating pair: ${participants_exp_rep[str(all_part[i])]} - {participants_exp_rep[str(all_part[j])]}")
                if i == j:
                    all_data = participants_exp_rep[str(all_part[i])]
                    results[i][j] = pairwise_distances(all_data[:len(all_data)//2], all_data[len(all_data)//2:], threshold=1)
                else:
                    results[i][j] = pairwise_distances(participants_exp_rep[str(all_part[i])], participants_exp_rep[str(all_part[j])], threshold=1)

        print("Results: ", results)

        print("Creating Heatmap")
        output_path = os.path.join(result_path, "heatmap_avg_min_cos.png")
        output_title = "Average Minimal Cosine Heatmap"
        generate_heatmap(results, output_title, output_path)

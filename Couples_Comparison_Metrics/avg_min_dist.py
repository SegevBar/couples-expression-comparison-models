import os
import numpy as np
import torch
from scipy.spatial.distance import cdist
from generate_histogram import generate_double_histogram
from scipy.stats import mannwhitneyu
from scipy import stats

# CUDA device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def _find_closest_exp(vector, part2):
    vector = vector.clone().detach()
    part2 = part2.clone().detach()

    distances = cdist(vector.unsqueeze(0), part2, metric='euclidean')
    distances = torch.tensor(distances, dtype=torch.float64, device=device)
    min_distance = torch.min(distances)
    return min_distance.item()


def _run_metric_couple(part1, part2):
    part1 = torch.tensor(part1, dtype=torch.float64, device=device)
    part2 = torch.tensor(part2, dtype=torch.float64, device=device)

    min_distances1 = torch.zeros(len(part1), dtype=torch.float64, device=device)
    for i, vector in enumerate(part1):
        min_distances1[i] = _find_closest_exp(vector, part2)

    min_distances2 = torch.zeros(len(part2), dtype=torch.float64, device=device)
    for i, vector in enumerate(part2):
        min_distances2[i] = _find_closest_exp(vector, part1)

    mean_min_distances1 = torch.mean(min_distances1)
    mean_min_distances2 = torch.mean(min_distances2)

    return (mean_min_distances1.item() + mean_min_distances2.item()) / 2.0


class AvgMinDist:
    @staticmethod
    def run_metric(coupling, strangers, participants_exp_rep, result_path):
        print("\nRunning Average Minimal Distance Metric")

        couples_results = {}
        strangers_results = {}
        for couple in coupling:
            print("calculating couple", couple)
            couples_results[couple] = _run_metric_couple(participants_exp_rep[str(couple[0])],
                                                         participants_exp_rep[str(couple[1])])
        for couple in strangers:
            print("calculating strangers", couple)
            strangers_results[couple] = _run_metric_couple(participants_exp_rep[str(couple[0])],
                                                           participants_exp_rep[str(couple[1])])

        #print("Couples: ", couples_results.values(), sum(couples_results.values())/len(couples_results.values()))
        #print("Strangers: ", strangers_results.values(), sum(strangers_results.values())/len(strangers_results.values()))

        print("Calculate statistics:")
        couple_res = [val for val in couples_results.values()]
        strangers_res = [val for val in strangers_results.values()]

        print("Couples (mean, std): ", np.mean(couple_res), " , ", np.std(couple_res))
        print("Strangers (mean, std): ", np.mean(strangers_res), " , ", np.std(strangers_res))

        # Perform the Mann-Whitney U test
        statistic, p_value = mannwhitneyu(couple_res, strangers_res)
        alpha = 0.05
        print("mann-whitneyu statistic: ", statistic)
        print(f"P-Value = {p_value},  alpha = {alpha}")
        if p_value < alpha:
            print("Reject the null hypothesis: The distributions are different.")
        else:
            print("Fail to reject the null hypothesis: The distributions are similar.")

        # Perform a two-sample t-test
        t_statistic, p_value = stats.ttest_ind(couple_res, strangers_res)
        print("t-statistic: ", t_statistic)
        print(f"P-Value = {p_value},  alpha = {alpha}")
        if p_value < alpha:
            print("Reject the null hypothesis: The means are significantly different.")
        else:
            print("Fail to reject the null hypothesis: The means are not significantly different.")


        print("Creating Histogram")
        output_path = os.path.join(result_path, "hist_avg_min_dist.png")
        generate_double_histogram(list(couples_results.values()), list(strangers_results.values()), output_path)


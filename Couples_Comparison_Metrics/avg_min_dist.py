from scipy.spatial.distance import euclidean
import numpy as np

from generate_histogram import generate_double_histogram


def _find_closest_exp(vector, part2):
    min_distance = float('inf')
    for index, row in enumerate(part2):
        distance = euclidean(vector, row)
        min_distance = min(min_distance, distance)
    return min_distance


def _run_metric_couple(part1, part2):
    min_distances1 = np.zeros(len(part1), dtype=np.float64)
    for i, vector in enumerate(part1):
        min_distances1[i] = _find_closest_exp(vector, part2)
    print(min_distances1)

    min_distances2 = np.zeros(len(part2), dtype=np.float64)
    for i, vector in enumerate(part2):
        min_distances2[i] = _find_closest_exp(vector, part1)
    print(min_distances2)

    return np.mean([np.mean(min_distances1), np.mean(min_distances2)])


class AvgMinDist:
    @staticmethod
    def run_metric(coupling, strangers, participants_exp_rep):
        print("Running Average Minimal Distance Metric")

        couples_results = {}
        strangers_results = {}
        for couple in coupling:
            print("strated ", couple)
            couples_results[couple] = _run_metric_couple(participants_exp_rep[str(couple[0])], participants_exp_rep[str(couple[1])])
        for couple in strangers:
            print("strated ", couple)
            strangers_results[couple] = _run_metric_couple(participants_exp_rep[str(couple[0])], participants_exp_rep[str(couple[1])])

        print(couples_results.values(), strangers_results.values())
        generate_double_histogram(couples_results.values(), strangers_results.values())


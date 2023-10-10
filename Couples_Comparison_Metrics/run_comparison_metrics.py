import argparse
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from avg_cos_similarity import AvgCosSim
from run_tsne import TSNE
from Metrics.metrics_utils.data_utils import *
from avg_min_dist import AvgMinDist
from clusters_couple_ratio import AvgClusterRatio

METRICS = {
    "avg_min_dist": AvgMinDist,
    "avg_cos_similarity": AvgCosSim,
    "cluster_couple_ratio": AvgClusterRatio,
    "tsne": TSNE
}


def get_absolute_path(dir_type):
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    parent_dir = os.path.dirname(script_dir)
    return os.path.join(parent_dir, dir_type)


def parse_key_value_pairs(s):
    pairs = s.split()
    metrics = []
    for pair in pairs:
        key, value = pair.split(":")
        if value == "True":
            metrics.append(key)
    return metrics


def main(args):
    results_dir = get_absolute_path("Results")
    csvs_path = os.path.join(results_dir, args.resultpath)
    run_metrics = args.metrics
    coupling_path = os.path.join(csvs_path, 'coupling.csv')

    # create a result folder
    result_path = os.path.join(csvs_path, "comparison_metrics_results")
    os.makedirs(result_path)

    # load data - expressions representations and coupling
    participants_exp_rep = load_exp_rep(csvs_path)
    couples = get_couples(coupling_path)
    strangers = get_strangers(couples)

    # compute metrics
    for metric in run_metrics:
        if metric == "avg_min_dist":
            AvgMinDist.run_metric(couples, strangers, participants_exp_rep, result_path, threshold=0.9)
        elif metric == "avg_cos_similarity":
            AvgCosSim.run_metric(couples, strangers, participants_exp_rep, result_path, threshold=0.9)
        elif metric == "cluster_couple_ratio":
            AvgClusterRatio.run_metric(couples, strangers, participants_exp_rep, result_path, eps=2.0)
        if metric != "tsne":
            METRICS[metric].run_metric(participants_exp_rep, result_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='defining comparison metrics to run')
    parser.add_argument('-r', '--resultpath', type=str, help='name of directory containing the expressions csvs')
    parser.add_argument('--metrics', type=parse_key_value_pairs)
    main(parser.parse_args())

import argparse

from avg_min_dist import AvgMinDist
from clusters_couple_ratio import ClusterCoupleRatio
from data_utils import *


METRICS = {
    "avg_min_dist": AvgMinDist,
    "cluster_couple_ratio": ClusterCoupleRatio
}

def parse_key_value_pairs(s):
    pairs = s.split()
    metrics = []
    for pair in pairs:
        key, value = pair.split(":")
        if bool(value):
            metrics.append(key)
    return metrics


def main(args):
    results_dir = get_absolute_path("Results")
    csvs_path = os.path.join(results_dir, args.resultpath)
    run_metrics = args.metrics
    coupling_path = os.path.join(csvs_path, 'coupling.csv')
    print(csvs_path, run_metrics, coupling_path)

    # load data - expressions representations and coupling
    participants_exp_rep = load_exp_rep(csvs_path)
    couples = get_couples(coupling_path)

    print(run_metrics)
    for metric in run_metrics:
        METRICS[metric].run_metric(couples, participants_exp_rep)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='defining comparison metrics to run')
    parser.add_argument('-r', '--resultpath', type=str, help='name of directory containing the expressions csvs')
    parser.add_argument('--metrics', type=parse_key_value_pairs)
    main(parser.parse_args())

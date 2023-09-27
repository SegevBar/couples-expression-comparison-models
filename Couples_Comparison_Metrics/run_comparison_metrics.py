import argparse
from data_utils import *


def main(args):
    cluster_couple_ratio = args.clusters
    euclidean_average = args.euclidean
    csvs_path = args.resultpath
    coupling_path = os.path.join(csvs_path, 'coupling.csv')

    # load data - expressions representations and coupling
    participants_exp_rep = load_exp_rep(csvs_path)
    couples = get_couples(coupling_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='defining comparison metrics to run')
    parser.add_argument('-r', '--resultpath', type=str, help='name of directory containing the expressions csvs')
    parser.add_argument('-d', '--datapath', type=str, help='name of the directory containing the data, specifically the coupling.csv')
    parser.add_argument('--clusters', default=False, help='defines the running status of cluster_couple_ratio metric')
    parser.add_argument('--euclidean', default=False, help='defines the running status of euclidean_average metric')
    main(parser.parse_args())

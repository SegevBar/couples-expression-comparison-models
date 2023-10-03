from model_validation.tsne import TsneAll
from model_validation.pairwise_cluster_ratio import DbscanCluster
from model_validation.pairwise_avg_cos_similarity import PairwiseAvgMinCos
from model_validation.pairwise_avg_min_dist import PairwiseAvgMinDist
from metrics_utils.data_utils import *


CURR_DATA_PATH = "spectre"


def get_absolute_path(dir_type):
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    parent_dir = os.path.dirname(script_dir)
    return os.path.join(parent_dir, dir_type)


def main():
    results_dir = os.path.join(get_absolute_path("Results"), CURR_DATA_PATH)
    coupling_path = os.path.join(results_dir, 'coupling.csv')

    # create a result folder
    result_path = os.path.join(results_dir, "model_metric_validation_results")
    os.makedirs(result_path, exist_ok=True)

    # load data - expressions representations and coupling
    participants_exp_rep = load_exp_rep(results_dir)
    all_exp_rep, part_labels = get_all_exp_rep_and_label(participants_exp_rep)

    couples = get_couples(coupling_path)
    all_part = get_all_participants(couples)
    sample_couple, couple_labels = get_couple_exp_rep_and_label(participants_exp_rep, couples[0][0], couples[0][1])

    # run metrics
    # TsneAll.run_metric_couple(sample_couple, couple_labels, result_path)
    TsneAll.run_metric(all_exp_rep, part_labels, result_path)
    PairwiseAvgMinDist.run_metric(all_part, participants_exp_rep, result_path)
    PairwiseAvgMinCos.run_metric(all_part, participants_exp_rep, result_path)
    DbscanCluster.run_metric(all_part, participants_exp_rep, result_path)


if __name__ == '__main__':
    main()

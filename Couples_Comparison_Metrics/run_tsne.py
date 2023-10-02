import os

from Metrics.metrics_utils.data_utils import get_all_exp_rep_and_label
from Metrics.metrics_utils.data_visualization.generate_tsne import generate_tsne


def tsne_couple(data, part_labels, result_path):
    print("\nRunning t-SNE metric on couple")
    output_path = os.path.join(result_path, "couple_tsne.png")
    output_title = "Couples Expressions t-SNE"

    generate_tsne(data, output_title, output_path, part_labels)


class TSNE:
    @staticmethod
    def run_metric_all(data, result_path):
        print("-" * 150)
        print(f"\nRunning t-SNE type: {type}")

        all_exp_rep, part_labels = get_all_exp_rep_and_label(data)
        output_path = os.path.join(result_path, "all_points_tsne.png")
        output_title = "All Expressions t-SNE"

        generate_tsne(all_exp_rep, output_title, output_path, part_labels)


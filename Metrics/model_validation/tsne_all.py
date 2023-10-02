import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from metrics_utils.data_visualization.generate_tsne import generate_tsne


class TsneAll:
    @staticmethod
    def run_metric(all_exp_rep, part_labels, result_path):
        print("-" * 150)
        print("Running t-SNE metric\n")
        output_path = os.path.join(result_path, "all_points_tsne.png")
        output_title = "All Expressions t-SNE"

        generate_tsne(all_exp_rep, output_title, output_path, part_labels)

    @staticmethod
    def run_metric_couple(couple_exp_rep, part_labels, result_path):
        print("\nRunning t-SNE metric on couple")
        output_path = os.path.join(result_path, "couple_tsne.png")
        output_title = "Couples Expressions t-SNE"

        generate_tsne(couple_exp_rep, output_title, output_path, part_labels)

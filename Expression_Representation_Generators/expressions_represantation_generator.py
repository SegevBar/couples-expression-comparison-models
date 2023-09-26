import os
import csv
import argparse
from datetime import datetime


def get_absolute_path(dir_type):
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    parent_dir = os.path.dirname(script_dir)
    return os.path.join(parent_dir, dir_type)


def main(args):
    print(args.typegenerator)
    data_dir = get_absolute_path("Data")
    results_dir = get_absolute_path("Results")
    print(data_dir, results_dir)

    curr_result_path = os.path.join(results_dir, args.resultpath)
    print(curr_result_path)

    # init chosen generator
    if args.typegenerator == "EMOCA":
        from EMOCA.emoca_expressions_represantation_generator import EmocaExpGenerator
        generator = EmocaExpGenerator
    elif args.typegenerator == "SPECTRE":
        from SPECTRE.spectre_expressions_represantation_generator import SpectreExpGenerator
        generator = SpectreExpGenerator
    elif args.typegenerator == "DECA":
        from DECA.deca_expressions_represantation_generator import DecaExpGenerator
        generator = DecaExpGenerator

    for foldername in os.listdir(data_dir):
        print(foldername)
        folder_path = os.path.join(data_dir, foldername)

        if os.path.isdir(folder_path):
            all_expressions_representations = []

            for filename in os.listdir(folder_path):
                if filename.endswith('.mp4'):
                    video_path = os.path.join(folder_path, filename)
                    curr_expressions_representations = generator(video_path).generate_expressions_representation()
                    all_expressions_representations = all_expressions_representations + curr_expressions_representations

            # Save outputs to CSV
            csv_filename = os.path.join(curr_result_path, foldername + ".csv")
            with open(csv_filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(all_expressions_representations)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='expressions represantation generator')
    parser.add_argument('-t', '--typegenerator', default='SPECTRE', type=str,
                        help='type of expression representation generator')
    parser.add_argument('-r', '--resultpath', type=str, help='name of csvs result folder')
    main(parser.parse_args())

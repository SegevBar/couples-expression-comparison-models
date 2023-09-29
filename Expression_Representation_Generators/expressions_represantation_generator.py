import os
import argparse
import numpy as np


def get_absolute_path(dir_type):
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    parent_dir = os.path.dirname(script_dir)
    return os.path.join(parent_dir, dir_type)


def main(args):
    data_dir = get_absolute_path("Data")
    results_dir = get_absolute_path("Results")

    curr_result_path = os.path.join(results_dir, args.resultpath)
    print(curr_result_path, data_dir)

    coupling = {}
    coupling_path = os.path.join(curr_result_path, "coupling.csv")

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

    for filename in os.listdir(data_dir):
        if filename.endswith(".mp4"):
            print("-"*100)
            print(f"Current video: {filename}")

            # get current user_id and it's couple_id
            parts = filename.split("_")
            user_id = parts[0]
            couple_id = parts[1]

            # find couples
            if not coupling.get(couple_id):
                coupling[couple_id] = set()
            coupling[couple_id].add(user_id)

            # apply expression representation generator
            video_path = os.path.join(data_dir, filename)
            curr_expressions_representations = generator(video_path).generate_expressions_representation()

            # save expression representation to csv file
            csv_filename = os.path.join(curr_result_path, user_id + ".csv")
            with open(csv_filename, 'a') as file:
                np.savetxt(file, curr_expressions_representations, delimiter=',')

    # save coupling
    np.savetxt(coupling_path, np.array([list(value) for value in coupling.values()]), delimiter=',', fmt='%s')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='expressions represantation generator')
    parser.add_argument('-t', '--typegenerator', default='SPECTRE', type=str,
                        help='type of expression representation generator')
    parser.add_argument('-r', '--resultpath', type=str, help='name of csvs result folder')
    main(parser.parse_args())

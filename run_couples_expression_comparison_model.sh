#!/bin/bash
export TZ="Israel"

# Get project setup from configuration file
source config.cfg

current_exp_rep_generator=$EXP_REP_GENERATOR
conda_env="${current_exp_rep_generator,,}"

## Uplaod your data manualy to couples_expression_comparison_models\Data folder
answer_data=""
while [[ ! "$answer_data" =~ ^[YyNn]$ ]]; do
    read -p "Please make sure your data is saved to couples_expression_comparison_models\Data folder. Press y to continue " answer_data
    if [[ ! "$answer_data" =~ ^[YyNn]$ ]]; then
        echo "Invalid input! Please answer with y."
    fi
done
if [[ "$answer_data" =~ ^[Yy]$ ]]; then
    echo "Starting data processing."
else
    echo "Terminating program"
    exit 1
fi

# Creating a result folder for current run
current_date=$(date +"%Y%m%d_%H%M")
result_folder_name="results_${current_date}_${current_exp_rep_generator}"
mkdir "Results/$result_folder_name"
echo "Folder '$result_folder_name' created."

echo "Generating expressions represantations CSVS"
eval "$(conda shell.bash hook)"
conda activate $conda_env
echo "activated $conda_env conda env"
cd Expression_Representation_Generators
python expressions_represantation_generator.py -t $current_exp_rep_generator -r $result_folder_name

# Run Comparisons Metrics
echo "Calculating Metrics:"
cd ../Couples_Comparison_Metrics
python run_comparison_metrics.py -r "spectre" --metrics "avg_min_dist:${AVERAGE_MINIMAL_DISTANCE} avg_cos_similarity:${AVERAGE_COSINE_SIMILARITY} cluster_couple_ratio:${CLUSTER_COUPLE_RATIO} tsne"${TSNE}"

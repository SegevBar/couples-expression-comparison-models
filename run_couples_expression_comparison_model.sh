#!/bin/bash

# Get project setup from configuration file
source config.cfg

current_exp_rep_generator=$EXP_REP_GENERATOR
conda_env="${current_exp_rep_generator,,}"

# Uplaod your data manualy to couples_expression_comparison_models\Data folder
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
folder_name="Results/${current_exp_rep_generator}_${current_date}"
mkdir "$folder_name"
echo "Folder '$folder_name' created."

echo "Generating expressions represantations CSVS"
eval "$(conda shell.bash hook)"
conda activate $conda_env
python expressions_represantation_generator.py


# Run Coparisons Matrics
echo "Calculating Matrics:"

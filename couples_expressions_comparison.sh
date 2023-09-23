#!/bin/bash
urle () { [[ "${1}" ]] || return 1; local LANG=C i x; for (( i = 0; i < ${#1}; i++ )); do x="${1:i:1}"; [[ "${x}" == [a-zA-Z0-9.~-] ]] && echo -n "${x}" || printf '%%%02X' "'${x}"; done; echo; }
expression_represantation_generators=("emoca" "spectre" "deca")

echo "Starting Program :)"

# Fetch FLAME data
echo -e "Before you continue, you must register at https://flame.is.tue.mpg.de/ and agree to the FLAME license terms."
read -p "Username (FLAME):" username
read -p "Password (FLAME):" password
username=$(urle $username)
password=$(urle $password)

# If running from google colab - install condacolab
answer_colab=""
while [[ ! "$answer_colab" =~ ^[YyNn]$ ]]; do
    read -p "Are you running from Google Colab? (y/n) " answer_colab
    if [[ ! "$answer_colab" =~ ^[YyNn]$ ]]; then
        echo "Invalid input! Please answer with y or n."
    fi
done
if [[ "$answer_colab" =~ ^[Yy]$ ]]; then
    pip install -q condacolab
    import condacolab
    condacolab.install()
fi


# Uplaod your data manualy to couples_expression_comparison_models\Data folder
answer_data=""
while [[ ! "$answer_data" =~ ^[YyNn]$ ]]; do
    read -p "Please make sure your data is saved to couples_expression_comparison_models\Data folder. Press y to continue" answer_data
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


# Use one of the following models to generate expressions represantation CSV for each participant
echo "Generating expression represantation:"
PS3="Choose a script by number: "
answer_exp_generator=""
while [[ ! "$answer_exp_generator" =~ ^[YyNn]$ ]]; do
    read -p "Do you need to install the model? (y/n) " answer_exp_generator
    if [[ ! "$answer_exp_generator" =~ ^[YyNn]$ ]]; then
        echo "Invalid input! Please answer with y or n."
    fi
done
if [[ "$answer_exp_generator" =~ ^[Yy]$ ]]; then
    while true; do
        select choice in "emoca" "spectre" "deca"; do
            case $choice in
                emoca)
                    echo "You selected EMOCA."
                    cd Expression_Represantation_Generators/EMOCA
                    bash emoca_installation.sh
                    break 2
                    ;;
                spectre)
                    echo "You selected SPECTRE."
                    cd Expression_Represantation_Generators/SPECTRE
                    bash spectre_installation.sh username password

                    break 2
                    ;;
                deca)
                    echo "You selected DECA."
                    cd Expression_Represantation_Generators/DECA
                    bash deca_installation.sh username password
                    break 2
                    ;;
                *)
                    echo "Invalid choice! Please select from the list."
                    break
                    ;;
            esac
        done
    done
fi

current_date=$(date +"%Y%m%d_%H%M")
folder_name="Results/${choice}_${current_date}"
mkdir "$folder_name"
echo "Folder '$folder_name' created."

echo "Generating expressions represantations CSVS"
eval "$(conda shell.bash hook)"
conda activate $choice
python expressions_represantation_generator.py


# Run Coparisons Matrics
echo "Calculating Matrics:"


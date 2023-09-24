#!/bin/bash

# Get project setup from configuration file
source config.cfg

# update running configuration if needed
printf "\n======== Setting up your running configuration! ========\n\n"
echo "---------    Current Running Configuration:    ---------"
echo ""

# update Configured Expression Representation Generator
echo "Configured Expression Representation Generator:   $EXP_REP_GENERATOR"
echo ""
PS3="Choose a model by number: "
answer_exp_generator=""
while [[ ! "$answer_exp_generator" =~ ^[YyNn]$ ]]; do
    read -p "Would you like to update the expression representation generator configuration to a different model? (y/n) " answer_exp_generator
    if [[ ! "$answer_exp_generator" =~ ^[YyNn]$ ]]; then
        echo "Invalid input! Please answer with y or n."
    fi
done
if [[ "$answer_exp_generator" =~ ^[Yy]$ ]]; then
    while true; do
        select choice in "EMOCA" "SPECTRE" "DECA"; do
            sed -i "/EXP_REP_GENERATOR=/c\EXP_REP_GENERATOR=\"$choice\"" config.cfg
            break 2
        done
    done
fi
echo ""

# update configured comparison metrics
echo "Configured comparison metrics:"
echo "    Euclidean Average: ${EUCLIDEAN_AVERAGE}"
echo "    Cluster Couple Ratio: ${CLUSTER_COUPLE_RATIO}"
echo ""

answer_comparison_metrics=""
while [[ ! "$answer_comparison_metrics" =~ ^[YyNn]$ ]]; do
    read -p "Do you want to update the comparison metrics configuration? (y/n) " answer_comparison_metrics
    if [[ ! "$answer_comparison_metrics" =~ ^[YyNn]$ ]]; then
        echo "Invalid input! Please answer with y or n."
    fi
done
if [[ "$answer_comparison_metrics" =~ ^[Yy]$ ]]; then
    answer_euclidean=""
    while [[ ! "$answer_euclidean" =~ ^[YyNn]$ ]]; do
        read -p "Do you want to run Euclidean Average metric? (y/n) " answer_euclidean
        if [[ ! "$answer_euclidean" =~ ^[YyNn]$ ]]; then
            echo "Invalid input! Please answer with y or n."
        else
            if [[ "$answer_euclidean" =~ ^[Yy]$ ]]; then
                sed -i "/EUCLIDEAN_AVERAGE=/c\EUCLIDEAN_AVERAGE=\"$TRUE\"" config.cfg
            else
                sed -i "/EUCLIDEAN_AVERAGE=/c\EUCLIDEAN_AVERAGE=\"$FALSE\"" config.cfg
            fi
        fi
    done
    answer_cluster=""
    while [[ ! "$answer_cluster" =~ ^[YyNn]$ ]]; do
        read -p "Do you want to run Cluster Couple Ratio metric? (y/n) " answer_cluster
        if [[ ! "$answer_cluster" =~ ^[YyNn]$ ]]; then
            echo "Invalid input! Please answer with y or n."
        else
            if [[ "$answer_cluster" =~ ^[Yy]$ ]]; then
                sed -i "/CLUSTER_COUPLE_RATIO=/c\CLUSTER_COUPLE_RATIO=\"$TRUE\"" config.cfg
            else
                sed -i "/CLUSTER_COUPLE_RATIO=/c\CLUSTER_COUPLE_RATIO=\"$FALSE\"" config.cfg
            fi
        fi
    done
fi

echo ""
echo "Configuration updated!"

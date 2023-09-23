#!/bin/bash

echo "Creating conda environment"
conda create --name deca python=3.7
eval "$(conda shell.bash hook)" # make sure conda works in the shell script
conda activate deca
if echo $CONDA_PREFIX | grep deca
then
    echo "Conda environment successfully activated"
else
    echo "Conda environment not activated. Probably it was not created successfully for some reason. Please activate the conda environment before running this script"
    exit
fi

echo "Installing conda packages"
pip install -r deca_model/requirements.txt

echo "echo "Download Assets""
bash deca_model/fetch_data.sh

echo "Installation finished"

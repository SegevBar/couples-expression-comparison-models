#!/bin/bash

echo "Creating conda environment"
conda create --name spectre python=3.8
eval "$(conda shell.bash hook)" # make sure conda works in the shell script
conda activate spectre
if echo $CONDA_PREFIX | grep spectre
then
    echo "Conda environment successfully activated"
else
    echo "Conda environment not activated. Probably it was not created successfully for some reason. Please activate the conda environment before running this script"
    exit
fi
echo "Installing conda packages"
conda install pytorch==1.11.0 torchvision==0.12.0 torchaudio==0.11.0 cudatoolkit=11.3 -c pytorch
conda install -c conda-forge -c fvcore fvcore iopath
pip install -r spectre_model/requirements.txt
conda install -c conda-forge yacs
pip install numpy==1.23.1

echo "Installing external packages"
cd spectre_model/external/face_alignment
pip install -e .
cd ../face_detection
git lfs pull
pip install -e .

pip install gdown
pip install git+https://github.com/facebookresearch/pytorch3d.git@v0.6.2
### This takes about 20 minutes

echo "Installation finished"

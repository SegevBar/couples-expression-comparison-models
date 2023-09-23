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

cd spectre_model/external/face_alignment
pip install -e .
cd ../face_detection
git lfs pull
pip install -e .
cd ../..

echo "Download Assets"
pip install gdown
echo -e "\nDownloading FLAME..."
mkdir -p data/FLAME2020/
wget --post-data "username=$1&password=$2" 'https://download.is.tue.mpg.de/download.php?domain=flame&sfile=FLAME2020.zip&resume=1' -O './FLAME2020.zip' --no-check-certificate --continue
unzip FLAME2020.zip -d data/FLAME2020/
rm -rf FLAME2020.zip

echo -e "\nDownload pretrained SPECTRE model..."
gdown --id 1vmWX6QmXGPnXTXWFgj67oHzOoOmxBh6B
mkdir -p pretrained/
mv spectre_model.tar pretrained/

conda install -c conda-forge yacs
pip install numpy==1.23.1
pip install git+https://github.com/facebookresearch/pytorch3d.git@v0.6.2

echo "Installation finished"

#!/bin/bash

echo "If you wish to use EMOCA, please register at:"
echo -e '\e]8;;https://emoca.is.tue.mpg.de\ahttps://emoca.is.tue.mpg.de\e]8;;\a'
while true; do
    read -p "I have registered and agreed to the license terms at https://emoca.is.tue.mpg.de? (y/n)" yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

echo "Installing mamba"
conda install mamba -n base -c conda-forge
if ! command -v mamba &> /dev/null
then
    echo "mamba could not be found. Please install mamba before running this script"
    exit
fi
echo "Creating conda environment"
mamba create -n emoca python=3.8
eval "$(conda shell.bash hook)" # make sure conda works in the shell script
conda activate emoca
if echo $CONDA_PREFIX | grep emoca
then
    echo "Conda environment successfully activated"
else
    echo "Conda environment not activated. Probably it was not created successfully for some reason. Please activate the conda environment before running this script"
    exit
fi
echo "Installing conda packages"
mamba env update -n emoca --file emoca_model/conda-environment_init.yml

echo "Installing other requirements"
pip install -r emoca_model/requirements.txt
pip install Cython==0.29
pip install git+https://github.com/facebookresearch/pytorch3d.git@v0.6.2

echo "Installing GDL"
pip install -e .

echo "Download Assets"
bash emoca_model/gdl_apps/EMOCA/demos/download_assets.sh

echo "Installation finished"

#!/bin/bash
echo "Pulling submodules"
bash emoca_model/pull_submodules.sh
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

#pip install pandas==1.4.2
#pip install numba==0.56.4
#pip install numpy==1.20.3
#pip install scikit-video==1.1.11
#pip install ipykernel
#pip install ffmpeg-python

echo "Making sure Pytorch3D installed correctly"
pip install git+https://github.com/facebookresearch/pytorch3d.git@v0.6.2
echo "Installing GDL"
pip install -e .
echo "Installation finished"

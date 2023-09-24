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
pip install git+https://github.com/facebookresearch/pytorch3d.git@v0.6.2

echo "Download Assets"
echo -e "\nDownloading FLAME..."
wget --post-data "username=$1&password=$2" 'https://download.is.tue.mpg.de/download.php?domain=flame&sfile=FLAME2020.zip&resume=1' -O './deca_model/data/FLAME2020.zip' --no-check-certificate --continue
unzip ./deca_model/data/FLAME2020.zip -d ./deca_model/data/FLAME2020
mv ./deca_model/data/FLAME2020/generic_model.pkl ./deca_model/data
echo -e "\nDownloading deca_model..."
FILEID=1rp8kdyLPvErw2dTmqtjISRVvQLj6Yzje
FILENAME=./deca_model/data/deca_model.tar
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id='${FILEID} -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=${FILEID}" -O $FILENAME && rm -rf /tmp/cookies.txt

echo "Installation finished"

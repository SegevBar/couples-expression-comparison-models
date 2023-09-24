# Couples Expression Comparison Model


## Installation

0) Install [conda](https://www.anaconda.com/download)
1) Clone this repo:
```bash
git clone --recurse-submodules -j4 https://github.com/SegevBar/couples_expression_comparison_models.git
cd couples_expression_comparison_models/
```
2) Set your running environment configuration:
   * You will be asked what expression representation generator you would like to use out of the options: EMOCA, SPECTRE, DECA.
   * You will be asked what expressions comparison metrics you would like to use out of the options: Euclidean Average, Cluster Couple Ratio. You can choose more then one.
   * The settings are saved to **config.cfg** file.
   * You don't have to edit the configuration if the current settings satisfy your needs.
```bash
bash setup.sh
```
3) Install Packages and Assets:
   * This step might take some time
   * You will be asked to enter your FLAME registration username and password - make sure you are registered [here](https://flame.is.tue.mpg.de/index.html).
   * Only the packages and assetes relevant to your current configuration will be installed, if you changed the configuration from the last time running on your local machine, you have to perform this step again.
```bash
bash install.sh
```

## Usage 
1) Save your data in **couples_expression_comparison_models\Data** directory according to the following format:
   * Each participant should have a unique folder containing all their videos.
   * A csv file named **"coupling.csv"** filled with the coupled participants by the name of their folder, an example is provided. 
2) Run the program script: 
```bash
bash run_couples_expression_comparison_model.sh
```
The program:
* Creates a csv file for each participant containing the expressions' representation for each video frame.
* Calculates the comparison metrics by the couples provided in the coupling.csv and presents the results.

### Running from Google Colab
We provided you a jupiter notebook prepared for running in Google Colab named **exp_compare_demo.ipynb**.\
Just follow the steps and run the code cell by cell.\
**Make sure to downlaod the resuls files! They won't be saved in the colab environment.**


## Project Structure 
This repo has two subpackages - `expression represantation generator` and `couples expression comparison matrics` 

### expression represantation generator


### couples expression comparison matrics




## Citation 

This repo is has been heavily based on the original implementations of several models. We would like to acknowledge the following repositories which we have benefited greatly from:

[EMOCA](https://github.com/radekd91/emoca):
```
@inproceedings{EMOCA:CVPR:2021,
  title = {{EMOCA}: {E}motion Driven Monocular Face Capture and Animation},
  author = {Danecek, Radek and Black, Michael J. and Bolkart, Timo},
  booktitle = {Conference on Computer Vision and Pattern Recognition (CVPR)},
  pages = {20311--20322},
  year = {2022}
}
```
[DECA](https://github.com/YadiraF/DECA):
```
@article{DECA:Siggraph2021,
  title={Learning an Animatable Detailed {3D} Face Model from In-The-Wild Images},
  author={Feng, Yao and Feng, Haiwen and Black, Michael J. and Bolkart, Timo},
  journal = {ACM Transactions on Graphics (ToG), Proc. SIGGRAPH},
  volume = {40}, 
  number = {8}, 
  year = {2021}, 
  url = {https://doi.org/10.1145/3450626.3459936} 
}
```
[SPECTRE](https://filby89.github.io/spectre/): 
```
@article{filntisis2022visual,
  title = {Visual Speech-Aware Perceptual 3D Facial Expression Reconstruction from Videos},
  author = {Filntisis, Panagiotis P. and Retsinas, George and Paraperas-Papantoniou, Foivos and Katsamanis, Athanasios and Roussos, Anastasios and Maragos, Petros},
  journal = {arXiv preprint arXiv:2207.11094},
  publisher = {arXiv},
  year = {2022},
}
```

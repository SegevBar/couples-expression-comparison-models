# Couples Expression Comparison Model


## Installation 

### Dependencies

0) Install [conda](https://docs.conda.io/en/latest/miniconda.html)
1) Clone this repo 
2) Run the installation script:
```bash
bash installation.sh
```
3) Download the core assets with the following script:
```bash
bash download_assets.sh
```

## Usage 

1) run the relevant expression represantation generator: 
```bash
pyton expressions_represantation_generator.py
```
1) run the couples expression comparison matrics:
```bash
pyton couples_expression_comparison_matrics.py
```



## Structure 
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

'''
@inproceedings{DECA:Siggraph2021,
  title={Learning an Animatable Detailed {3D} Face Model from In-The-Wild Images},
  author={Feng, Yao and Feng, Haiwen and Black, Michael J. and Bolkart, Timo},
  journal = {ACM Transactions on Graphics, (Proc. SIGGRAPH)},
  volume = {40},
  number = {8},
  year = {2021},
  url = {https://doi.org/10.1145/3450626.3459936}
}
'''

import os, sys
import numpy as np
from tqdm import tqdm
import torch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DECA.deca_model.decalib.deca import DECA
from . import rev_datasets
from DECA.deca_model.decalib.utils.config import cfg as deca_cfg

PATH = "DECA"


class DecaExpGenerator:
    def __init__(self, input_path, device="cuda"):
        self.input_path = input_path
        self.device = device
        self.preprocessed_video_path = os.path.join(PATH, "preprocessed_video")
        self.video_name = os.path.splitext(os.path.basename(input_path))[0]
        self.iscrop = True
        self.detector = "fan"
        self.sample_step = 10
        self.rasterizer_type = "pytorch3d"  # or "standard"

    def generate_expressions_representation(self):
        print("deca start")
        device = self.device

        # load test images
        testdata = rev_datasets.TestData(self.input_path, self.preprocessed_video_path, iscrop=self.iscrop, face_detector=self.detector,
                                     sample_step=self.sample_step)

        # run DECA
        deca_cfg.model.use_tex = False
        deca_cfg.rasterizer_type = self.rasterizer_type
        deca_cfg.model.extract_tex = True
        deca = DECA(config=deca_cfg, device=device)

        exp_array = np.array([])
        frame_counter = 0

        for i in tqdm(range(len(testdata))):
            frame_counter += 1

            name = testdata[i]['imagename']
            images = testdata[i]['image'].to(device)[None, ...]

            with torch.no_grad():
                codedict = deca.encode(images)

                exp_vector = codedict['exp'].cpu().numpy()
                exp_array = np.append(exp_array, exp_vector)

        exp_array = exp_array.reshape(frame_counter, 50)
        return exp_array

"""
@inproceedings{EMOCA:CVPR:2021,
  title = {{EMOCA}: {E}motion Driven Monocular Face Capture and Animation},
  author = {Danecek, Radek and Black, Michael J. and Bolkart, Timo},
  booktitle = {Conference on Computer Vision and Pattern Recognition (CVPR)},
  pages = {20311--20322},
  year = {2022}
}
"""

from gdl_apps.EMOCA.utils.load import load_model
from gdl.datasets.FaceVideoDataModule import TestFaceVideoDM
import gdl
from pathlib import Path
from tqdm import auto
import argparse
from gdl_apps.EMOCA.utils.io import save_obj, save_images, save_codes, test
import numpy as np
import os

from Expression_Representation_Generators.abs_generator import AbstractGenerator

PATH = "EMOCA"


class EmocaExpGenerator(AbstractGenerator):
    def __init__(self, input_path, device="cuda"):
        self.input_path = input_path
        self.device = device
        self.model_name = "EMOCA_v2_lr_mse_20"
        self.path_to_models = str(Path(gdl.__file__).parents[1] / "assets/EMOCA/models")
        self.mode = "detail"
        self.processed_subfolder = None
        self.preprocessed_video_path = os.path.join(PATH, "preprocessed_video")
        self.video_name = os.path.splitext(os.path.basename(input_path))[0]

    def str2bool(self, v):
        if isinstance(v, bool):
            return v
        if v.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif v.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError('Boolean value expected.')

    def create_preprocessed_video_dir(self):
        if os.path.exists(self.preprocessed_video_path):
            os.rmdir(self.preprocessed_video_path)
        os.makedirs(self.preprocessed_video_path)

    def generate_expressions_representation(self):
        self.create_preprocessed_video_dir()
        
        # 1) Process the video - extract the frames from video and detected faces
        dm = TestFaceVideoDM(self.input_video, self.preprocessed_video_path, processed_subfolder=self.processed_subfolder,
            batch_size=4, num_workers=4)
        dm.prepare_data()
        dm.setup()
        processed_subfolder = Path(dm.output_dir).name

        # 2) Load the model
        emoca, conf = load_model(self.path_to_models, self.model_name, self.mode)
        emoca.cuda()
        emoca.eval()

        # 3) Get the data loadeer with the detected faces
        dl = dm.test_dataloader()

        exp_array = np.array([])
        frame_counter = 0
        # 4) Run the model on the data
        for j, batch in enumerate(auto.tqdm(dl)):
            frame_counter += 1

            current_bs = batch["image"].shape[0]
            img = batch
            vals, visdict = test(emoca, img)

            exp_vector = vals['expcode'].cpu().numpy()
            exp_array = np.append(exp_array, exp_vector)

            for i in range(current_bs):
                name = batch["image_name"][i]
                sample_output_folder = Path(self.preprocessed_video_path) / name
                sample_output_folder.mkdir(parents=True, exist_ok=True)

        exp_array = exp_array.reshape(frame_counter, 50)
        return exp_array

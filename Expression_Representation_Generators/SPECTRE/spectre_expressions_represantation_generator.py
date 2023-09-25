'''
@misc{filntisis2022visual,
  title = {Visual Speech-Aware Perceptual 3D Facial Expression Reconstruction from Videos},
  author = {Filntisis, Panagiotis P. and Retsinas, George and Paraperas-Papantoniou, Foivos and Katsamanis, Athanasios and Roussos, Anastasios and Maragos, Petros},
  publisher = {arXiv},
  year = {2022},
}
'''

import os
import torch
import numpy as np
import cv2
from skimage.transform import estimate_transform, warp

import collections
from tqdm import tqdm

from Expression_Representation_Generators.abs_generator import AbstractGenerator
from spectre_model.datasets.data_utils import landmarks_interpolate
from spectre_model.src.spectre import SPECTRE
from spectre_model.config import cfg as spectre_cfg

PATH = "SPECTRE"


class SpectreExpGenerator(AbstractGenerator):
    def __init__(self, input_path, device="cuda"):
        self.input_path = input_path
        self.device = device
        self.preprocessed_video_path = os.path.join(PATH, "preprocessed_video")
        self.video_name = os.path.splitext(os.path.basename(input_path))[0]

    def extract_frames(self, detect_landmarks=True):
        vidcap = cv2.VideoCapture(self.input_path)

        if detect_landmarks is True:
            from spectre_model.external.Visual_Speech_Recognition_for_Multiple_Languages.tracker.face_tracker import FaceTracker
            from spectre_model.external.Visual_Speech_Recognition_for_Multiple_Languages.tracker.utils import get_landmarks
            face_tracker = FaceTracker()

        imagepath_list = []
        count = 0

        face_info = collections.defaultdict(list)

        fps = vidcap.get(cv2.CAP_PROP_FPS)

        with tqdm(total=int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))) as pbar:
            while True:
                success, image = vidcap.read()
                if not success:
                    break

                if detect_landmarks is True:
                    detected_faces = face_tracker.face_detector(image, rgb=False)
                    # -- face alignment
                    landmarks, scores = face_tracker.landmark_detector(image, detected_faces, rgb=False)
                    face_info['bbox'].append(detected_faces)
                    face_info['landmarks'].append(landmarks)
                    face_info['landmarks_scores'].append(scores)

                imagepath = os.path.join(self.preprocessed_video_path, f"{self.video_name}_{count:06d}.jpg")
                cv2.imwrite(imagepath, image)  # save frame as JPEG file
                count += 1
                imagepath_list.append(imagepath)
                pbar.update(1)
                pbar.set_description("Preprocessing frame %d" % count)

        landmarks = get_landmarks(face_info)
        print('video frames are stored in {}'.format(self.preprocessed_video_path))
        return imagepath_list, landmarks, fps

    def crop_face(self, frame, landmarks, scale=1.0):
        image_size = 224
        left = np.min(landmarks[:, 0])
        right = np.max(landmarks[:, 0])
        top = np.min(landmarks[:, 1])
        bottom = np.max(landmarks[:, 1])

        h, w, _ = frame.shape
        old_size = (right - left + bottom - top) / 2
        center = np.array([right - (right - left) / 2.0, bottom - (bottom - top) / 2.0])

        size = int(old_size * scale)

        src_pts = np.array([[center[0] - size / 2, center[1] - size / 2], [center[0] - size / 2, center[1] + size / 2],
                            [center[0] + size / 2, center[1] - size / 2]])
        DST_PTS = np.array([[0, 0], [0, image_size - 1], [image_size - 1, 0]])
        tform = estimate_transform('similarity', src_pts, DST_PTS)

        return tform

    def create_preprocessed_video_dir(self):
        if os.path.exists(self.preprocessed_video_path):
            os.rmdir(self.preprocessed_video_path)
        os.makedirs(self.preprocessed_video_path)

    def generate_expressions_representation(self):
        crop_face = True
        spectre_cfg.pretrained_modelpath = "spectre_model/pretrained/spectre_model.tar"
        spectre_cfg.model.use_tex = False

        self.create_preprocessed_video_dir()

        spectre = SPECTRE(spectre_cfg, self.device)
        spectre.eval()

        image_paths, landmarks, fps = self.extract_frames(detect_landmarks=crop_face)
        if crop_face:
            landmarks = landmarks_interpolate(landmarks)
            if landmarks is None:
                print('No faces detected in input {}'.format(self.input_path))
        original_video_length = len(image_paths)
        # pad
        image_paths.insert(0,image_paths[0])
        image_paths.insert(0,image_paths[0])
        image_paths.append(image_paths[-1])
        image_paths.append(image_paths[-1])

        landmarks.insert(0,landmarks[0])
        landmarks.insert(0,landmarks[0])
        landmarks.append(landmarks[-1])
        landmarks.append(landmarks[-1])

        landmarks = np.array(landmarks)
        L = 50 # chunk size

        # create lists of overlapping indices
        indices = list(range(len(image_paths)))
        overlapping_indices = [indices[i: i + L] for i in range(0, len(indices), L-4)]

        if len(overlapping_indices[-1]) < 5:
            # if the last chunk has less than 5 frames, pad it with the semilast frame
            overlapping_indices[-2] = overlapping_indices[-2] + overlapping_indices[-1]
            overlapping_indices[-2] = np.unique(overlapping_indices[-2]).tolist()
            overlapping_indices = overlapping_indices[:-1]

        overlapping_indices = np.array(overlapping_indices)

        image_paths = np.array(image_paths) # do this to index with multiple indices

        with torch.no_grad():
            exp_array = np.array([])
            frame_counter = 0

            for chunk_id in range(len(overlapping_indices)):
                print('Processing frames {} to {}'.format(overlapping_indices[chunk_id][0], overlapping_indices[chunk_id][-1]))
                image_paths_chunk = image_paths[overlapping_indices[chunk_id]]

                landmarks_chunk = landmarks[overlapping_indices[chunk_id]] if crop_face else None

                images_list = []

                """ load each image and crop it around the face if necessary """
                for j in range(len(image_paths_chunk)):
                    frame_counter += 1
                    frame = cv2.imread(image_paths_chunk[j])
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    kpt = landmarks_chunk[j]

                    tform = crop_face(frame, kpt, scale=1.6)
                    cropped_image = warp(frame, tform.inverse, output_shape=(224, 224))

                    images_list.append(cropped_image.transpose(2, 0, 1))

                frame_counter = frame_counter - 4  # fix padding
                images_array = torch.from_numpy(np.array(images_list)).type(dtype=torch.float32).to(
                    self.device)  # K,224,224,3

                codedict, initial_deca_exp, initial_deca_jaw = spectre.encode(images_array)
                codedict['exp'] = codedict['exp'] + initial_deca_exp
                exp_vector = codedict['exp']

                exp_vector_np = exp_vector.cpu().numpy()
                exp_vector_np_cropped = exp_vector_np[2:-2, :]
                exp_array = np.append(exp_array, exp_vector_np_cropped)

            exp_array = exp_array.reshape(frame_counter, 50)
            return exp_array

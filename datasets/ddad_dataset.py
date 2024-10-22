import os
import skimage.transform
import numpy as np
import PIL.Image as pil
import pickle, json, cv2
import torch, torchvision

from .base_dataset import BaseDataset

class ddadDataset(BaseDataset):
    """Superclass for different types of Waymo dataset loaders
    """
    def __init__(self, *args, **kwargs):
        super(ddadDataset, self).__init__(*args, **kwargs)

        self.K = dict()
        self.get_all_intrinsic()
        self.full_res_shape = (640, 384)
       # self.median_ts = 100.0              # process_datasets/process_nuscenes_timestep.py

    def get_all_intrinsic(self):
        for file in self.filenames:
            folder = file.split()[0]
            if folder not in self.K:
                self.K[folder] = np.eye(4, dtype=np.float32)

                cam_path = os.path.join(self.data_path, 'training',folder, 'cam.txt')
                self.K[folder][:3, :3] = np.genfromtxt(cam_path).astype(np.float32).reshape((3,3))
                self.K[folder][0, :]/=640
                self.K[folder][1, :]/=384

    def get_intrinsic(self, folder):
        return self.K[folder]
    
    def get_gt_dim(self, folder, frame_index, side):
        return self.full_res_shape[1], self.full_res_shape[0]
    
    def get_img_path(self, folder, frame_index):
        f_str = "{:06d}{}".format(frame_index, self.img_ext)
        return os.path.join(self.data_path, 'training',folder, f_str)

    def get_color(self, folder, frame_index, side, do_flip):

        color = self.loader(self.get_img_path(folder, frame_index))
        
        if do_flip:
            color = color.transpose(pil.FLIP_LEFT_RIGHT)
        return color
    
    def get_depth(self, folder, frame_index, side, do_flip):
        f_str = "{:06d}{}".format(frame_index, '.npy')
        depth_path = os.path.join(self.data_path,'training', folder, 'depth', f_str)

        depth = np.load(depth_path)

        if do_flip:
            depth[:,0] = self.full_res_shape[0] - depth[:,0]
        
        depth = np.concatenate((depth[:,1:2], depth[:,0:1], depth[:,2:3]), axis=1)    # (N, 3) -> [h_i, w_i, z_i]

        return depth

    def get_mask(self, folder, frame_index, side =None):
        f_str = "{:06d}{}".format(frame_index, '_mask.npy')
        return os.path.join(self.data_path, 'training',folder, f_str)

    def get_sky(self, folder, frame_index, side =None):
        f_str = "{:06d}{}".format(frame_index, '_sky.npy')
        return os.path.join(self.data_path, 'training',folder , f_str)

    

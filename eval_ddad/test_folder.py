import torch.utils.data as data
import numpy as np
#from imageio.v2 import imread
from path import Path
import torch
from scipy import sparse
from PIL import Image 
def pil_loader(path):
    # open path as file to avoid ResourceWarning
    # (https://github.com/python-pillow/Pillow/issues/835)
    with open(path, 'rb') as f:
        with Image.open(f) as img:
            return img.convert('RGB')

def load_sparse_depth(filename):
    sparse_depth = sparse.load_npz(filename)
    depth = sparse_depth.todense()
    return np.array(depth)


def crawl_folder(folder, dataset='nyu'):

    imgs = sorted((folder/'color/').files('*.png') +
                  (folder/'color/').files('*.jpg'))

    if dataset == 'nyu':
        depths = sorted((folder/'depth/').files('*.png'))
    elif dataset == 'kitti':
        depths = sorted((folder/'depth/').files('*.npy'))
    elif dataset == 'ddad':
        depths = sorted((folder/'depth/').files('*.npz'))

    return imgs, depths


class TestSet(data.Dataset):
    """A sequence data loader where the files are arranged in this way:
        root/color/0000000.png
        root/depth/0000000.npz or png
    """

    def __init__(self, root, transform=None, dataset='nyu',h=384,w =640):
        self.root = Path(root)/'testing'
        self.resize = transform.Resize((h,w),interpolation=transform.InterpolationMode.BICUBIC)
        self.dataset = dataset
        self.imgs, self.depths = crawl_folder(self.root, self.dataset)
        self.to_tensor = transform.ToTensor()
    def __getitem__(self, index):
        #print(self.imgs[index])
        img = pil_loader(self.imgs[index])
        
        if self.dataset == 'nyu':
            depth = torch.from_numpy(
                imread(self.depths[index]).astype(np.float32)).float()/5000
        elif self.dataset == 'kitti':
            depth = torch.from_numpy(
                np.load(self.depths[index]).astype(np.float32))
        elif self.dataset == 'ddad':
            depth = torch.from_numpy(load_sparse_depth(
                self.depths[index]).astype(np.float32))

    #if self.transform is not None:
        img = self.resize(img)
        img = self.to_tensor(img)
            #img = img

        return img, depth

    def __len__(self):
        return len(self.imgs)

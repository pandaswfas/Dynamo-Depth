import numpy as np
import torch
from torch.utils.data import DataLoader
from tqdm import tqdm

from .test_folder import TestSet
from .losses.loss_functions import compute_errors

from networks.depth_decoder import DepthDecoder,LiteDepthDecoder
from networks.resnet_encoder import ResnetEncoder
from networks.depth_encoder import LiteMono
from torchvision import transforms
import os
import matplotlib.pyplot as plt
@torch.no_grad()
def main():
    # hparams = get_opts()

    # # initialize network
    # system = SC_Depth(hparams)

    # # # load ckpts
    # system = system.load_from_checkpoint('/media/usst/sdb8/wl/epoch=99-val_loss=0.1438.ckpt', strict=False)

    # model = system.depth_net
    # model.cuda()
    # model.eval()
    #init_model
    mode_path = '/mnt/sda/wl/Dynamo-Depth-main_ddad/log/ddad/models/motion_init_01_best'
    encoder = ResnetEncoder(18, 0)
    path = os.path.join(mode_path,'depth_enc.pth') 
    encoder_ = torch.load(path)
    encoder_dict = encoder.state_dict()
    encoder.load_state_dict({k:v for k,v in encoder_.items() if k in encoder_dict})
    decoder = DepthDecoder(encoder.num_ch_enc, [0,1,2,3])
    path = os.path.join(mode_path,'depth_dec.pth') 
    decoder_ = torch.load(path)
    decoder_dict = decoder.state_dict()
    decoder.load_state_dict({k:v for k,v in decoder_.items() if k in decoder_dict})
    encoder.cuda()
    decoder.cuda()
    encoder.eval()
    decoder.eval()
    # mode_path = '/mnt/sda/wl/Dynamo-Depth-main_ddad/log/ddad/models/pose_init_00'
    # encoder = LiteMono(model='lite-mono-8m', drop_path_rate=0, pretrained=0)
    # path = os.path.join(mode_path,'depth_enc.pth') 
    # encoder_ = torch.load(path)
    # encoder_dict = encoder.state_dict()
    # encoder.load_state_dict({k:v for k,v in encoder_.items() if k in encoder_dict})
    # decoder = LiteDepthDecoder(encoder.num_ch_enc, [0,1,2])
    # path = os.path.join(mode_path,'depth_dec.pth') 
    # decoder_ = torch.load(path)
    # decoder_dict = decoder.state_dict()
    # decoder.load_state_dict({k:v for k,v in decoder_.items() if k in decoder_dict})

    # encoder.cuda().eval()
    # decoder.cuda().eval()


    print('\n===load weight from:{}===\n'.format(mode_path))
    # # get training resolution
    training_size = [384, 640]

    # data loader
    # test_transform = custom_transforms.Compose([
    #     custom_transforms.RescaleTo(training_size),
    #     custom_transforms.ArrayToTensor(),
    #     transforms.ToTensor()]
    # )
    test_dataset = TestSet(
        '/mnt/sda/wl/DDAD/ddad/',
        transforms,
        dataset= 'ddad'
    )
    print('{} samples found in test scenes'.format(len(test_dataset)))

    test_loader = DataLoader(test_dataset,
                             batch_size=2,
                             shuffle=False,
                             num_workers=4,
                             pin_memory=True
                             )
    
    all_errs = []
    def disp_to_depth(disp, min_depth, max_depth):
        min_disp = 1 / max_depth
        max_disp = 1 / min_depth
        scaled_disp = min_disp + (max_disp - min_disp) * disp
        depth = 1 / scaled_disp
        return scaled_disp, depth

    with torch.no_grad():
        for i, (tgt_img, gt_depth) in enumerate(tqdm(test_loader)):
            #print(tgt_img)
            # plt.imshow(tgt_img[0].permute(1,2,0).detach().cpu())
            # plt.show()
            pred_depth = decoder(encoder(tgt_img.cuda()))[('disp',0)]
            #pred_depth = model(tgt_img.cuda())
            _,pred_depth = disp_to_depth(pred_depth,0.1,100)
            # plt.subplot(121)
            # plt.imshow(pred_depth[0][0].detach().cpu())
            # plt.subplot(122)
            # plt.imshow(tgt_img[0].permute(1,2,0).detach().cpu())
            # plt.show()
            errs = compute_errors(gt_depth.cuda(), pred_depth,
                                'ddad')

            all_errs.append(np.array(errs))

    all_errs = np.stack(all_errs)
    mean_errs = np.mean(all_errs, axis=0)

    print("\n  " + ("{:>8} | " * 9).format("abs_diff", "abs_rel",
          "sq_rel", "log10", "rmse", "rmse_log", "a1", "a2", "a3"))
    print(("&{: 8.4f}  " * 9).format(*mean_errs.tolist()) + "\\\\")


if __name__ == '__main__':
    main()

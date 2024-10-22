# Self-supervised monocular depth estimation in nighttime and dynamic scenes

![绘图1 - 副本](https://github.com/user-attachments/assets/ec4c5225-d1d0-4829-994b-95b0cfa71fec)

## Datasets
### 💾 KITTI Dataset

🔹 Please refer to the [raw KITTI dataset](http://www.cvlibs.net/datasets/kitti/raw_data.php) for downloading the kitti Dataset.
### 💾 nuScenes Dataset

🔹 Please refer to the [nuScenes official website](https://www.nuscenes.org) for downloading the nuScenes Dataset.

### 💾 DDAD Dataset

🔹 Please refer to the [ddad](https://github.com/TRI-ML/DDAD?tab=readme-ov-file) for downloading the DDAD Dataset.

## Evaluation
Scripts for evaluation are found in `eval/`, including [depth](eval/depth.py), 

The following are a set of shared arguments to use with any of the evaluation scripts above.
- `-l </PATH/TO/MODEL/CKPT>` indicates which model checkpoint to be evaluated.
- `--depth_model <MODEL_NAME>` specifies which depth model (`"litemono"` or `"monodepthv2"`) to use, with default `"litemono"`.
- `-d <DATASET_NAME>` specifies which dataset (`"DDAD"`, `"nuscenes"`, or `"kitti"`) to evaluate on, and the default is `"DDAD"`.
- `--eval_dir` defines the output directory where the results would be saved, with default `"./outputs"`.

**Note**: To access the trained models for Waymo Open, please fill out the [Google Form](https://forms.gle/nRezg2gr7QDXJGcA9), and [raise an issue](https://github.com/YihongSun/Dynamo-Depth/issues/new) if we don't get back to you in two days. Please note that Waymo open dataset is under strict non-commercial license so we are not allowed to share the model with you if it will used for any profit-oriented activities.

### 📊 Depth
[eval/depth.py](eval/depth.py) evaluates monocular depth estimation, with results saved in `./outputs/<CKPT>_<DATASET>/depth/`.

🔹 To replicate the results reported in the paper (Table 1 and 2), run the following lines. 
```
## === Missing checkpoints will be downloaded automatically === ##

python3 eval/depth.py -l ckpt/W_Dynamo-Depth                                  ## please fill out the form for ckpt!!
python3 eval/depth.py -l ckpt/W_Dynamo-Depth_MD2 --depth_model monodepthv2    ## please fill out the form for ckpt!!
python3 eval/depth.py -l ckpt/N_Dynamo-Depth -d nuscenes
python3 eval/depth.py -l ckpt/N_Dynamo-Depth_MD2 --depth_model monodepthv2 -d nuscenes
python3 eval/depth.py -l ckpt/K_Dynamo-Depth -d kitti
python3 eval/depth.py -l ckpt/K_Dynamo-Depth_MD2 --depth_model monodepthv2 -d kitti
```

|     Model     |   Dataset |  Abs Rel  |   Sq Rel  |    RMSE   |  RMSE log | delta < 1.25 | delta < 1.25<sup>2</sup> | delta < 1.25<sup>3</sup> |
|:-------------------------:|:------:|:---------:|:---------:|:---------:|:---------:|:------------:|:--------------:|:--------------:|
|  [KITTI_MD2]( https://pan.baidu.com/s/1NccK2jafE_US2GF8NyTPqQ?pwd=vx4u)  |  KITTI  | 0.117  |  0.842  |  4.848  |  0.193  |  0.869  |  0.958  |  0.982   |
|  [KITTI_LM](https://pan.baidu.com/s/1s0DImH-uKpkVTpHuTtBcng) |  KITTI   | 0.107  |  0.824  |  4.648  |  0.184  |  0.886  |  0.962  |  0.983   |
|  [nuScenes_MD2]( https://pan.baidu.com/s/1fyHEQDdR5l8zH1kfMkWq5g?pwd=38ay)  |  nuScenes  |  0.145  |  1.416  |  7.092  |  0.245  |  0.802  |  0.921  |  0.967  |
|  [nuScenes_LM]  |  nuScenes   |  0.147  |  1.423  |  6.871  |  0.243  |  0.800  |  0.922  |  0.968  |
|  [DDAD_MD2]  |  DDAD |  0.166  |  3.643  |  17.291  |  0.286  |  0.764  |  0.902  |  0.949  |
|  [DDAD_LM]  |  DDAD   |  0.152  |  3.519  |  14.684  |  0.244  |  0.805  |  0.928  |  0.968  |

(*) Very minor differences compared to the results in the paper. Rest of the checkpoints are consistent with the paper.  
(†) Please refer to the note above for obtaining access to the models trained on Waymo Open Dataset.

🔹 To replicate the results reported in the Appendix (Table 6 and 7), run the following lines.
```
## === Missing checkpoints will be downloaded automatically === ##

python3 eval/depth.py -l ckpt/N_Dynamo-Depth -d nuscenes --split nuscenes_dayclear
python3 eval/depth.py -l ckpt/N_Dynamo-Depth_MD2 --depth_model monodepthv2 -d nuscenes --split nuscenes_dayclear
```
Note that by adding `--split nuscenes_dayclear`, we evaluate on the nuScenes day-clear subset as defined in `splits/nuscenes_dayclear/test_files.txt` instead of the original `splits/nuscenes/test_files.txt`



## Notice
Our complete code will be revised after the paper is published.
The test program is complete and some weights have been uploaded.

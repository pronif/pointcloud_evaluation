# ----------------------------------------------------------------------------
# -                   TanksAndTemples Website Toolbox                        -
# -                    http://www.tanksandtemples.org                        -
# ----------------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2017
# Arno Knapitsch <arno.knapitsch@gmail.com >
# Jaesik Park <syncle@gmail.com>
# Qian-Yi Zhou <Qianyi.Zhou@gmail.com>
# Vladlen Koltun <vkoltun@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# ----------------------------------------------------------------------------
#
# This python script is for downloading dataset from www.tanksandtemples.org
# The dataset has a different license, please refer to
# https://tanksandtemples.org/license/

from setup import *
from trajectory_io import *
import copy
import numpy as np

MAX_POINT_NUMBER = 4e6


def trajectory_alignment(traj_to_register, gt_traj_col, gt_trans):
    traj_pcd_col = convert_trajectory_to_pointcloud(gt_traj_col)
    traj_pcd_col.transform(gt_trans)

    corres = Vector2iVector(np.asarray(
            list(map(lambda x: [x, x], range(len(gt_traj_col))))))

    rr=RANSACConvergenceCriteria()
    rr.max_iteration = 100000
    rr.max_validation = 100000

    # in this case a log file was used which contains
    # every movie frame (see tutorial for details)
    if len(traj_to_register) > 1600:
        traj_col2 = gen_sparse_trajectory(mapping, traj_to_register)
        traj_to_register_pcd = convert_trajectory_to_pointcloud(traj_col2)
    else:
        traj_to_register_pcd = convert_trajectory_to_pointcloud(
                traj_to_register)

    #randomvar = 0.05 # 5% error added
    randomvar = 0.0
    nr_of_cam_pos = len(traj_to_register_pcd.points)
    rand_number_added = np.asanyarray(traj_to_register_pcd.points) * \
            (np.random.rand(nr_of_cam_pos,3)*randomvar-randomvar/2.0+1)
    list_rand = list(rand_number_added)
    traj_to_register_pcd_rand = PointCloud()
    for elem in list_rand:
        traj_to_register_pcd_rand.points.append(elem)

    # Rough registration based on aligned colmap SfM data
    reg = registration_ransac_based_on_correspondence(
            traj_to_register_pcd_rand, traj_pcd_col, corres, 0.2,
            TransformationEstimationPointToPoint(True),6, rr)
    return reg.transformation


def crop_and_downsample(pcd, crop_volume,
        down_sample_method='voxel', voxel_size=0.01, trans=np.identity(4)):
    pcd_copy = copy.deepcopy(pcd)
    pcd_copy.transform(trans)
    pcd_crop = crop_volume.crop_point_cloud(pcd_copy)
    if down_sample_method == 'voxel':
        return voxel_down_sample(pcd_crop, voxel_size)
    elif down_sample_method == 'uniform':
        n_points = len(pcd_crop.points)
        if(n_points > MAX_POINT_NUMBER):
            ds_rate = int(round(n_points/float(MAX_POINT_NUMBER)))
            return uniform_down_sample(pcd_crop, ds_rate)
    return pcd_crop


def registration_unif(source, gt_target, init_trans,
        crop_volume, threshold, max_itr, max_size = 4*MAX_POINT_NUMBER,
        verbose = True):
    if verbose:
        print("[Registration] threshold: %f" % threshold)
        set_verbosity_level(VerbosityLevel.Debug)

    s = crop_and_downsample(source, crop_volume,
            down_sample_method='uniform', trans=init_trans)
    t = crop_and_downsample(gt_target, crop_volume,
            down_sample_method='uniform')
    reg = registration_icp(s, t, threshold, np.identity(4),
            TransformationEstimationPointToPoint(True),
            ICPConvergenceCriteria(1e-6, max_itr))
    reg.transformation = np.matmul(reg.transformation, init_trans)
    return reg


def registration_vol_ds(source, gt_target, init_trans,
        crop_volume, voxel_size, threshold, max_itr,
        verbose = True):
    if verbose:
        print("[Registration] voxel_size: %f, threshold: %f"
                % (voxel_size, threshold))
        set_verbosity_level(VerbosityLevel.Debug)
    s = crop_and_downsample(source, crop_volume,
            down_sample_method='voxel', trans=init_trans)
    t = crop_and_downsample(gt_target, crop_volume,
            down_sample_method='voxel')
    reg = registration_icp(s, t, threshold, np.identity(4),
            TransformationEstimationPointToPoint(True),
            ICPConvergenceCriteria(1e-6, max_itr))
    reg.transformation = np.matmul(reg.transformation, init_trans)
    return reg

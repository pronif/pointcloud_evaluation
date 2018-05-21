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
import copy
import numpy as np

MAX_POINT_NUMBER = 4e6

def downsample(pcd, down_sample_method='voxel',
               voxel_size=0.01, trans=np.identity(4)):
    pcd_copy = copy.deepcopy(pcd)
    pcd_copy.transform(trans)
    if down_sample_method == 'voxel':
        return voxel_down_sample(pcd_copy, voxel_size)
    elif down_sample_method == 'uniform':
        n_points = len(pcd_copy.points)
        if (n_points > MAX_POINT_NUMBER):
            ds_rate = int(round(n_points / float(MAX_POINT_NUMBER)))
            return uniform_down_sample(pcd_copy, ds_rate)
    return pcd_copy


def registration_unif(source, gt_target, init_trans,
                      threshold, max_itr, max_size=4 * MAX_POINT_NUMBER,
                      verbose=True):
    if verbose:
        print("[Registration] threshold: %f" % threshold)
        set_verbosity_level(VerbosityLevel.Debug)

    s = downsample(source, down_sample_method='uniform',
                   trans=init_trans)
    t = downsample(gt_target,
                   down_sample_method='uniform')
    reg = registration_icp(s, t, threshold, np.identity(4),
                           TransformationEstimationPointToPoint(True),
                           ICPConvergenceCriteria(1e-6, max_itr))
    reg.transformation = np.matmul(reg.transformation, init_trans)
    return reg


def registration_vol_ds(source, gt_target, init_trans,
                        voxel_size, threshold, max_itr, verbose=True):
    if verbose:
        print("[Registration] voxel_size: %f, threshold: %f"
              % (voxel_size, threshold))
        set_verbosity_level(VerbosityLevel.Debug)
    s = downsample(source,
                   down_sample_method='voxel', trans=init_trans)
    t = downsample(gt_target,
                   down_sample_method='voxel')
    reg = registration_icp(s, t, threshold, np.identity(4),
                           TransformationEstimationPointToPoint(True),
                           ICPConvergenceCriteria(1e-6, max_itr))
    reg.transformation = np.matmul(reg.transformation, init_trans)
    return reg

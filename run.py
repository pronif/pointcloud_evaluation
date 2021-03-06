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

# this script requires Open3D python binding
# please follow the intructions in setup.py before running this script.
import numpy as np

from setup import *
from registration import *
from evaluation import *
from util import *
from plot import *


def run_evaluation():
    scene_name = DATASET_DIR.split("/")[-2]
    print("")
    print("===========================")
    print("Evaluating %s" % scene_name)
    print("===========================")

    dTau = threshold

    # User input files
    recon_file = DATASET_DIR + RECONSTRUCTION_FILE
    gt_file = DATASET_DIR + GROUND_TRUTH_FILE
    # Output file folder
    mvs_outpath = DATASET_DIR + '/evaluation/'
    make_dir(mvs_outpath)

    # Load reconstruction and according GT
    print(recon_file)
    pcd = read_point_cloud(recon_file)
    print(gt_file)
    gt_pcd = read_point_cloud(gt_file)
    if TRANSFORMATION_FILE is None:
        gt_trans = np.eye(4)
    else:
        transformation_file = DATASET_DIR + TRANSFORMATION_FILE
        gt_trans = np.loadtxt(transformation_file)
    dist_threshold = dTau

    if(do_ICP):
        # Registration refinement in 3 iterations
        r2 = registration_vol_ds(pcd, gt_pcd,
                                 gt_trans, 3 * dTau, dTau * 120, 20)
        r3 = registration_vol_ds(pcd, gt_pcd,
                                 r2.transformation, 2 * dTau, dTau * 30, 20)
        r = registration_unif(pcd, gt_pcd,
                              r3.transformation, dTau * 15, 20)
        r = r.transformation
    else:
        r = gt_trans

    # skip transformation refinement
    # r = gt_trans
    # no crop volume
    vol = []

    # Histogramms and P/R/F1
    plot_stretch = 5
    [precision, recall, fscore, edges_source, cum_source,
     edges_target, cum_target] = EvaluateHisto(
        pcd, gt_pcd, r, vol, dTau / 2.0, dTau,
        mvs_outpath, plot_stretch, scene_name)
    eva = [precision, recall, fscore]
    print("==============================")
    print("evaluation result : %s" % scene_name)
    print("==============================")
    print("distance tau : %.3f" % dTau)
    print("precision : %.4f" % eva[0])
    print("recall : %.4f" % eva[1])
    print("f-score : %.4f" % eva[2])
    print("==============================")

    # Plotting
    plot_graph(scene_name, fscore, dist_threshold, edges_source, cum_source,
               edges_target, cum_target, plot_stretch, mvs_outpath)


if __name__ == "__main__":
    run_evaluation()

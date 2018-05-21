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


# ----------------------------------------------------------------------------
# INSTRUCTION
# ----------------------------------------------------------------------------

# STEP 0) Specify the path where training dataset folder is located.
DATASET_DIR = "/home/v4rl/data/unreal_statue/"

# STEP 1) this evaluation script require Open3D python binding
# to install Open3D, please start from http://open3d.org/docs/getting_started.html

# STEP 2) specify path to where Open3D build is
OPEN3D_BUILD_PATH = "/home/v4rl/repo/Open3D/build/"

# STEP 3) specify path to where
# py3d.so, py3d_[python_version].so or py3d.lib is located
OPEN3D_PYTHON_LIBRARY_PATH = OPEN3D_BUILD_PATH + "lib/" # Mac/Ubuntu

# STEP 4) specify path to where
# Open3D"s experimental applications (ViewDistances and ConvertPointCloud)
OPEN3D_EXPERIMENTAL_BIN_PATH = OPEN3D_BUILD_PATH + "bin/Experimental/" # Mac/Ubuntu

# STEP 5) Set the names for ground truth and reconstruction pointclouds
GROUND_TRUTH_FILE = "statue_ground_truth.ply"
RECONSTRUCTION_FILE = "recon_cropped.ply"

# STEP 5) Set the names for the transformation file from ground truth to reconstructed pointcloud
TRANSFORMATION_FILE = "unreal_statue_trans.txt"

# STEP 6) Set the evaluation parameters
threshold = 0.1
do_ICP = False

# ----------------------------------------------------------------------------
# END OF INSTRUCTION
# ----------------------------------------------------------------------------

if OPEN3D_BUILD_PATH is None:
    raise SystemExit("Error:: [OPEN3D_BUILD_PATH] in setup.py is not defined")
if OPEN3D_PYTHON_LIBRARY_PATH is None:
    raise SystemExit("Error:: [OPEN3D_PYTHON_LIBRARY_PATH] in setup.py is not defined")
if OPEN3D_EXPERIMENTAL_BIN_PATH is None:
    raise SystemExit("Error:: [OPEN3D_EXPERIMENTAL_BIN_PATH] in setup.py is not defined")
if RECONSTRUCTION_FILE is None:
    raise SystemExit("Error:: [RECONSTRUCTION_FILE] in setup.py is not defined")
if GROUND_TRUTH_FILE is None:
    raise SystemExit("Error:: [GROUND_TRUTH_FILE] in setup.py is not defined")

import sys
sys.path.append(OPEN3D_PYTHON_LIBRARY_PATH)
try:
    from py3d import *
except:
    raise SystemExit("Error:: please correctly set paths for Open3D in setup.py")

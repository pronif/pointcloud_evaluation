# Pointcloud Evaluation

These scripts evaluate the *precision* (accuracy) and *recall* (completeness) of a reconstructed pointcloud against a 
ground truth pointcloud.

The code is forked form [Tanks and Temples](https://github.com/IntelVCL/TanksAndTemples.git). 
See the linked paper for more information about the methodology and the measures.

### Input
* Ground truth pointcloud
* Reconstructed pointcloud
* Threshold (distance below which a point is considered inlier)
* [Optional] Homogeneous transform between the GT and reconstruction

*Note:* The pointclouds are assumed to be aligned.
There is the option to input a transform file from GT to reconstruction in numpy format.
You can set the option do_ICP to true if you want to run ICP based alignment.

### Output
Precision, recall and F1 score with the given threshold.

Precision and recall curve

## How to use:
**Step 0**. Install Open3D. Follow instructions from [http://open3d.org/docs/getting_started.html]
Checkout release v0.1.1, because of major API changes in subsequent versions.

**Step 1** Follow the instructions in setup.py

**Step 2** Execute with `python run.py`
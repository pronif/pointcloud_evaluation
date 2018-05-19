# Pointcloud Evaluation

These scripts evaluate the a pointcloud against a pointcloud ground truth. The *precision* (accuracy) and *recall* (completeness) of the tested pointcloud are calculated at different thresholds to output a precision-recall curve.

The code is forked form [Tanks and Temples](https://github.com/IntelVCL/TanksAndTemples.git). See the linked paper for more information on the methology and on the measures.

## How to use:
**Step 0**. Install Open3D. Follow instructions from http://open3d.org/docs/getting_started.html
Chekout release v0.1.1, because of major API changes in subsequent versions.

#!/bin/bash

PATH=/esmmc/spIsoNet/bin:$PATH
export PATH
# do not use ~/.local python
PYTHONNOUSERSITE=1
export PYTHONNOUSERSITE
export CONDA_ROOT=/esmmc/spIsoNet
eval "$(${CONDA_ROOT}/bin/conda shell.bash hook)"
export CONDA_ENV="spisonet"
export RELION_EXTERNAL_RECONSTRUCT_EXECUTABLE="python /esmmc/spIsoNet/envs/spisonet/lib/python3.10/site-packages/spIsoNet/bin/relion_wrapper.py"
conda activate spisonet
module use /esmmc/modulefiles
module add cuda/11.6.0_510.39.01  gcc/8.2.1-devtoolset-8
spisonet.py "$@"

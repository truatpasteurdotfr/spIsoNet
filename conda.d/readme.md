install miniconda in /esmmc with `install-miniconda3-spIsoNet.sh`
conda create -n spisonet python=3.10
conda activate spisonet
# using cuda 12.1 (as of 2024/04/16)
pip3 install torch torchvision torchaudio
git clone https://github.com/IsoNet-cryoET/spIsoNet
cd spIsoNet
python3 -m pip install .
# export conda setup with the `conda-yaml.sh` script and `pip freese`
# create script with recent enough cuda and gcc version (as we are using centos7)


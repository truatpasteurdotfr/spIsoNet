#!/bin/sh
PATH=/sbin:/usr/sbin:/usr/bin:/bin

set -e
set -u

tbindir=$(mktemp -d)
trap "rm -rf \"$tbindir\"" TERM INT EXIT

export TMPDIR=`mktemp -d /dev/shm/${USER}-XXXXX`
miniconda3=/esmmc/spIsoNet 

_install() {
cd $tbindir && \
curl -qsSLkO https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
&& bash Miniconda3-latest-Linux-x86_64.sh -b -p ${miniconda3} \
&& rm Miniconda3-latest-Linux-x86_64.sh
${miniconda3}/bin/conda update conda -y && ${miniconda3}/bin/conda update --all -y
}

_install
_o=~/bin/enable-miniconda3-spIsoNet.sh
[ ! -d ~/bin ] && mkdir -p ~/bin 
cat <<EOF > ${_o}
PATH=${miniconda3}/bin:\$PATH
export PATH
# do not use ~/.local python
PYTHONNOUSERSITE=1
export PYTHONNOUSERSITE
export CONDA_ROOT=${miniconda3}
eval "\$(\${CONDA_ROOT}/bin/conda shell.bash hook)"
EOF
chmod 755 ${_o}

echo "${_o} created, to activate this conda installation:"
echo "source ${_o}"


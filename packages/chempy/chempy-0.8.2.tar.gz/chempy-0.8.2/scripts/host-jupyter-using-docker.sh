#!/bin/bash -ue
#
# This script requires that Docker is installed.
#
# Arguments: mount-path, port-number, Dockerfile-path
#
# To host a local jupyter notebook server rung e.g.:
#
#  $ ./scripts/host-jupyter-using-docker.sh
#  $ ./scripts/host-jupyter-using-docker.sh . 8888 ./scripts/environment
#
# To instead run the test suite, specify "0" as the port number:
#
#  $ ./scripts/host-jupyter-using-docker.sh . 0 ./scripts/environment
#
MOUNT=${1:-.}
PORT=${2:-8888}
DOCKERIMAGE=${3:-./scripts/environment}
PKG=$(find . -maxdepth 2 -name __init__.py -print0 | xargs -0 -n1 dirname | xargs basename)
HOST_USER=${SUDO_USER:-${LOGNAME}}
if [[ "${HOST_USER}" == root ]]; then
    >&2 echo "Need another user name than root (pip will fail)"
    exit 1
fi
if [[ "$MOUNT" == .* ]]; then
    MOUNT="$(pwd)/$MOUNT"
fi
if [[ "$DOCKERIMAGE" == ./* ]]; then
    DOCKERIMAGE=$(sudo docker build $DOCKERIMAGE | tee /dev/tty | tail -1 | cut -d' ' -f3)
fi
if [[ "$PORT" == "0" ]]; then
    LOCALCMD="pytest -sv -ra --pyargs $PKG"
    PORTFWD=""
else
    LOCALCMD="jupyter notebook --no-browser --port $PORT --ip=* index.ipynb"
    PORTFWD="-p ${4:-127.0.0.1}:$PORT:$PORT"
fi
MYCMD="groupadd -f --gid \$HOST_GID \$HOST_WHOAMI; \
useradd --uid \$HOST_UID --gid \$HOST_GID --home /mount \$HOST_WHOAMI; \
sudo --login -u \$HOST_WHOAMI PYCVODES_NO_LAPACK=1 PYCVODES_NO_KLU=1 python3 -m pip install --user -e .[all]; \
sudo --login -u \$HOST_WHOAMI /mount/.local/bin/jupyter-nbextension enable --user --py widgetsnbextension; \
sudo --login -u \$HOST_WHOAMI LD_LIBRARY_PATH=/usr/local/lib MPLBACKEND=Agg /mount/.local/bin/$LOCALCMD"
set -x
sudo docker run --rm --name "${PKG}_nb_${PORT}" $PORTFWD \
 -e HOST_WHOAMI=${HOST_USER} -e HOST_UID=$(id -u ${HOST_USER}) -e HOST_GID=$(id -g ${HOST_USER})\
 -v $MOUNT:/mount -w /mount -it $DOCKERIMAGE /bin/bash -x -c "$MYCMD"

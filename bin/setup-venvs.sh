#!/bin/bash
# shellcheck disable=SC1090
#set -euo pipefail


function setup-venv {
    echo "Setting up $1"
    python3 -m venv "$HOME/www/python/$1"
    . "$HOME/www/python/$1/bin/activate"
    python3 -m pip install -U pip setuptools wheel
    python -m pip install requests
    python -m pip install pyyaml
    # shellcheck disable=SC2086
    python3 -m pip install $2
    deactivate
}

setup-venv venv "-U -r $HOME/www/python/app/requirements.txt"



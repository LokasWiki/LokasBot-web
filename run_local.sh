# run setup on local machine
# create virtual environment and install dependencies
python3 -m venv .venv
# activate virtual environment
source .venv/bin/activate
# upgrade pip
python3 -m pip install -U pip setuptools wheel
# install dependencies
python -m pip install requests
python -m pip install pyyaml
# install dependencies from requirements.txt
pip install -r requirements.txt
# install dependencies from requirements-dev.txt
pip install -r requirements-dev.txt

copier -r cc292cf
py -3.9 -m venv .venv
.venv/Scripts/activate
pip install -U pip  # throws [WinError 5], but still works on its own
pip install wheel
pip install -r tooling/requirements_dev.txt
python tooling/bump_pyproject.py
flit install -s

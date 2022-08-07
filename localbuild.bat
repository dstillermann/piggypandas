@echo off
python -m build --sdist
python -m build --wheel
python -m pip install -e .
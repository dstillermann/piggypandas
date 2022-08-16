@echo off
del /Q dist\*.*
python -m build --sdist
python -m build --wheel
python -m pip install -e .
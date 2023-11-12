@echo off
del /Q dist\*.*
python -m build --sdist
python -m build --wheel
rem python -m pip install -e .
python -m pip uninstall -y piggypandas
for %%f in ( dist\*.whl ) do python -m pip install "%%f"
@echo off
twine check dist/*
twine upload dist/* --verbose
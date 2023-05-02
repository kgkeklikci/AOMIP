## Important
* Please execute all scripts from repository root directory.

## Requirements
* Inside the homework file, you will find a `requirements.txt` file for dependencies.
* Arguably if not the most, one of the most important dependencies is the [python-dotenv]("https://pypi.org/project/python-dotenv/") package, which configures the script variables from a sourced `.env` file. To establish this, `.gitignore` was modified accordingly.
* Please download this [dataset](https://zenodo.org/record/2688112#.ZFBTsOxByu4) and place it under a folder named `datasets` in repository root.

## Homework 3: Preprocessing for computed tomography
* Execute the following script to generate the output for flat-field correction.
* `python -B homework/hw01/preprocessor.py`
* Script loads the [raw](https://gitlab.lrz.de/IP/teaching/applied-optimization-methods-for-inverse-problems/aomip-kaan-guney-keklikci/-/tree/main/homework/hw01/output/scan/raw) input files, stores them into matrices and performs flat-field correction given the formula. 
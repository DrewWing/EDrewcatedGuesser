
# setup.py
# by Drew Wingfield
# part of the FTCAPI project

# With help from 
# https://stackoverflow.com/questions/26900328/install-dependencies-from-setup-py
# for stuff with setup.py and requirements.txt
# The below code was copied and modified from hayj on that page.

import os
import setuptools

lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = f"{lib_folder}/requirements.txt"
install_requires = [] # Here we'll add: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()

setuptools.setup(name="mypackage", install_requires=install_requires)
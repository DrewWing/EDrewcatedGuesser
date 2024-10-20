# Guide to Machine Learning in this Project

# <p style="color:red"><u>**This Documentation is currently OUTDATED**</u></p>

The machine learning algorithm is just fine on its own, and you should not retrain it unless you know what you are doing. \
If you *are* retraining the algorithm, follow these steps.
1. Run `update-dataset-global.sh` to gather the data (uses `opr/all-events`).
2. Run `prepare-machinelearning.py` to process the data (creates `machinefile.csv`).
3. Actually train the algorithm by running the `ml-test.py` program (uses `machinefile.csv`).


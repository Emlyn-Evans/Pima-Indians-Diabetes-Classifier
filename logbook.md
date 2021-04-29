# Logbook

This is a logbook to track that work that we've done so that we know where we
are up to.

## TODO
- Actual cross validation of NB and DT
- Section 5: Weka classifiers

## 27/4/21 - Emlyn

- Added pima.csv file using Weka instructions
- Completed Naive Bayes
- Did some preliminary testing on NB using the weather example

## 28/4/21 - Emlyn

- Added the initial decision tree, needs testing
- Started printing the tree in order to check the correctness

## 29/4/21 - Emlyn

- Tested decision tree on weather data, found bugs and fixed them
- Investigated decision tree with original dataset with csv filters to confirm
- Finalised decision tree
- Added n-folds sample splitter
- Completed Section 4, Feature selection

### Note about CFS
Attributes kept with indexes:
- 1: Plasma Glucose Concentration
- 4: 2-hour Serum Insulin
- 5: Body Mass Index
- 6: Diabetes Pedigree Function
- 7: Age

Removed:
- 0: Pregnancies
- 2: Diastolic Blood Pressure
- 3: Triceps Skin Fold Thickness
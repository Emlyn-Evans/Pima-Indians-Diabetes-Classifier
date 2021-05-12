# Logbook

This is a logbook to track that work that we've done so that we know where we
are up to.


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
- Completed Section 4, Feature 

## 2/5/21 - Emlyn

- Implemented Cross Validation of NB and DT to give us an accuracy score
- First submission
- Implemented gain ratio for DTs and refined stopping conditions
- Implemented handling for when we encounter new categories when predicting
- Final submission

## 11/5/21 - Archie
- Begin report write-up on Overleaf
- Finished Introduction section (subject to review) and began Data section
- Need to add why the features were chosen during CFS

## 12/5/21 - Emlyn
- Added CFS files with headers
- Did WEKA classifiers with Archie
- Corrected some errors with comments and code

## 12/5/21 - Archie

- Verified Weka results and our code's results along with Emlyn
- Added table of results to Overleaf


# Notes

### Note 1 about DTs
I think we always prefer to use gain ratio over information gain as if splitting
between two attributes produces the same information gain, the gain ratio will
at least choose the attribute with less categories, which makes the tree
simpler. If the attributes have the same number of categories, then the gain
ratio is the same as the information gain anyway.
However, using gain ratio makes me fail a testcase so information gain it is.
Talk about gain ratio in the report.

### Note 2 about DTs
If the DT encounters a category to split that it hasn't seen before when
predicting, we must handle it in some way. A simple approach is the take the
average of yes and no predictions of the node as a prediction. The issue with
this is that if we encounter something new at the root, then we are basically
taking a random guess.
A more interesting and cooler approach is to take a weighted average of all possible
branches for the splits that we do have. Here, we include the probability of
different categories for this attribute but also extract as much information
from other attributes as possible.
I think the most accurate approach is
to split it down the closest branches (if we have low, then we send it down
medium, and if we have medium, we send it down low and high). However, this
approach raises issues as it isn't generalisable for all categories as we don't
know which we will have, and we might not have multiple. Hence, the middle
approach was taken.


### Note about CV
10 Fold Cross Validation Accuracy
- NB: 0.7460526315789474
- DT: 0.746138072453862

Other DT accuracies based off subtle changes in algorithm:
- DT test unseen path average with information gain: 0.746138072453862
- DT test unseen node majority with information gain: 0.7474367737525631
- DT empty category majority wth unseen path average with gain ratio: 0.7396103896103896
- DT empty category majority with unseen node majority with gain ratio: 0.740909090909091

Training and testing with the full dataset
- NB: 0.7526041666666666
- DT: 0.8216145833333334

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


### Note about 10-CV
I need to modularise the training and testing of both NB and DT. I need to be
able to feed NB a dataset for it to work off, and feed DT a dataset rather than
using the whole training dataset. I also need the testing functions to return a
list of yes/no for each thing to test from. I will print the regular ones and
use the 10-CV ones to create accuracy metrics.


### Note on Printing DTs
FULL TREE
Plasma Glucose Concentration = high
|    Body Mass Index = high
|    |    Age = high
|    |    |    Diabetes Pedigree Function = high
|    |    |    |    Diastolic Blood Pressure = high
|    |    |    |    |    Pregnancies = low
|    |    |    |    |    |    Triceps Skin Fold Thickness = high
|    |    |    |    |    |    |    2-hour Serum Insulin = high: yes (9/4)
|    |    |    |    |    |    |    2-hour Serum Insulin = low: yes (1/0)
|    |    |    |    |    |    Triceps Skin Fold Thickness = low: yes (1/0)
|    |    |    |    |    Pregnancies = high: yes (12/2)
|    |    |    |    Diastolic Blood Pressure = low
|    |    |    |    |    Pregnancies = low: yes (1/1)
|    |    |    |    |    Pregnancies = high: no (2/0)
|    |    |    Diabetes Pedigree Function = low
|    |    |    |    2-hour Serum Insulin = high
|    |    |    |    |    Triceps Skin Fold Thickness = high
|    |    |    |    |    |    Diastolic Blood Pressure = high
|    |    |    |    |    |    |    Pregnancies = high: yes (9/6)
|    |    |    |    |    |    |    Pregnancies = low: no (12/11)
|    |    |    |    |    |    Diastolic Blood Pressure = low
|    |    |    |    |    |    |    Pregnancies = low: yes (2/1)
|    |    |    |    |    |    |    Pregnancies = high: yes (3/0)
|    |    |    |    |    Triceps Skin Fold Thickness = low
|    |    |    |    |    |    Pregnancies = low
|    |    |    |    |    |    |    Diastolic Blood Pressure = high: yes (1/1)
|    |    |    |    |    |    |    Diastolic Blood Pressure = low: no (1/0)
|    |    |    |    |    |    Pregnancies = high: no (1/0)
|    |    |    |    2-hour Serum Insulin = low: yes (1/0)
|    |    Age = low
|    |    |    Triceps Skin Fold Thickness = high
|    |    |    |    Diabetes Pedigree Function = low
|    |    |    |    |    Diastolic Blood Pressure = high: no (12/8)
|    |    |    |    |    Diastolic Blood Pressure = low: yes (4/3)
|    |    |    |    Diabetes Pedigree Function = high
|    |    |    |    |    Diastolic Blood Pressure = high: yes (6/5)
|    |    |    |    |    Diastolic Blood Pressure = low: no (3/2)
|    |    |    Triceps Skin Fold Thickness = low
|    |    |    |    Diastolic Blood Pressure = high: no (3/0)
|    |    |    |    Diastolic Blood Pressure = low
|    |    |    |    |    2-hour Serum Insulin = high
|    |    |    |    |    |    Diabetes Pedigree Function = high: yes (1/1)
|    |    |    |    |    |    Diabetes Pedigree Function = low: no (1/0)
|    |    |    |    |    2-hour Serum Insulin = low: no (1/0)
|    Body Mass Index = low
|    |    Triceps Skin Fold Thickness = high
|    |    |    2-hour Serum Insulin = high
|    |    |    |    Diabetes Pedigree Function = high: no (5/0)
|    |    |    |    Diabetes Pedigree Function = low
|    |    |    |    |    Age = high
|    |    |    |    |    |    Diastolic Blood Pressure = high: no (5/1)
|    |    |    |    |    |    Diastolic Blood Pressure = low: no (2/0)
|    |    |    |    |    Age = low
|    |    |    |    |    |    Diastolic Blood Pressure = low: yes (2/2)
|    |    |    |    |    |    Diastolic Blood Pressure = high: no (1/0)
|    |    |    2-hour Serum Insulin = low
|    |    |    |    Diabetes Pedigree Function = high: yes (1/0)
|    |    |    |    Diabetes Pedigree Function = low: no (1/0)
|    |    Triceps Skin Fold Thickness = low: no (9/0)
Plasma Glucose Concentration = low
|    Body Mass Index = low: no (66/0)
|    Body Mass Index = high
|    |    2-hour Serum Insulin = high
|    |    |    Age = low
|    |    |    |    Diastolic Blood Pressure = low
|    |    |    |    |    Triceps Skin Fold Thickness = low: no (7/0)
|    |    |    |    |    Triceps Skin Fold Thickness = high
|    |    |    |    |    |    Diabetes Pedigree Function = low: no (9/3)
|    |    |    |    |    |    Diabetes Pedigree Function = high: no (5/1)
|    |    |    |    Diastolic Blood Pressure = high: no (18/0)
|    |    |    Age = high
|    |    |    |    Diabetes Pedigree Function = low
|    |    |    |    |    Triceps Skin Fold Thickness = high
|    |    |    |    |    |    Pregnancies = high
|    |    |    |    |    |    |    Diastolic Blood Pressure = high: no (8/1)
|    |    |    |    |    |    |    Diastolic Blood Pressure = low: no (1/0)
|    |    |    |    |    |    Pregnancies = low
|    |    |    |    |    |    |    Diastolic Blood Pressure = high: no (11/2)
|    |    |    |    |    |    |    Diastolic Blood Pressure = low: no (3/1)
|    |    |    |    |    Triceps Skin Fold Thickness = low: no (1/0)
|    |    |    |    Diabetes Pedigree Function = high
|    |    |    |    |    Diastolic Blood Pressure = high: yes (3/3)
|    |    |    |    |    Diastolic Blood Pressure = low: yes (1/0)
|    |    2-hour Serum Insulin = low
|    |    |    Diastolic Blood Pressure = high
|    |    |    |    Age = high: no (12/0)
|    |    |    |    Age = low
|    |    |    |    |    Triceps Skin Fold Thickness = high
|    |    |    |    |    |    Diabetes Pedigree Function = low: no (5/1)
|    |    |    |    |    |    Diabetes Pedigree Function = high: yes (1/0)
|    |    |    |    |    Triceps Skin Fold Thickness = low: no (6/0)
|    |    |    Diastolic Blood Pressure = low: no (23/0)
Plasma Glucose Concentration = very high
|    2-hour Serum Insulin = high
|    |    Body Mass Index = low
|    |    |    Age = high
|    |    |    |    Triceps Skin Fold Thickness = high
|    |    |    |    |    Pregnancies = high
|    |    |    |    |    |    Diabetes Pedigree Function = high
|    |    |    |    |    |    |    Diastolic Blood Pressure = low: yes (1/0)
|    |    |    |    |    |    |    Diastolic Blood Pressure = high: yes (1/1)
|    |    |    |    |    |    Diabetes Pedigree Function = low: yes (2/0)
|    |    |    |    |    Pregnancies = low: yes (2/2)
|    |    |    |    Triceps Skin Fold Thickness = low: yes (3/0)
|    |    |    Age = low
|    |    |    |    Diastolic Blood Pressure = low: no (1/0)
|    |    |    |    Diastolic Blood Pressure = high
|    |    |    |    |    Triceps Skin Fold Thickness = low: yes (1/1)
|    |    |    |    |    Triceps Skin Fold Thickness = high: no (1/0)
|    |    Body Mass Index = high
|    |    |    Pregnancies = low
|    |    |    |    Age = high
|    |    |    |    |    Diabetes Pedigree Function = low
|    |    |    |    |    |    Diastolic Blood Pressure = high
|    |    |    |    |    |    |    Triceps Skin Fold Thickness = high: yes (14/2)
|    |    |    |    |    |    |    Triceps Skin Fold Thickness = low: yes (3/0)
|    |    |    |    |    |    Diastolic Blood Pressure = low
|    |    |    |    |    |    |    Triceps Skin Fold Thickness = low: yes (1/1)
|    |    |    |    |    |    |    Triceps Skin Fold Thickness = high: yes (3/0)
|    |    |    |    |    Diabetes Pedigree Function = high
|    |    |    |    |    |    Triceps Skin Fold Thickness = high
|    |    |    |    |    |    |    Diastolic Blood Pressure = high: yes (10/5)
|    |    |    |    |    |    |    Diastolic Blood Pressure = low: yes (1/1)
|    |    |    |    |    |    Triceps Skin Fold Thickness = low: yes (1/0)
|    |    |    |    Age = low
|    |    |    |    |    Diabetes Pedigree Function = high: yes (12/0)
|    |    |    |    |    Diabetes Pedigree Function = low
|    |    |    |    |    |    Triceps Skin Fold Thickness = high
|    |    |    |    |    |    |    Diastolic Blood Pressure = high: yes (7/2)
|    |    |    |    |    |    |    Diastolic Blood Pressure = low: yes (3/0)
|    |    |    |    |    |    Triceps Skin Fold Thickness = low
|    |    |    |    |    |    |    Diastolic Blood Pressure = high: yes (1/0)
|    |    |    |    |    |    |    Diastolic Blood Pressure = low: no (1/0)
|    |    |    Pregnancies = high
|    |    |    |    Diabetes Pedigree Function = high: yes (16/0)
|    |    |    |    Diabetes Pedigree Function = low
|    |    |    |    |    Diastolic Blood Pressure = high: yes (12/3)
|    |    |    |    |    Diastolic Blood Pressure = low: yes (3/1)
|    2-hour Serum Insulin = low
|    |    Diabetes Pedigree Function = low: no (2/0)
|    |    Diabetes Pedigree Function = high: yes (1/0)
Plasma Glucose Concentration = medium
|    Age = high
|    |    Body Mass Index = low
|    |    |    Diastolic Blood Pressure = high
|    |    |    |    Pregnancies = low
|    |    |    |    |    Diabetes Pedigree Function = low
|    |    |    |    |    |    Triceps Skin Fold Thickness = high: no (2/1)
|    |    |    |    |    |    Triceps Skin Fold Thickness = low: no (2/0)
|    |    |    |    |    Diabetes Pedigree Function = high: no (3/0)
|    |    |    |    Pregnancies = high: no (13/0)
|    |    |    Diastolic Blood Pressure = low
|    |    |    |    Pregnancies = low
|    |    |    |    |    Triceps Skin Fold Thickness = high: no (5/0)
|    |    |    |    |    Triceps Skin Fold Thickness = low: no (2/1)
|    |    |    |    Pregnancies = high: yes (1/0)
|    |    Body Mass Index = high
|    |    |    Diabetes Pedigree Function = low
|    |    |    |    2-hour Serum Insulin = high
|    |    |    |    |    Diastolic Blood Pressure = high
|    |    |    |    |    |    Pregnancies = high: no (14/12)
|    |    |    |    |    |    Pregnancies = low
|    |    |    |    |    |    |    Triceps Skin Fold Thickness = high: no (18/11)
|    |    |    |    |    |    |    Triceps Skin Fold Thickness = low: yes (1/1)
|    |    |    |    |    Diastolic Blood Pressure = low
|    |    |    |    |    |    Triceps Skin Fold Thickness = high
|    |    |    |    |    |    |    Pregnancies = high: yes (3/3)
|    |    |    |    |    |    |    Pregnancies = low: yes (5/4)
|    |    |    |    |    |    Triceps Skin Fold Thickness = low: no (2/1)
|    |    |    |    2-hour Serum Insulin = low: no (5/0)
|    |    |    Diabetes Pedigree Function = high
|    |    |    |    Pregnancies = low
|    |    |    |    |    Triceps Skin Fold Thickness = high
|    |    |    |    |    |    Diastolic Blood Pressure = high: yes (9/7)
|    |    |    |    |    |    Diastolic Blood Pressure = low: yes (3/3)
|    |    |    |    |    Triceps Skin Fold Thickness = low: yes (2/0)
|    |    |    |    Pregnancies = high: yes (13/0)
|    Age = low
|    |    Body Mass Index = high
|    |    |    Triceps Skin Fold Thickness = high
|    |    |    |    Pregnancies = low
|    |    |    |    |    Diabetes Pedigree Function = high
|    |    |    |    |    |    Diastolic Blood Pressure = high
|    |    |    |    |    |    |    2-hour Serum Insulin = high: no (12/2)
|    |    |    |    |    |    |    2-hour Serum Insulin = low: no (3/0)
|    |    |    |    |    |    Diastolic Blood Pressure = low
|    |    |    |    |    |    |    2-hour Serum Insulin = high: yes (3/3)
|    |    |    |    |    |    |    2-hour Serum Insulin = low: yes (1/0)
|    |    |    |    |    Diabetes Pedigree Function = low
|    |    |    |    |    |    Diastolic Blood Pressure = low
|    |    |    |    |    |    |    2-hour Serum Insulin = high: no (18/2)
|    |    |    |    |    |    |    2-hour Serum Insulin = low: no (5/1)
|    |    |    |    |    |    Diastolic Blood Pressure = high
|    |    |    |    |    |    |    2-hour Serum Insulin = high: no (20/5)
|    |    |    |    |    |    |    2-hour Serum Insulin = low: no (3/0)
|    |    |    |    Pregnancies = high: yes (1/1)
|    |    |    Triceps Skin Fold Thickness = low
|    |    |    |    Diabetes Pedigree Function = high
|    |    |    |    |    Diastolic Blood Pressure = low
|    |    |    |    |    |    2-hour Serum Insulin = high: no (3/1)
|    |    |    |    |    |    2-hour Serum Insulin = low: no (2/0)
|    |    |    |    |    Diastolic Blood Pressure = high: no (4/0)
|    |    |    |    Diabetes Pedigree Function = low: no (14/0)
|    |    Body Mass Index = low
|    |    |    Diabetes Pedigree Function = low: no (34/0)
|    |    |    Diabetes Pedigree Function = high
|    |    |    |    2-hour Serum Insulin = high: no (5/0)
|    |    |    |    2-hour Serum Insulin = low
|    |    |    |    |    Diastolic Blood Pressure = low: yes (1/1)
|    |    |    |    |    Diastolic Blood Pressure = high: no (1/0)


CFS TREE
Plasma Glucose Concentration = high
|    Body Mass Index = high
|    |    Age = high
|    |    |    Diabetes Pedigree Function = high
|    |    |    |    2-hour Serum Insulin = high: yes (23/9)
|    |    |    |    2-hour Serum Insulin = low: yes (1/0)
|    |    |    Diabetes Pedigree Function = low
|    |    |    |    2-hour Serum Insulin = high: yes (26/22)
|    |    |    |    2-hour Serum Insulin = low: yes (1/0)
|    |    Age = low
|    |    |    2-hour Serum Insulin = high
|    |    |    |    Diabetes Pedigree Function = low: no (18/12)
|    |    |    |    Diabetes Pedigree Function = high: no (10/9)
|    |    |    2-hour Serum Insulin = low: no (1/0)
|    Body Mass Index = low
|    |    2-hour Serum Insulin = high
|    |    |    Diabetes Pedigree Function = high: no (6/0)
|    |    |    Diabetes Pedigree Function = low
|    |    |    |    Age = high: no (8/1)
|    |    |    |    Age = low: no (8/2)
|    |    2-hour Serum Insulin = low
|    |    |    Diabetes Pedigree Function = high
|    |    |    |    Age = low: no (1/0)
|    |    |    |    Age = high: yes (1/0)
|    |    |    Diabetes Pedigree Function = low: no (2/0)
Plasma Glucose Concentration = low
|    Body Mass Index = low: no (66/0)
|    Body Mass Index = high
|    |    2-hour Serum Insulin = high
|    |    |    Age = low
|    |    |    |    Diabetes Pedigree Function = low: no (28/3)
|    |    |    |    Diabetes Pedigree Function = high: no (11/1)
|    |    |    Age = high
|    |    |    |    Diabetes Pedigree Function = low: no (24/4)
|    |    |    |    Diabetes Pedigree Function = high: yes (4/3)
|    |    2-hour Serum Insulin = low
|    |    |    Age = high: no (16/0)
|    |    |    Age = low
|    |    |    |    Diabetes Pedigree Function = low: no (21/1)
|    |    |    |    Diabetes Pedigree Function = high: no (9/1)
Plasma Glucose Concentration = 'very high'
|    2-hour Serum Insulin = high
|    |    Body Mass Index = low
|    |    |    Age = high: yes (9/3)
|    |    |    Age = low
|    |    |    |    Diabetes Pedigree Function = high: no (1/0)
|    |    |    |    Diabetes Pedigree Function = low: no (2/1)
|    |    Body Mass Index = high
|    |    |    Age = high
|    |    |    |    Diabetes Pedigree Function = low: yes (36/7)
|    |    |    |    Diabetes Pedigree Function = high: yes (28/6)
|    |    |    Age = low
|    |    |    |    Diabetes Pedigree Function = high: yes (12/0)
|    |    |    |    Diabetes Pedigree Function = low: yes (11/3)
|    2-hour Serum Insulin = low
|    |    Diabetes Pedigree Function = low: no (2/0)
|    |    Diabetes Pedigree Function = high: yes (1/0)
Plasma Glucose Concentration = medium
|    Age = high
|    |    Body Mass Index = low
|    |    |    2-hour Serum Insulin = high
|    |    |    |    Diabetes Pedigree Function = low: no (13/2)
|    |    |    |    Diabetes Pedigree Function = high: no (11/1)
|    |    |    2-hour Serum Insulin = low: no (3/0)
|    |    Body Mass Index = high
|    |    |    Diabetes Pedigree Function = low
|    |    |    |    2-hour Serum Insulin = high: no (42/33)
|    |    |    |    2-hour Serum Insulin = low: no (5/0)
|    |    |    Diabetes Pedigree Function = high: yes (27/10)
|    Age = low
|    |    Body Mass Index = high
|    |    |    Diabetes Pedigree Function = high
|    |    |    |    2-hour Serum Insulin = high: no (22/6)
|    |    |    |    2-hour Serum Insulin = low: no (5/1)
|    |    |    Diabetes Pedigree Function = low
|    |    |    |    2-hour Serum Insulin = high: no (51/8)
|    |    |    |    2-hour Serum Insulin = low: no (10/1)
|    |    Body Mass Index = low
|    |    |    Diabetes Pedigree Function = low: no (34/0)
|    |    |    Diabetes Pedigree Function = high
|    |    |    |    2-hour Serum Insulin = high: no (5/0)
|    |    |    |    2-hour Serum Insulin = low: no (2/1)



# Reflection Stuff:
- It's fun and interesting to implement these by yourself, and compare to black
  box ones from Weka.
- Naive Bayes is actually super simple but powerful - it's amazing that you can
  get a good classifier from just the mean and var of some attribute.
- Interesting how many different fine tuning things you can do for DTs, like
  using information gain or gain ratio, or splitting unseen categories down
  known ones and taking weighted average or just taking majority class.


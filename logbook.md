# Logbook

This is a logbook to track that work that we've done so that we know where we
are up to.

## TODO
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
- Completed Section 4, Feature 

## 2/5/21 - Emlyn

- Implemented Cross Validation of NB and DT to give us an accuracy score
- First submission
- Implemented gain ratio for DTs and refined stopping conditions
- Implemented handling for when we encounter new categories when predicting
- Final submission


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



# Reflection Stuff:
- It's fun and interesting to implement these by yourself, and compare to black
  box ones from Weka.
- Naive Bayes is actually super simple but powerful - it's amazing that you can
  get a good classifier from just the mean and var of some attribute.
- Interesting how many different fine tuning things you can do for DTs, like
  using information gain or gain ratio, or splitting unseen categories down
  known ones and taking weighted average or just taking majority class.
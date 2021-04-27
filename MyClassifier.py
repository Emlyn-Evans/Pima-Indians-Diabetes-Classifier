"""My Classifier"""

import sys

# TODO: Extract Data
def extract_data(filename, numeric=True):

    # We aren't certain to receive a csv file, so we can't use csv module
    data = []

    with open(filename, "r") as file:

        lines = file.readlines()

        for i in lines:

            row = []

            strings = i.strip().split(",")

            for j in range(len(strings)):

                entry = strings[j]

                # Handling for numeric or discrete
                if numeric is True:

                    if j < 8:

                        entry = float(entry)

                row.append(entry)

            data.append(row)

    return data


def train_naive_bayes(training_data):

    return


# TODO: Naive Bayes
def naive_bayes(training_file, testing_file):

    training_data = extract_data(training_file, True)
    testing_data = extract_data(testing_file, True)

    train_naive_bayes(training_data)

    # Find mean and sd for normal

    return


# TODO: Decision Tree
def decision_tree():

    return


# Run with: python3 MyClassifier.py pima.csv ? NB
# Run with: python3 MyClassifier.py pima-indians-diabetes.discrete ? DT

# Reading command line arguments
training_file = sys.argv[1]
testing_file = sys.argv[2]
algorithm = sys.argv[3]

numeric = True

if algorithm == "DT":

    numeric = False

data = extract_data(training_file, numeric)

for i in data:

    print(i)
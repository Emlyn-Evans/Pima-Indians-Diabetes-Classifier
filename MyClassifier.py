"""My Classifier"""

import sys
import math
import random
from decision_tree import Decision_Tree


class Classifier:
    def __init__(self, training_file, testing_file, algorithm):

        self.training_file = training_file
        self.testing_file = testing_file
        self.algorithm = algorithm
        self.n_attributes = None
        self.n_training = None
        self.n_testing = None
        self.training_data = None
        self.training_labels = None
        self.testing_data = None

        # Extract the training and testing data
        self.training_data, self.training_labels = self.extract_data(self.training_file)
        self.n_training = len(self.training_data)
        self.testing_data = self.extract_data(self.testing_file)[0]
        self.n_testing = len(self.testing_data)

        if self.algorithm == "NB":

            self.naive_bayes()

        else:

            self.decision_tree()

    def extract_data(self, filename):

        # We aren't certain to receive a csv file, so we can't use csv module
        data = []
        labels = []

        with open(filename, "r") as file:

            lines = file.readlines()

            for i in lines:

                row = []

                strings = i.strip().split(",")

                if self.n_attributes is None:

                    self.n_attributes = len(strings) - 1

                for j in range(self.n_attributes):

                    entry = strings[j]

                    # Handling for numeric or discrete
                    if self.algorithm == "NB":

                        entry = float(entry)

                    row.append(entry)

                data.append(row)

                # If we have labels (training data)
                if len(strings) == self.n_attributes + 1:

                    labels.append(strings[len(strings) - 1])

        return data, labels

    def normal_pdf(self, x, mean, var):

        return math.exp(-((x - mean) ** 2) / (2 * var)) / math.sqrt(var * 2 * math.pi)

    def naive_bayes(self):

        # Training
        yes_attribute_sums = []
        yes_attribute_means = []
        yes_attribute_rss = []
        yes_attribute_vars = []
        n_yes = 0
        no_attribute_sums = []
        no_attribute_means = []
        no_attribute_rss = []
        no_attribute_vars = []
        n_no = 0

        for i in range(self.n_attributes):

            yes_attribute_sums.append(0)
            yes_attribute_means.append(0)
            yes_attribute_rss.append(0)
            yes_attribute_vars.append(0)
            no_attribute_sums.append(0)
            no_attribute_means.append(0)
            no_attribute_rss.append(0)
            no_attribute_vars.append(0)

        # Find mean of all attributes
        for i in range(self.n_training):

            if self.training_labels[i] == "yes":

                n_yes += 1

                for j in range(self.n_attributes):

                    yes_attribute_sums[j] += self.training_data[i][j]

            else:

                n_no += 1

                for j in range(self.n_attributes):

                    no_attribute_sums[j] += self.training_data[i][j]

        for i in range(self.n_attributes):

            yes_attribute_means[i] = yes_attribute_sums[i] / n_yes
            no_attribute_means[i] = no_attribute_sums[i] / n_no

        # Find variance (using n-1 not n)
        for i in range(self.n_training):

            if self.training_labels[i] == "yes":

                for j in range(self.n_attributes):

                    yes_attribute_rss[j] += (
                        self.training_data[i][j] - yes_attribute_means[j]
                    ) ** 2

            else:

                for j in range(self.n_attributes):

                    no_attribute_rss[j] += (
                        self.training_data[i][j] - no_attribute_means[j]
                    ) ** 2

        for i in range(self.n_attributes):

            yes_attribute_vars[i] = yes_attribute_rss[i] / (n_yes - 1)
            no_attribute_vars[i] = no_attribute_rss[i] / (n_no - 1)

        # P(E | yes) * P(yes) > P(E | no) * P(no) ?

        # Testing
        for i in self.testing_data:

            evidence_yes = n_yes / self.n_training
            evidence_no = n_no / self.n_training

            for j in range(self.n_attributes):

                evidence_yes *= self.normal_pdf(
                    i[j], yes_attribute_means[j], yes_attribute_vars[j]
                )
                evidence_no *= self.normal_pdf(
                    i[j], no_attribute_means[j], no_attribute_vars[j]
                )

            if evidence_yes >= evidence_no:

                print("yes")

            else:

                print("no")

        return evidence_yes, evidence_no

    def decision_tree(self):

        # What happens when we get given categories we haven't seen before?
        # i.e. we only see high or low, and we get thrown a medium to test?

        tree = Decision_Tree(self.training_data, self.training_labels)

        tree.print_tree_dfs()

        # test = ["overcast", "hot", "normal", "false"]
        # test = ["rainy", "cool", "normal", "true"]

        # print(tree.predict(test))

        return

    def generate_n_sample_folds(self, n):

        folds = {}

        for i in range(n):

            folds[i] = []

        yes_index = []
        size_yes = 0
        no_index = []
        size_no = 0

        for i in range(self.n_training):

            if self.training_labels[i] == "yes":

                yes_index.append(i)
                size_yes += 1

            else:

                no_index.append(i)
                size_no += 1

        # Split yes classes between n folds
        while size_yes >= n:

            for i in range(n):

                folds[i].append(yes_index[size_yes - 1 - i])

            size_yes -= n

        for i in range(size_yes):

            folds[i].append(yes_index[size_yes - 1 - i])

        # Split no classes between n folds
        while size_no >= n:

            for i in range(n):

                folds[i].append(no_index[size_no - 1 - i])

            size_no -= n

        for i in range(size_no):

            folds[i].append(no_index[size_no - 1 - i])

        return folds

    def write_n_sample_folds(self, filename, folds):

        with open(filename, "w") as file:

            for key in folds:

                file.write(f"fold{key}\n")

                for i in range(len(folds[key])):

                    string = ""

                    for j in range(self.n_attributes):

                        string += f"{self.training_data[folds[key][i]][j]},"

                    string.strip(",")

                    file.write(string + "\n")

                file.write("\n")


# Run with: python3 MyClassifier.py pima.csv pima.csv NB
# Run with: python3 MyClassifier.py pima-indians-diabetes.discrete pima-indians-diabetes.discrete DT

# Reading command line arguments
training_file = sys.argv[1]
testing_file = sys.argv[2]
algorithm = sys.argv[3]

classifier = Classifier(training_file, testing_file, algorithm)

folds = classifier.generate_n_sample_folds(10)
classifier.write_n_sample_folds("pima-folds.csv", folds)
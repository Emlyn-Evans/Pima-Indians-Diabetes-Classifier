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
        self.data_folds = None
        self.label_folds = None
        self.predictions = None

        # Extract the training and testing data
        self.training_data, self.training_labels = self.extract_data(self.training_file)
        self.n_training = len(self.training_data)
        self.testing_data = self.extract_data(self.testing_file)[0]
        self.n_testing = len(self.testing_data)

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

    def confusion_matrix(self, predictions, labels):

        # Generate confusion matrix for accuracy, sensitivity, specificity
        n = len(predictions)
        tp = 0
        tn = 0
        fp = 0
        fn = 0

        for i in range(n):

            if predictions[i] == "yes":

                if labels[i] == "yes":

                    tp += 1

                else:

                    fp += 1

            else:

                if labels[i] == "yes":

                    fn += 1

                else:

                    tn += 1

        matrix = [tp, fp, fn, tn]

        return matrix

    def cross_validation(self):

        n_folds = 10
        self.generate_n_sample_folds(n_folds)

        accuracy_sum = 0

        # Iteratively set the training and testing data to include all but 1
        # fold
        for i in range(n_folds):

            training_data = []
            training_labels = []
            testing_data = self.data_folds[i]
            testing_labels = self.label_folds[i]

            for j in range(n_folds):

                if j != i:

                    training_data += self.data_folds[j]
                    training_labels += self.label_folds[j]

            if self.algorithm == "NB":

                predictions = self.naive_bayes(
                    training_data, training_labels, testing_data
                )

            else:

                predictions = self.decision_tree(
                    training_data, training_labels, testing_data
                )

            matrix = self.confusion_matrix(predictions, testing_labels)
            accuracy = (matrix[0] + matrix[3]) / len(predictions)
            accuracy_sum += accuracy

            # print(f"Fold: {i}: Acc: {accuracy}")

        self.accuracy = accuracy_sum / n_folds

        # print(f"Total Accuracy: {self.accuracy}")

        return

    def naive_bayes(self, training_data, training_labels, testing_data):

        # Training lists for Bayes' Theorem computation
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

        n_training = len(training_data)

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
        for i in range(n_training):

            if training_labels[i] == "yes":

                n_yes += 1

                for j in range(self.n_attributes):

                    yes_attribute_sums[j] += training_data[i][j]

            else:

                n_no += 1

                for j in range(self.n_attributes):

                    no_attribute_sums[j] += training_data[i][j]

        for i in range(self.n_attributes):

            yes_attribute_means[i] = yes_attribute_sums[i] / n_yes
            no_attribute_means[i] = no_attribute_sums[i] / n_no

        # Find variance (using n-1 not n)
        for i in range(n_training):

            if training_labels[i] == "yes":

                for j in range(self.n_attributes):

                    yes_attribute_rss[j] += (
                        training_data[i][j] - yes_attribute_means[j]
                    ) ** 2

            else:

                for j in range(self.n_attributes):

                    no_attribute_rss[j] += (
                        training_data[i][j] - no_attribute_means[j]
                    ) ** 2

        for i in range(self.n_attributes):

            yes_attribute_vars[i] = yes_attribute_rss[i] / (n_yes - 1)
            no_attribute_vars[i] = no_attribute_rss[i] / (n_no - 1)

        # Testing
        prediction = []

        for i in testing_data:

            evidence_yes = n_yes / n_training
            evidence_no = n_no / n_training

            # Plug values into normal pdf and sum evidence
            for j in range(self.n_attributes):

                evidence_yes *= self.normal_pdf(
                    i[j], yes_attribute_means[j], yes_attribute_vars[j]
                )
                evidence_no *= self.normal_pdf(
                    i[j], no_attribute_means[j], no_attribute_vars[j]
                )

            # If P(E | yes) * P(yes) > P(E | no) * P(no), we take yes
            if evidence_yes >= evidence_no:

                prediction.append("yes")

            else:

                prediction.append("no")

        return prediction

    def decision_tree(self, training_data, training_labels, testing_data):

        # Create and build the decision tree
        tree = Decision_Tree(training_data, training_labels)

        # tree.print_tree_dfs()

        # Test for when we encounter a new category not seen before in testing
        # test = ["low", "high", "high", "high", "high", "high", "high", "potato"]
        # print(f"YEET: {tree.predict(test)}")

        predictions = []

        for i in range(len(testing_data)):

            predictions.append(tree.predict(testing_data[i]))

        return predictions

    def predict_testing(self):

        if self.algorithm == "NB":

            self.predictions = self.naive_bayes(
                self.training_data, self.training_labels, self.testing_data
            )

        else:

            self.predictions = self.decision_tree(
                self.training_data, self.training_labels, self.testing_data
            )

        return

    def print_predictions(self, predictions=None):

        if predictions is None:

            predictions = self.predictions

        for i in predictions:

            print(i)

    def generate_n_sample_folds(self, n):

        # Generate n sample folds for cross validation
        self.data_folds = {}
        self.label_folds = {}

        for i in range(n):

            self.data_folds[i] = []
            self.label_folds[i] = []

        yes_data = []
        size_yes = 0
        no_data = []
        size_no = 0

        # Count number of yes and no data lines for stratification
        for i in range(self.n_training):

            if self.training_labels[i] == "yes":

                yes_data.append(self.training_data[i])
                size_yes += 1

            else:

                no_data.append(self.training_data[i])
                size_no += 1

        # Split yes classes between n folds
        while size_yes >= n:

            for i in range(n):

                self.data_folds[i].append(yes_data[size_yes - 1 - i])
                self.label_folds[i].append("yes")

            size_yes -= n

        for i in range(size_yes):

            self.data_folds[i].append(yes_data[size_yes - 1 - i])
            self.label_folds[i].append("yes")

        # Split no classes between n folds
        while size_no >= n:

            for i in range(n):

                self.data_folds[i].append(no_data[size_no - 1 - i])
                self.label_folds[i].append("no")

            size_no -= n

        for i in range(size_no):

            self.data_folds[i].append(no_data[size_no - 1 - i])
            self.label_folds[i].append("no")

        return

    def write_n_sample_folds(self, filename):

        # Write sample folds to output file
        with open(filename, "w") as file:

            for key in self.data_folds:

                file.write(f"fold{key + 1}\n")

                for i in range(len(self.data_folds[key])):

                    string = ""

                    for j in range(self.n_attributes):

                        string += f"{self.data_folds[key][i][j]},"

                    string += f"{self.label_folds[key][i]}"

                    file.write(string + "\n")

                file.write("\n")


# Reading command line arguments
training_file = sys.argv[1]
testing_file = sys.argv[2]
algorithm = sys.argv[3]

classifier = Classifier(training_file, testing_file, algorithm)

# For cross validation, uncomment lines below:
# classifier.cross_validation()
# print(classifier.accuracy)

# For Naive Bayes, run with: python3 MyClassifier.py pima.csv pima.csv NB
# Accuracy
# - Full dataset: 0.7526041666666666
# - 10 folds CV: 0.7460526315789474
# For Decision Tree, run with: python3 MyClassifier.py pima-indians-diabetes.discrete pima-indians-diabetes.discrete DT
# Accuracy
# - Full dataset: 0.8190104166666666
# - 10 folds CV: 0.7409090909090909

# For normal functionality, uncomment lines below:
classifier.predict_testing()
classifier.print_predictions()

# For output on full dataset:
# matrix = classifier.confusion_matrix(classifier.predictions, classifier.training_labels)
# print((matrix[0] + matrix[3]) / (matrix[0] + matrix[1] + matrix[2] + matrix[3]))

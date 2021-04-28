import math


class Node:
    def __init__(
        self, data, labels, n_attributes, n_yes, n_no, parent, depth, category
    ):

        self.data = data
        self.labels = labels
        self.n = len(data)
        self.n_attributes = n_attributes
        self.n_yes = n_yes
        self.n_no = n_no
        self.information_counts = {}
        self.information = self.compute_information(self.n_yes, self.n_no, self.n)
        self.rule = None
        self.predict = None
        self.parent = parent
        self.children = {}
        self.depth = depth
        self.category = category

        return

    def compute_information(self, n_yes, n_no, n_total):

        if n_yes == 0:

            n_yes = n_total

        if n_no == 0:

            n_no = n_total

        return -((n_yes / n_total) * math.log2(n_yes / n_total)) - (
            (n_no / n_total) * math.log2(n_no / n_total)
        )

    def compute_best_attribute(self):

        for i in range(self.n_attributes):

            self.information_counts[i] = {}

        for i in range(self.n):

            for j in range(self.n_attributes):

                # Index 0 is yes and index 1 is no
                if self.data[i][j] not in self.information_counts[j]:

                    self.information_counts[j][self.data[i][j]] = [0, 0]

                if self.labels[i] == "yes":

                    self.information_counts[j][self.data[i][j]][0] += 1

                else:

                    self.information_counts[j][self.data[i][j]][1] += 1

        # Information gain for each attribute
        best_gain = None

        for i in range(self.n_attributes):

            attribute_information = 0

            for key in self.information_counts[i]:

                weight = (
                    self.information_counts[i][key][0]
                    + self.information_counts[i][key][1]
                ) / self.n

                attribute_information = weight * self.compute_information(
                    self.information_counts[i][key][0],
                    self.information_counts[i][key][1],
                    self.n,
                )

            # If this is 0, then we are at a leaf and everything is sorted
            if attribute_information > 0:

                # If this is 0, then splitting off this attribute is redundant
                if self.information - attribute_information > 0:

                    if best_gain is None:

                        best_gain = self.information - attribute_information
                        self.rule = i

                    if self.information - attribute_information > best_gain:

                        self.rule = i

        return


class Decision_Tree:
    def __init__(self, data, labels):

        n_yes = 0
        n_no = 0

        for i in range(len(labels)):

            if labels[i] == "yes":

                n_yes += 1

            else:

                n_no += 1

        self.root = Node(data, labels, len(data[0]), n_yes, n_no, None, 0, None)

        self.compute_tree_recursion(self.root)

        return

    def compute_tree_recursion(self, node):

        node.compute_best_attribute()

        if node.rule is None:

            # We reach the stopping condition
            if node.n_yes >= node.n_no:

                node.predict = "yes"

            else:

                node.predict = "no"

            return

        data_split = {}
        labels_split = {}

        for key in node.information_counts[node.rule]:

            data_split[key] = []
            labels_split[key] = []

        for i in range(node.n):

            data_split[node.data[i][node.rule]].append(node.data[i])
            labels_split[node.data[i][node.rule]].append(node.labels[i])

        for key in data_split:

            child = Node(
                data_split[key],
                labels_split[key],
                node.n_attributes,
                node.information_counts[node.rule][key][0],
                node.information_counts[node.rule][key][1],
                node,
                node.depth + 1,
                key,
            )

            node.children[key] = child
            self.compute_tree_recursion(child)

        return

    def predict(self, test):

        node = self.root

        while node.predict is None:

            node = node.children[test[node.rule]]

        return node.predict

"""Decision Tree"""

import math


class Node:
    def __init__(
        self,
        depth,
        data,
        labels,
        n_attributes,
        n_yes,
        n_no,
        rule_string,
    ):

        self.depth = depth
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
        self.rule_string = rule_string
        self.children = {}

        return

    def compute_information(self, n_yes, n_no, n_total):

        # If we get 0 counts, log will throw and error
        if n_yes == 0:

            n_yes = n_total

        if n_no == 0:

            n_no = n_total

        # Formula for two classes
        information = -((n_yes / n_total) * math.log2(n_yes / n_total)) - (
            (n_no / n_total) * math.log2(n_no / n_total)
        )

        return information

    def compute_best_attribute(self):

        # We create a dictionary for each attribute, then dictionaries for each
        # category in each attribute with counts for classes.
        for i in range(self.n_attributes):

            self.information_counts[i] = {}

        for i in range(self.n):

            for j in range(self.n_attributes):

                if self.data[i][j] not in self.information_counts[j]:

                    # Index 0 is yes and index 1 is no
                    self.information_counts[j][self.data[i][j]] = [0, 0]

                if self.labels[i] == "yes":

                    self.information_counts[j][self.data[i][j]][0] += 1

                else:

                    self.information_counts[j][self.data[i][j]][1] += 1

        # Compute information gain for each attribute and select the best
        best_gain = None

        for i in range(self.n_attributes):

            attribute_information = 0
            split_information = 0

            for key in self.information_counts[i]:

                size_of_branch = (
                    self.information_counts[i][key][0]
                    + self.information_counts[i][key][1]
                )

                weight = size_of_branch / self.n

                attribute_information += weight * self.compute_information(
                    self.information_counts[i][key][0],
                    self.information_counts[i][key][1],
                    size_of_branch,
                )

                split_information += -(
                    (size_of_branch / self.n) * math.log2((size_of_branch / self.n))
                )

            # If the gain is 0, then splitting off this attribute is redundant
            gain = self.information - attribute_information

            if gain > 0:

                if split_information > 0:

                    gain_ratio = gain / split_information

                    # print(
                    #     f"Attribute: {i}: Total_Info: {self.information}: Att_Info: {attribute_information}: Gain: {self.information - attribute_information}: Gain ratio: {gain_ratio}"
                    # )

                    if best_gain is None:

                        best_gain = gain_ratio
                        self.rule = i

                    if gain_ratio > best_gain:

                        self.rule = i
                        best_gain = gain_ratio

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

        self.root = Node(1, data, labels, len(data[0]), n_yes, n_no, "")

        self.compute_tree_recursion(self.root)

    def compute_tree_recursion(self, node):

        # Compute the best attribute to split off at each node
        node.compute_best_attribute()

        # Stopping condition: no attributes gives information gain
        if node.rule is None:

            # We take the majority guess
            if node.n_yes >= node.n_no:

                node.predict = "yes"

            else:

                node.predict = "no"

            node.rule_string += f": {node.predict}"

            return

        # Update rule string for identification
        if node.rule_string == "":

            node.rule_string += f"{node.rule} = "

        else:

            node.rule_string += f", {node.rule} = "

        # Split the data into categories for children
        data_split = {}
        labels_split = {}

        for key in node.information_counts[node.rule]:

            data_split[key] = []
            labels_split[key] = []

        for i in range(node.n):

            data_split[node.data[i][node.rule]].append(node.data[i])
            labels_split[node.data[i][node.rule]].append(node.labels[i])

        # Create child and recurse
        for key in data_split:

            child = Node(
                node.depth + 1,
                data_split[key],
                labels_split[key],
                node.n_attributes,
                node.information_counts[node.rule][key][0],
                node.information_counts[node.rule][key][1],
                node.rule_string + f"{key}",
            )

            node.children[key] = child

            if child.n > 0:

                self.compute_tree_recursion(child)

            else:

                # Stopping condition: if child is empty
                if node.n_yes >= node.n_no:

                    child.predict = "yes"

                else:

                    child.predict = "no"

                child.rule_string += f": {child.predict}"

        return

    def predict(self, test, node=None):

        # Search down height of tree to find prediction
        if node is None:

            node = self.root

        while node.predict is None:

            if test[node.rule] in node.children:

                node = node.children[test[node.rule]]

            else:

                # When we encounter a new category not seen before
                weighted_sum = 0

                for i in node.children:

                    prediction = self.predict(test, node.children[i])

                    if prediction == "yes":

                        weighted_sum += node.children[i].n

                    else:

                        weighted_sum -= node.children[i].n

                # Use this for majority node implementation
                # weighted_sum = node.n_yes - node.n_no

                if weighted_sum >= 0:

                    return "yes"

                else:

                    return "no"

        return node.predict

    def print_tree_dfs(self, node=None):

        if node is None:

            node = self.root

        print(f"{'-' * node.depth} {node.rule_string}")

        for i in node.children:

            self.print_tree_dfs(node.children[i])
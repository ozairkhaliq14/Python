import pandas as pd
import scipy.stats
import math
import copy
import csv


colTitles = ['Alternate', 'Bar', 'Weekend', 'Hungry','Patrons','Price','Raining','Reservations','Type','WaitEstimate','Result']
allExamples={}
alpha = 0.05

class TreeNode():
    def __init__(self, depth):
        self.value = None
        self.branch = None
        self.children = None
        self.depth = depth
    
def build_decision_tree(examples, attributes, parent_examples, depth):
    if examples.empty:
        return pluralityValue(parent_examples)
    elif sameClassification(examples):
        return examples['Result'].iloc[0]
    elif not attributes:
        return pluralityValue(examples)
    else:
        attribute_importance = {a: calculateImportance(a, examples) for a in attributes}
        best_attribute = max(attribute_importance, key=attribute_importance.get)

        tree_node = TreeNode(depth)
        tree_node.children = []
        tree_node.value = best_attribute

        remaining_attributes = attributes.copy()
        remaining_attributes.remove(best_attribute)

        for unique_value in allExamples[best_attribute].unique():
            filtered_examples = examples[examples[best_attribute] == unique_value]
            filtered_examples.reset_index(drop=True, inplace=True)

            subtree = build_decision_tree(filtered_examples, remaining_attributes, examples, depth + 1)
            if isinstance(subtree, TreeNode):
                subtree.branch = unique_value
                tree_node.children.append(subtree)
            else:
                leaf_node = TreeNode(depth + 1)
                leaf_node.value = subtree
                leaf_node.branch = unique_value
                tree_node.children.append(leaf_node)

        return tree_node
    
def calculateImportance(attribute, examples):
    grouped_results = examples.groupby(['Result'], sort=False).size().reset_index(name='Count')
    positive_count = find_count('Yes', grouped_results)
    negative_count = find_count('No', grouped_results)

    return entropy(positive_count / (positive_count + negative_count)) - remainder(attribute, examples)

def find_count(value, data):
    index = 0 if data['Result'].iloc[0] == value else 1
    return data['Count'][index]

def pluralityValue(examples):
    grouped_results = examples.groupby(['Result'], sort=False).size().reset_index(name='Count')
    max_idx = 0

    for i in range(len(grouped_results) - 1):
        max_idx = i + 1 if grouped_results['Count'][i] < grouped_results['Count'][i + 1] else i

    return grouped_results['Result'][max_idx]

def entropy(q):
    if q != 0 and 1 - q != 0:
        return -1 * (q * math.log2(q) + (1 - q) * math.log2(1 - q))
    elif q != 0 and 1 - q == 0:
        return -1 * (q * math.log2(q))
    else:
        return -1 * (1 - q) * math.log2(1 - q)

def remainder(attribute, examples):
    example_length = len(examples)
    attribute_counts = examples.groupby([attribute], sort=True).size().reset_index(name='count')

    positive_examples = examples[examples['Result'] == 'Yes']
    positive_counts = positive_examples.groupby([attribute], sort=True).size().reset_index(name='pos')

    negative_examples = examples[examples['Result'] == 'No']
    negative_counts = negative_examples.groupby([attribute], sort=True).size().reset_index(name='neg')

    merged_counts = pd.merge(positive_counts, negative_counts, how='outer', left_on=attribute, right_on=attribute)
    merged_counts.fillna(0, inplace=True)

    total = 0
    for _, row in merged_counts.iterrows():
        combined_count = row['pos'] + row['neg']
        total += (combined_count / example_length) * entropy(row['pos'] / combined_count)

    return total


def sameClassification(examples):
    first_result = examples['Result'].iloc[0]
    all_same = all(examples['Result'][i] == first_result for i in range(len(examples)))

    return all_same

def statisticalSignificanceTest(node, examples):
    if node.children is not None:
        num_children = len(node.children)
        pos_count = len(examples[examples['Result'] == 'Yes'])
        neg_count = len(examples[examples['Result'] == 'No'])
        chi_square_stat = 0

        for child in node.children:
            filtered_examples = examples[examples[node.value] == child.branch]
            if len(filtered_examples) != 0:
                pos_child_count = len(filtered_examples[filtered_examples['Result'] == 'Yes'])
                neg_child_count = len(filtered_examples[filtered_examples['Result'] == 'No'])
                expected_pos_child_count = pos_count * (pos_child_count + neg_child_count) / (pos_count + neg_count)
                expected_neg_child_count = neg_count * (pos_child_count + neg_child_count) / (pos_count + neg_count)
                chi_square_stat += (pos_child_count - expected_pos_child_count)**2 / expected_pos_child_count + \
                                   (neg_child_count - expected_neg_child_count)**2 / expected_neg_child_count
            else:
                chi_square_stat += 0

        critical_value = scipy.stats.chi2.ppf(1 - alpha, num_children - 1)

        if chi_square_stat > critical_value:
            for child in node.children:
                statisticalSignificanceTest(child, examples[examples[node.value] == child.branch])
        else:
            node.children = None
            node.value = 'Yes' if pos_count > neg_count else 'No'
    else:
        return

def display_tree(start_depth, tree, indent_width=4):
    def traverse_tree(tree, indent=""):
        if tree.children is None:
            print(indent + f"[{tree.branch}]" + "─" * indent_width + f"{tree.value}")
        else:
            print(indent + f"[{tree.branch}]" + "─" * indent_width + f"{tree.value}")

            for child in tree.children:
                traverse_tree(child, indent + " " * 10)

    tree.branch = "ROOT"
    traverse_tree(tree)


def main():
    global allExamples
    dataset = pd.read_csv('restaurant.csv', names=colTitles, skipinitialspace=True)
    allExamples = dataset
    colTitles.remove('Result')
    decision_tree = build_decision_tree(dataset, colTitles, dataset, 0)

    print("------------ Decision Tree ------------")
    display_tree(0, decision_tree)

    print("\n\n------------ Pruned Decision Tree ------------")
    statisticalSignificanceTest(decision_tree, dataset)
    display_tree(0, decision_tree)

if __name__ == "__main__":
    main()

# IAMCERINI

# Import the modules
import fileinput
import itertools
import re
import time

# countCrosses counts the number of edge crosses between two layers using a matrix
def countCrosses(Matrix, L1_index, L1_width, L2_width):
    crosses_count = 0
    for L1_node in range(0, L1_index):
        for L2_node in range(0, L2_width):  # print("Edge 1: %i %i" % (L1_node, L2_node))
            if Matrix[L1_node][L2_node] != 0:  # print("Edge 1 Found")
                for L1_node_compare in range(0, L1_width):
                    for L2_node_compare in range(0, L2_width):
                        if Matrix[L1_node_compare][
                            L2_node_compare] != 0:  # print("Edge 2 Found: %i %i" % (L1_node_compare, L2_node_compare))
                            if ((L2_node > L2_node_compare) and (
                                L1_node < L1_node_compare)):  # print("Edge Cross between [%i][%i] and [%i][%i]" % (
                                crosses_count += 1  # print("Crosses Count: %i" % (crosses_count))
    return crosses_count

# getCrossCount fills in the edge matrix with the edges between two nodes of two different layers. 1 indicates that there is an edge and then performs the cross count
def getCrossCount(list_of_edges, layer_a, layer_b):
    matrix = [[0 for x in range(len(layer_a))] for y in range(len(layer_b))]
    for edge in list_of_edges:
        if edge[0] in layer_a:
            matrix[layer_a.index(edge[0])][layer_b.index(edge[1])] = 1
    cross_count = countCrosses(matrix, len(layer_a) - 1, len(layer_a), len(layer_b))
    return cross_count

# generatePermutations generates all permutations for all nodes of each layer
def generatePermutations(list_of_layers, number_of_layers):
    list_of_permutations = [{} for x in range(number_of_layers)]  # Create the list of layer permutations
    for i in range(len(list_of_layers)):
        node_permutations = []  # Reset the layer node permutation list
        for node_list in itertools.permutations(list_of_layers[i]):
            node_permutations.append(node_list)  # For each permutation in the layer, add it to the node list
        list_of_permutations[
            i] = node_permutations  # Add the list of all node permutations for a given layer to the full list of permutations
    return list_of_permutations

# parseInputFile parses all the information in the input file
def parseInputFile():
    list_of_layers = []
    list_of_edges = []
    number_of_layers = 0
    index = 0
    for line in fileinput.input():
        new_command = ''
        if (re.findall('in_layer', line)):
            new_command = line.replace('in_layer(', '')
            new_command = new_command.replace(').', '')
            new_command = new_command.strip().split(",")
            list_of_layers[int(new_command[0]) - 1].append(
                new_command[1])  # Insert the node in the node list of the current layer
            index = index + 1
        elif (re.findall('edge', line)):
            new_command = line.replace('edge(', '')
            new_command = new_command.replace(').', '')
            new_command = new_command.strip().split(",")
            list_of_edges.append([new_command[0], new_command[1]])
        elif (re.findall('width', line)):
            list_of_nodes = []  # Create the list of nodes of size width for the new layer
            list_of_layers.append(list_of_nodes)  # Add the list of nodes to the list of layers
            index = 0
        elif (re.findall('layers', line)):
            new_command = line.replace('layers(', '')
            new_command = new_command.replace(').', '')
            number_of_layers = int(new_command)
    fileinput.close()  # Close the file
    return list_of_layers, list_of_edges, number_of_layers

def main():
    list_of_layers, list_of_edges, number_of_layers = parseInputFile()  # Parse the input from file
    total_cross_count = 0
    for i in range(number_of_layers - 1):
        total_cross_count = total_cross_count + getCrossCount(list_of_edges, list_of_layers[i], list_of_layers[i + 1]) # Get cross count of initial input permutation
    if total_cross_count != 0: # Optimisation: Check if the initial input permutation is already optimised
        list_of_permutations = generatePermutations(list_of_layers, number_of_layers)  # Generate the permutations
        for p in itertools.product(*list_of_permutations):  # Run through the permutations
            count = 0  # Reset the cross count when running permutations
            for i in range(number_of_layers - 1):
                count = count + getCrossCount(list_of_edges, p[i], p[i + 1]) # Get the count between two layers and add it to the running count
                if count > total_cross_count:
                    break # Optimisation: Stop remaining counts for current permutation if count already exceeds the total count
            if count < total_cross_count:
                total_cross_count = count # Update the lowest recorded cross count if new count is less
            if total_cross_count == 0:
                break # Optimisation: If the total cross count is 0, then do not check any more permutations
    print("Optimization: %i" % (total_cross_count)) # Print optimised cross count

if __name__ == "__main__":
    main()
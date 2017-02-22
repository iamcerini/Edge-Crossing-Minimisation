# Andrea Cerini
# 109226255
# CSE 307 HW 2
# DUE FEB 21 2017
# Algorithm based on "An Edge Crossing Minimization Algorithm Based
# on Adjacency Matrix Transformation" by Y Zhang

# Import the modules
import fileinput
import itertools
import re
import time

def countCrosses(Matrix, L1_index, L1_width, L2_width):
    crosses_count = 0
    for L1_node in range(0, L1_index):
        for L2_node in range(0, L2_width):
            #print("Edge 1: %i %i" % (L1_node, L2_node))
            if Matrix[L1_node][L2_node] != 0:
                #print("Edge 1 Found")
                for L1_node_compare in range(0, L1_width):
                    for L2_node_compare in range(0, L2_width):
                        if Matrix[L1_node_compare][L2_node_compare] != 0:
                            #print("Edge 2 Found: %i %i" % (L1_node_compare, L2_node_compare))
                            if ((L2_node > L2_node_compare) and (L1_node < L1_node_compare)):
                                #print("Edge Cross between [%i][%i] and [%i][%i]" % (
                                #L1_node, L2_node, L1_node_compare, L2_node_compare))
                                crosses_count += 1
           # else:
                #print("No Edges")
            #print("\n")
    #print("Crosses Count: %i" % (crosses_count))
    return crosses_count
   # return

def print_mat(m):
   for row in m:
    print(row)

def main():
    print("\n")
    no_layers = 0
    current_layer_width = 0
    current_layer = 0
    list_of_layers = []
    list_of_nodes = []
    list_of_edges = []
    index = 0

    # PARSE THE INPUTS FROM THE FILES
    for line in fileinput.input():
        #print(line)
        new_command = ''
        if (re.findall('in_layer', line)):
            #print("IN LAYER")
            new_command = line.replace('in_layer(', '')
            new_command = new_command.replace(').', '')
            new_command = new_command.strip().split(",")
            #current_layer = new_command[0]
            #node_name = new_command[1]
            list_of_layers[int(new_command[0])-1].append(new_command[1]) # Insert the node in the node list of the current layer
            index = index + 1
        elif(re.findall('edge', line)):
           # print("EDGE")
            new_command = line.replace('edge(', '')
            new_command = new_command.replace(').', '')
            new_command = new_command.strip().split(",")
            list_of_edges.append([new_command[0], new_command[1]])
        elif (re.findall('width', line)):
           # print("WIDTH")
            new_command = line.replace('width(', '')
            new_command = new_command.replace(').', '')
            new_command = new_command.strip().split(",")
            current_layer = int(new_command[0])
            current_layer_width = int(new_command[1])-1
           # print("Width of Layer %i: %i" % (current_layer, current_layer_width))
            list_of_nodes = [] # Create the list of nodes of size width for the new layer
            list_of_layers.append(list_of_nodes) # Add the list of nodes to the list of layers
            index = 0
        elif (re.findall('layers', line)):
            new_command = line.replace('layers(', '')
            new_command = new_command.replace(').', '')
            no_layers = int(new_command)
           # print("Number of Layers: %i" % no_layers)
    fileinput.close()
    # END PARSING INPUTS


    # CREATE INITIAL EDGE MATRICES
    count = 0
    count_1 = 0
    count_2 = 0

    # CREATE INITIAL L1 and L2 MATRIX
    edge_matrix_1 = [[0 for x in range(len(list_of_layers[0]))] for y in range(len(list_of_layers[1]))]
    for edge in list_of_edges:
        if edge[0] in list_of_layers[0]:
            edge_matrix_1[list_of_layers[0].index(edge[0])][list_of_layers[1].index(edge[1])] = 1
    print("MATRIX 1")
    print_mat(edge_matrix_1)
    print("\n")
    count_1 = countCrosses(edge_matrix_1, len(list_of_layers[0])-1, len(list_of_layers[0]), len(list_of_layers[1]))

    # CREATE INITIAL L2 and L3 MATRIX
    edge_matrix_2 = [[0 for x in range(len(list_of_layers[1]))] for y in range(len(list_of_layers[2]))]
    for edge in list_of_edges:
        if edge[0] in list_of_layers[1]:
            edge_matrix_2[list_of_layers[1].index(edge[0])][list_of_layers[2].index(edge[1])] = 1
    print("\nMATRIX 2")
    print_mat(edge_matrix_2)
    print("\n")
    count_2 = countCrosses(edge_matrix_2, len(list_of_layers[1])-1, len(list_of_layers[1]), len(list_of_layers[2]))


    total_cross_count = count_1 + count_2 # The cross count for the end
    print("\nINITIAL COUNT: %i" % (total_cross_count))

    start_time = time.time()
    # RUN THE PERMUTATIONS
    count = 0 # The cross count when running permutations
    for p1 in itertools.permutations(list_of_layers[0]):
        #print(p1)
        for p2 in itertools.permutations(list_of_layers[1]):
            #print(p2)
            L1_L2_edge_matrix = [[0 for x in range(len(list_of_layers[0]))] for y in range(len(list_of_layers[1]))] # Clear the matrix
            for edge in list_of_edges:
                if edge[0] in p1:
                    L1_L2_edge_matrix[p1.index(edge[0])][p2.index(edge[1])] = 1
            L1_L2_cross_count = countCrosses(L1_L2_edge_matrix, len(list_of_layers[0])-1, len(list_of_layers[0]), len(list_of_layers[1]))
            for p3 in itertools.permutations(list_of_layers[2]):
                L2_L3_edge_matrix = [[0 for x in range(len(list_of_layers[1]))] for y in
                                     range(len(list_of_layers[2]))]  # Clear the matrix
                for edge in list_of_edges:
                    if edge[0] in p2:
                        L2_L3_edge_matrix[p2.index(edge[0])][p3.index(edge[1])] = 1
                L2_L3_cross_count = countCrosses(L2_L3_edge_matrix, len(list_of_layers[1]) - 1, len(list_of_layers[1]),
                                                 len(list_of_layers[2]))

                count = L1_L2_cross_count + L2_L3_cross_count
                if count < total_cross_count:
                    total_cross_count = count
                    edge_matrix_1 = L1_L2_edge_matrix[:]
                    edge_matrix_2 = L2_L3_edge_matrix[:]
                    new_node_list_1 = p1
                    new_node_list_2 = p2
                    new_node_list_3 = p3


    print("\n\n----- RESULTS -----\n")
    print("\n --- %s seconds --- \n" % (time.time() - start_time))
    list_of_layers[0] = new_node_list_1
    list_of_layers[1] = new_node_list_2
    list_of_layers[2] = new_node_list_3
    print("\nLAYER NODE ORDERING\n")
    print(list_of_layers[0])
    print(list_of_layers[1])
    print(list_of_layers[2])
    print("\nCROSS MINIMISATION COUNT\n")
    print(total_cross_count)
    print("\nMATRIX 1\n")
    print_mat(edge_matrix_1)
    print("\nMATRIX 2\n")
    print_mat(edge_matrix_2)


    # print("COMPARING LAYER 2 AND LAYER 3")
    # edge_matrix_1 = [[0 for x in range(len(list_of_layers[1]))] for y in range(len(list_of_layers[2]))]
    # for edge in list_of_edges:
    #     # Edge in list of edges [n3, n14]
    #     if edge[0] in list_of_layers[1]:
    #         edge_matrix_1[list_of_layers[1].index(edge[0])][list_of_layers[2].index(edge[1])] = 1
    #
    #
    # count = countCrosses(edge_matrix_1, len(list_of_layers[1])-1, len(list_of_layers[1]), len(list_of_layers[2]))
    # print_mat(edge_matrix_1)
    #
    # for p3 in itertools.permutations(list_of_layers[2]):
    #     # print(p2)
    #     L1_L2_edge_matrix = [[0 for x in range(len(list_of_layers[1]))] for y in
    #                        range(len(list_of_layers[2]))]  # Clear the matrix
    #     for edge in list_of_edges:
    #         if edge[0] in list_of_layers[1]:
    #             L1_L2_edge_matrix[list_of_layers[1].index(edge[0])][p3.index(edge[1])] = 1
    #     new_cross_count = countCrosses(L1_L2_edge_matrix, len(list_of_layers[1]) - 1, len(list_of_layers[1]),
    #                                    len(list_of_layers[2]))
    #     if new_cross_count < count:
    #         count = new_cross_count
    #         edge_matrix_1 = L1_L2_edge_matrix[:]
    #         new_node_list_3 = p3
    #     if count == 0:
    #         break
    #
    # total_cross_count = total_cross_count + count
    # list_of_layers[2] = new_node_list_3
    # print(list_of_layers[2])
    # print(count)
    #
    # print("\nFINAL RESULTS:")
    # print("Total Cross Count: %i" % total_cross_count)
    # print_mat(edge_matrix_1)
    #
    #
    # for results in list_of_layers:
    #     print(results)


    # For each permutations of L1
    # For each permutation of L2
        # Populate new matrix
        # Check the cross count
        # Save matrix if cross count less than initial
        # Update cross count to new lower cross count
        # ? If cross count = 0, go to next layer


if __name__ == "__main__":
    main()
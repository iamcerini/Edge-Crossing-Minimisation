# Andrea Cerini
# 109226255
# CSE 307 HW 2
# DUE FEB 21 2017
# Algorithm based on "An Edge Crossing Minimization Algorithm Based
# on Adjacency Matrix Transformation" by Y Zhang

# Import the modules
import sys
import fileinput
import numpy
import itertools
import re

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
    total_cross_count = 0
    # list_of_layers[0] = list_of_nodes , list of nodes for layer 1
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

    print("\n")
    edge_matrix = [[0 for x in range(len(list_of_layers[0]))] for y in range(len(list_of_layers[1]))]
    for edge in list_of_edges:
        # Edge in list of edges [n3, n14]
        if edge[0] in list_of_layers[0]:
            edge_matrix[list_of_layers[0].index(edge[0])][list_of_layers[1].index(edge[1])] = 1
    print_mat(edge_matrix)
    print("\n")


    count = countCrosses(edge_matrix, len(list_of_layers[0])-1, len(list_of_layers[0]), len(list_of_layers[1]))
    print(count)
    print("\n")



    for p1 in itertools.permutations(list_of_layers[0]):
        #print(p1)
        for p2 in itertools.permutations(list_of_layers[1]):
            #print(p2)
            new_edge_matrix = [[0 for x in range(len(list_of_layers[0]))] for y in range(len(list_of_layers[1]))] # Clear the matrix
            for edge in list_of_edges:
                if edge[0] in p1:
                    new_edge_matrix[p1.index(edge[0])][p2.index(edge[1])] = 1
            new_cross_count = countCrosses(new_edge_matrix, len(list_of_layers[0])-1, len(list_of_layers[0]), len(list_of_layers[1]))
            if new_cross_count < count:
                count = new_cross_count
                edge_matrix = new_edge_matrix[:]
                new_node_list_1 = p1
                new_node_list_2 = p2
        #     if count == 0:
        #         break
        # if count == 0:
        #     break
            #print_mat(edge_matrix)

    list_of_layers[0] = new_node_list_1
    list_of_layers[1] = new_node_list_2
    print(list_of_layers[0])
    print(list_of_layers[1])
    print(count)
    print_mat(edge_matrix)

    new_node_list_3 = 0;

    print(count)
    print("\n")
    total_cross_count = count
    count = 0


    print("COMPARING LAYER 2 AND LAYER 3")
    edge_matrix = [[0 for x in range(len(list_of_layers[1]))] for y in range(len(list_of_layers[2]))]
    for edge in list_of_edges:
        # Edge in list of edges [n3, n14]
        if edge[0] in list_of_layers[1]:
            edge_matrix[list_of_layers[1].index(edge[0])][list_of_layers[2].index(edge[1])] = 1


    count = countCrosses(edge_matrix, len(list_of_layers[1])-1, len(list_of_layers[1]), len(list_of_layers[2]))
    print_mat(edge_matrix)

    for p3 in itertools.permutations(list_of_layers[2]):
        # print(p2)
        new_edge_matrix = [[0 for x in range(len(list_of_layers[1]))] for y in
                           range(len(list_of_layers[2]))]  # Clear the matrix
        for edge in list_of_edges:
            if edge[0] in list_of_layers[1]:
                new_edge_matrix[list_of_layers[1].index(edge[0])][p3.index(edge[1])] = 1
        new_cross_count = countCrosses(new_edge_matrix, len(list_of_layers[1]) - 1, len(list_of_layers[1]),
                                       len(list_of_layers[2]))
        if new_cross_count < count:
            count = new_cross_count
            edge_matrix = new_edge_matrix[:]
            new_node_list_3 = p3
        if count == 0:
            break

    total_cross_count = total_cross_count + count
    list_of_layers[2] = new_node_list_3
    print(list_of_layers[2])
    print(count)

    print("\nFINAL RESULTS:")
    print("Total Cross Count: %i" % total_cross_count)
    print_mat(edge_matrix)


    for results in list_of_layers:
        print(results)


        # For each permutations of L1
        # For each permutation of L2
            # Populate new matrix
            # Check the cross count
            # Save matrix if cross count less than initial
            # Update cross count to new lower cross count
            # ? If cross count = 0, go to next layer



    # layers = 3
   #  L1_width, L2_width = 3, 3
   #  Matrix = [[0 for x in range(L1_width)] for y in range(L2_width)]
   #  Matrix[2][0] = 1
   #  Matrix[0][0] = 1
   #  Matrix[1][1] = 1
   #  Matrix[2][2] = 1
   #
   #  L1_index = L1_width - 1
   #  L1_compare_index = L1_width
   #  L2_index = L2_width
   #
   #  #count = countCrosses(Matrix, L1_index, L1_width, L2_width)
   #  #print(count)
   #  #count_pending = count
   #
   #  matrix_pending = [[0 for x in range(L1_width)] for y in range(L2_width)]
   #  matrix_pending = numpy.empty_like(Matrix)
   #  matrix_pending[:] = Matrix
   #
   #
   #  helpme = list(itertools.permutations(matrix_pending))
   #  for array in helpme:
   #      for row in array:
   #          print(row)
   #      print("\n")
   #  print("\n")
   # # matrix_pending = matrix_pending[:, numpy.random.permutation(matrix_pending.shape[1])]
   # # numpy.take(matrix_pending, numpy.random.permutation(matrix_pending.shape[0]), axis=0, out=matrix_pending);
   #  print_mat(matrix_pending)
   #  count = countCrosses(matrix_pending, L1_index, L1_width, L2_width)
   #  print(count)
   #  print("\n")

    #countCrosses(matrix_pending, L1_index, L1_width, L2_width)

   # if (count_pending < count):
    #    print("Yay")

    #for permutation in itertools.permutations(Matrix):
        #print(permutation)
        # s = [[str(e) for e in row] for row in test]
        # lens = [max(map(len, col)) for col in zip(*s)]
        # fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        # table = [fmt.format(*row) for row in s]
        # print('\n'.join(table))

if __name__ == "__main__":
    main()
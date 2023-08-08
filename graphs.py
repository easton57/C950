"""
Graph function for project 8
By: Easton Seidel
"""
import os
import math

# define some constants
max_value = os.sys.maxsize


class Graph:
    """ Our graph class for this project """

    def __init__(self, size):
        """ Initialization for graph """
        self.max_size = size

        # make an array full of max_value
        self.my_map = [[math.inf for x in range(self.max_size)] for y in range(self.max_size)]

        # fill my labels array with -1
        self.labels = [-1] * self.max_size

    def __str__(self):
        """ Print the graph """
        numvertices = self.find_numvertices()
        printed = False

        # print the first few lines
        output = ("numVertices: " + str(numvertices))
        output += ("\nVertex\tAdjacency List\n")

        # inefficient loop time yay
        for i in range(self.max_size):
            # print out the current vertex
            if self.labels[i] != -1:
                output += (self.labels[i] + "\t[")
            else:
                break

            # print out connecting vertex data
            for j in range(self.max_size):
                if self.my_map[i][j] is not math.inf:
                    # use a statement to determine if we need a comma
                    if printed is True:
                        output += (", (" + self.labels[j] + ", " + str(self.my_map[i][j]) + ")")
                    else:
                        output += ("(" + self.labels[j] + ", " + str(self.my_map[i][j]) + ")")
                        printed = True

            # set printed back to false and print a closed bracket
            printed = False
            output += ("]\n")

        print(output)

        return output

    def find_numvertices(self):
        """ Needed to find the number of vertices since I overcomplicated this in the beginning """
        total = 0

        for i in range(self.max_size):
            if self.labels[i] != -1:
                total += 1

        return total

    def add_vertex(self, label):
        """ Function to add a vertex to the graph """
        # verify that the label is a char or string
        # if type(label) != str:
        #     raise ValueError

        # loop to find the next empty
        for i in range(self.max_size):
            if self.labels[i] == -1:
                self.labels[i] = label
                return self

    def update_vertex(self, label, new_label):
        """ Function to update a vertex label of the graph """
        # Find the point that has the matching label
        for i in range(self.max_size):
            if label in self.labels[i][0] and self.labels[i] != -1:
                self.labels[i] = new_label
                return

    def add_edge(self, src, dest, w):
        """ Function to add a edge to the graph """
        # get the indexes of each point
        src_index = self.get_index(src)
        dest_index = self.get_index(dest)

        if src_index == -1 or dest_index == -1 or type(w) != int:
            if src_index == -1 or dest_index == -1 or type(w) != float:
                raise ValueError

        # Assign the weight to the map
        self.my_map[src_index][dest_index] = w

        return self

    def get_weight(self, src, dest):
        """ Function to return the weight of an edge """
        edge = 0

        # Find the index for the points
        src_index = self.get_index(src)
        dest_index = self.get_index(dest)

        if src_index == -1 or dest_index == -1:
            raise ValueError

        edge = self.my_map[src_index][dest_index]

        return edge

    def create_path(self, path, i, new_path):
        """ Function to recreate the path as a array """
        if path[i] == -1:
            new_path.append(self.labels[i])
            return new_path

        new_path.append(self.labels[i])

        return self.create_path(path, path[i], new_path)

    def get_index(self, label):
        """ Function to find the index of a label """
        for i in range(self.max_size):
            if label in self.labels[i][0] or label in self.labels[i][1]:
                return i

        print("Label not found")
        return -1

    def get_full_label(self, label):
        """ Function to find the index of a label """
        for i in range(self.max_size):
            if label in self.labels[i][0] or label in self.labels[i][1]:
                return self.labels[i]

        print("Label not found")
        return -1

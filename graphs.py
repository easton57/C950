"""
Graph function for project 8
By: Easton Seidel
"""
import os
import math

# define some constants
max_value = os.sys.maxsize
max_size = 10


class Graph:
    """ Our graph class for this project """

    def __init__(self):
        """ Initialization for graph """
        # make an array full of max_value
        self.my_map = [[math.inf for x in range(max_size)] for y in range(max_size)]

        # fill my labels array with -1
        self.labels = [-1] * max_size

    def __str__(self):
        """ Print the graph """
        numvertices = self.find_numvertices()
        printed = False

        # print the first few lines
        output = ("numVertices: " + str(numvertices))
        output += ("\nVertex\tAdjacency List\n")

        # inefficient loop time yay
        for i in range(max_size):
            # print out the current vertex
            if self.labels[i] != -1:
                output += (self.labels[i] + "\t[")
            else:
                break

            # print out connecting vertex data
            for j in range(max_size):
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

        for i in range(max_size):
            if self.labels[i] != -1:
                total += 1

        return total

    def add_vertex(self, label):
        """ Function to add a vertex to the graph """
        # verify that the label is a char or string
        if type(label) != str:
            raise ValueError

        # loop to find the next empty
        for i in range(max_size):
            if self.labels[i] == -1:
                self.labels[i] = label
                return self

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

    def dfs(self, starting_vertex):
        """ Depth first traversal """
        # print a cute little message
        print("Starting DFS with vertex", starting_vertex)

        # declare our queue
        queue = []
        visited = []
        j = 0

        # mark the starting_vertex as visited
        visited.append(starting_vertex)
        queue.append(self.get_index(starting_vertex))
        j += 1

        # loop a bit to visit each vertex
        while not self.is_empty(queue):
            # remove front item
            tmp = queue.pop()
            print("\tvisited", self.labels[tmp])

            # find adjacent vertices
            for i in range(max_size):
                # ignore if it is max_value or has been visited
                if self.my_map[tmp][i] is math.inf or self.already_visited(visited, i):
                    continue
                else:
                    visited.append(self.labels[i])
                    queue.append(i)

        return visited

    def bfs(self, starting_vertex):
        """ Breadth first traversal """
        # print a cute little message
        print("Starting BFS with vertex", starting_vertex)

        # declare our queue
        queue = []
        visited = []
        j = 0

        # mark the starting_vertex as visited
        visited.append(starting_vertex)
        queue.append(self.get_index(starting_vertex))
        j += 1

        # loop a bit to visit each vertex
        while not self.is_empty(queue):
            # remove front item
            tmp = queue.pop(0)
            print("\tvisited", self.labels[tmp])

            # find adjacent vertices
            for i in range(max_size):
                # ignore if it is max_value or has been visited
                if self.my_map[tmp][i] is math.inf or self.already_visited(visited, i):
                    continue
                else:
                    visited.append(self.labels[i])
                    queue.append(i)

        return visited

    def already_visited(self, visited, next_index):
        """ Function to check to see if we have visited a vertex """
        # loop to see if we have visited this sucker
        for i in range(len(visited)):
            if visited[i] == self.labels[next_index]:
                return True

        return False

    def is_empty(self, queue):
        """ Function to see if our queue is empty """
        try:
            queue[0]
        except IndexError:
            return True

        return False

    def dijkstra_shortest_path(self, src, dest=None):
        """ DSP for whole graph """
        # make sure src is in the map
        for i in range(max_size):
            if self.labels.index(src) is not None:
                break
            raise ValueError

        # declare needed stuff
        path = [-1] * max_size
        distance = [math.inf] * max_size
        prev_vertex = [math.inf] * max_size

        # set distance for starting vertex 0
        distance[self.get_index(src)] = 0

        # go through each vertex and find it's distance
        for i in range(max_size - 1):
            # declare some needed variables and give them ridiculous values
            min_path = math.inf

            for j in range(max_size):
                if prev_vertex[j] == math.inf and distance[j] <= min_path:
                    min_path = distance[j]
                    min_index = j

            # set the selected vertex as visited
            prev_vertex[min_index] = min_index

            # update the distance of adjacent vertices
            for k in range(max_size):
                if prev_vertex[k] and self.my_map[min_index][k] != math.inf and \
                        distance[min_index] != math.inf and \
                        distance[min_index] + self.my_map[min_index][k] < distance[k]:

                    path[k] = min_index
                    distance[k] = distance[min_index] + self.my_map[min_index][k]

        # choose whether we return everything or just a single path
        if dest is None:
            # put everything into a dict file
            all_paths = {}

            for i in range(max_size):
                # break if it goes too far
                if self.labels[i] == -1:
                    break

                if distance[i] == math.inf:
                    all_paths[self.labels[i]] = (math.inf, [])
                else:
                    all_paths[self.labels[i]] = (float(distance[i]), self.create_path(path, i, []))

            return all_paths
        else:
            if distance[self.get_index(dest)] == math.inf:
                my_tuple = (math.inf, [])
            else:
                path = self.create_path(path, self.get_index(dest), [])
                my_tuple = (float(distance[self.get_index(dest)]), path)
            return my_tuple

    def create_path(self, path, i, new_path):
        """ Function to recreate the path as a array """
        if path[i] == -1:
            new_path.append(self.labels[i])
            return new_path

        new_path.append(self.labels[i])

        return self.create_path(path, path[i], new_path)

    def get_index(self, label):
        """ Function to find the index of a label """
        for i in range(max_size):
            if self.labels[i] == label:
                return i

        print("Label not found")
        return -1

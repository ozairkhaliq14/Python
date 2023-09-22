import gc
import random
import math
import time
import psutil
import os
from collections import deque
import sys


# This class defines the state of the problem in terms of board configuration
class Board:
    def __init__(self, tiles):
        self.size = int(math.sqrt(len(tiles)))  # defining length/width of the board
        self.tiles = tiles

    # This function returns the resulting state from taking particular action from current state
    def execute_action(self, action):
        new_tiles = self.tiles[:]
        empty_index = new_tiles.index('0')
        if action == 'L':
            if empty_index % self.size > 0:
                new_tiles[empty_index - 1], new_tiles[empty_index] = new_tiles[empty_index], new_tiles[empty_index - 1]
        if action == 'R':
            if empty_index % self.size < (self.size - 1):
                new_tiles[empty_index + 1], new_tiles[empty_index] = new_tiles[empty_index], new_tiles[empty_index + 1]
        if action == 'U':
            if empty_index - self.size >= 0:
                new_tiles[empty_index - self.size], new_tiles[empty_index] = new_tiles[empty_index], new_tiles[
                    empty_index - self.size]
        if action == 'D':
            if empty_index + self.size < self.size * self.size:
                new_tiles[empty_index + self.size], new_tiles[empty_index] = new_tiles[empty_index], new_tiles[
                    empty_index + self.size]
        return Board(new_tiles)


# This class defines the node on the search tree, consisting of state, parent and previous action
class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

    # Returns string representation of the state
    def __repr__(self):
        return str(self.state.tiles)

    # Comparing current node with other node. They are equal if states are equal
    def __eq__(self, other):
        return self.state.tiles == other.state.tiles

    def __hash__(self):
        return hash(tuple(self.state.tiles))



class Search:

    # Utility function to randomly generate 15-puzzle
    def generate_puzzle(self, size):
        numbers = list(range(size * size))
        random.shuffle(numbers)
        return Node(Board(numbers), None, None)

    # This function returns the list of children obtained after simulating the actions on current node
    def get_children(self, parent_node):
        children = []
        actions = ['L', 'R', 'U', 'D']  # left,right, up , down ; actions define direction of movement of empty tile
        for action in actions:
            child_state = parent_node.state.execute_action(action)
            child_node = Node(child_state, parent_node, action)
            children.append(child_node)
        return children

    # This function backtracks from current node to reach initial configuration. The list of actions would constitute a solution path
    def find_path(self, node):
        path = []
        while (node.parent is not None):
            path.append(node.action)
            node = node.parent
        path.reverse()
        return path

    # This function runs breadth first search from the given root node and returns path, number of nodes expanded and total time taken
    def run_bfs(self, root_node):
        start_time = time.time()
        frontier = deque([root_node])
        explored = set()
        max_memory = 0
        while (len(frontier) > 0):
            max_memory = max(max_memory, sys.getsizeof(frontier) + sys.getsizeof(explored))
            cur_time = time.time()
            cur_node = frontier.popleft()
            explored.add(cur_node)
            if (self.goal_test(cur_node.state.tiles)):
                path = self.find_path(cur_node)
                end_time = time.time()

                return path, len(explored), (end_time - start_time), max_memory
            for child in self.get_children(cur_node):
                if child in explored:
                    continue
                else:
                    frontier.append(child)
        print("frontier empty")
        return False
    
    def get_all_nodes_at_depth(self, node, depth):
        if depth == 0:
            return [node]
        elif depth > 0:
            children = self.get_children(node)
            nodes = []
            for child in children:
                nodes += self.get_all_nodes_at_depth(child, depth-1)
            return nodes
        else:
            return []

    
    def run_ids(self,root_node): #Iterative Deepining Search
        def dls(node, limit): #Depth Limited Search
            nonlocal expanded_node # Want to use this outside of the nested func
            if self.goal_test(node.state.tiles):
                path = self.find_path(node)
                return path, 0
            elif limit == 0: #Abort if depth limit reached
                return False, 0
            else: 
                count = 0
                for child in self.get_children(node):
                    path, count_ = dls(child, limit - 1) #perform dls recursive
                    count += count_ #Node Counter
                    if path:
                        return path, count + 1
                    #gc.collect()
                return False, count + 1 #if no path found

        limit = 1
        start_time = time.time()
        expanded_node = 0
        end_time = time.time()
        frontier = [root_node]
        memory_consumed_each_depth = []
        memory_consumed = 0

        while (end_time := time.time() - start_time) < 30:
            #memory_consumed = psutil.Process().memory_info().rss
            memory_consumed = max(memory_consumed, sys.getsizeof(frontier) + sys.getsizeof(expanded_node)) #Calculate memory
            nodes_at_depth = self.get_all_nodes_at_depth(root_node, limit)
            memory_consumed_each_depth.append(sum(sys.getsizeof(n) for n in nodes_at_depth))
            path, count = dls(root_node, limit) #perform dls
            expanded_node += count #Node Counter
            if path: #return path if solution
                return path, expanded_node, end_time, memory_consumed, memory_consumed_each_depth
            limit += 1
            frontier = self.get_all_nodes_at_depth(root_node, limit)

        return None, None, None, None, None


    def goal_test(self, cur_tiles):
        return cur_tiles == ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '0']

    def solve(self, input):

        initial_list = input.split(" ")
        root = Node(Board(initial_list), None, None)
        path, expanded_nodes, time_taken, memory_consumed, memory_consumed_each_depth = self.run_ids(root)
        print("Moves: " + " ".join(path))
        print("Number of expanded Nodes: " + str(expanded_nodes))
        print("Time Taken: " + str(time_taken))
        print("Max Memory (Bytes): " + str(memory_consumed))
        #print("Memory Consumed at Each Depth (Bytes): " + str(memory_consumed_each_depth))
        return "".join(path)

if __name__ == '__main__':
    agent = Search()
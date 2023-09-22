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
    def __init__(self, state, parent, action, heuristic=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.heuristic = heuristic


        if heuristic == "manhattan":
            self.h = Search.manhattanDistance(self.state)
        elif heuristic == "misplaced":
            self.h = Search.misplacedTiles(self.state)
        else:
            self.h = 0



class Search:
    
    @staticmethod
    def manhattanDistance(tiles, size):
        distance = 0
        goal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
        for i, tile in enumerate(tiles):
            if tile != 0:
                tile_row, tile_col = divmod(i, size)
                goal_index = goal.index(tile)
                goal_row, goal_col = divmod(goal_index, size)
                distance += abs(tile_row - goal_row) + abs(tile_col - goal_col)
        return distance


    @staticmethod
    def misplacedTiles(tiles):
        distance = 0
        goal = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '0']
        for i, tile in enumerate(tiles):
            if tile != goal[i]:
                distance += 1
        return distance

    # Utility function to randomly generate 15-puzzle
    def generate_puzzle(self, size):
        numbers = list(range(size * size))
        random.shuffle(numbers)
        return Node(Board(numbers), None, None, None)

    # This function returns the list of children obtained after simulating the actions on current node
    def get_children(self, parent_node, heuristic):
        children = []
        actions = ['L', 'R', 'U', 'D']  # left,right, up , down ; actions define direction of movement of empty tile
        for action in actions:
            child_state = parent_node.state.execute_action(action)
            child_node = Node(child_state, parent_node, action, heuristic)
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
            for child in self.get_children(cur_node, self.heuristic):
                if child in explored:
                    continue
                else:
                    frontier.append(child)
        print("frontier empty")
        return False
    
    def run_astarSearch(self, root_node, heuristic):
        start_time = time.time()
        expanded_node = 0
        end_time = time.time()
        frontier = [root_node]
        memory_consumed_each_depth = []
        memory_consumed = 0
        explored = []

        while frontier:
            memory_consumed = max(memory_consumed, str(sys.getsizeof(frontier)) + str(sys.getsizeof(explored))) #Calculate memory
            cur_time = time.time()
            if cur_time - start_time > 30:
                return "solution not found"
            cur_node = frontier.pop(0)
            expanded_node += 1
            explored.append(cur_node)

            if self.goal_test(cur_node.state.tiles):
                path = self.find_path(cur_node)
                end_time = time.time()
                return (path, expanded_node, end_time - start_time, memory_consumed)
            
            for child in self.get_children(cur_node, heuristic):
                if child not in explored:
                    frontier.append(child)
                    frontier.sort(key=lambda node: node.g + node.h)
        return False

    def goal_test(self, cur_tiles):
        return cur_tiles == ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '0']

    def solve(self, initial_state, heuristic = "manhattan"): # Format : "1 0 2 4 5 7 3 8 9 6 11 12 13 10 14 15"
        initial_list = initial_state.split(" ")
        goal_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
        # Convert the strings to integers
        initial_list = list(map(int, initial_list))
        goal_list = list(map(int, goal_list))

        # Create the initial and goal nodes
        initial_node = Node(Board(initial_list), None, None)
        goal_node = Node(Board(goal_list), None, None)
        
        #Please use this as a reference to run with gradescope autograder.
        if heuristic == "manhattan":
            solution_moves = self.manhattanDistance(initial_list, len(initial_list))
        elif heuristic == "misplaced tiles":
            solution_moves = self.misplacedTiles(initial_list)
        
        print("Moves: " + solution_moves)
        print("Number of expanded Nodes: " + str(""))
        print("Time Taken: " + str(""))
        print("Max Memory (Bytes): " + str(""))
        return solution_moves # Get the list of moves to solve the puzzle. Format is "RDLDDRR"

if __name__ == '__main__':
    #Node.heuristic = input
    agent = Search()
    agent.solve()
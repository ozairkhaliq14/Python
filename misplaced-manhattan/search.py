import random
import math
import time
import psutil
import os
from collections import deque
import sys

class Search:
 
    def misplacedTiles(goal_state, node):
        n = node.state.tiles
        number_of_misplaced_tiles = sum([n[i] != goal_state[i] for i in range(len(goal_state))])
        return number_of_misplaced_tiles
    
    def manhattanDistance(child_state, self):
        goal_state = self.get_goal()
        size_of_child_state = child_state.state.size
        child_state_tiles = child_state.state.tiles
        goal_state_tiles = goal_state
        child_state_array = [child_state_tiles[i:i+size_of_child_state] for i in range(0, len(child_state_tiles), size_of_child_state)]
        goal_state_array = [goal_state_tiles[i:i+size_of_child_state] for i in range(0, len(goal_state_tiles), size_of_child_state)]
        manhattan_distance = 0
        for i in range(size_of_child_state):
            for j in range(size_of_child_state):
                if child_state_array[i][j] != 0:
                    row_goal, col_goal = divmod(goal_state.index(child_state_array[i][j]), size_of_child_state)
                    manhattan_distance += abs(i - row_goal) + abs(j - col_goal)
        return manhattan_distance

    
    def run_idastar(root_node, heuristic, self):
        start_time = time.time()
        bound = root_node.cost
        path = deque([root_node])
        explored = set()
        iteration = 0
        while True:
            explored.clear()
            found, final_path, no_of_nodes, cost = self.run_dls(path, 0, bound, explored, heuristic)
            if found == 'FOUND':
                end_time = time.time()
                return final_path, no_of_nodes, (end_time - start_time), sys.getsizeof(explored)
            if cost == float('inf'):
                return None
            bound = cost
            iteration += 1

    def run_dls(path, cost, limit, explored, heuristic, self):
        current_node = path[-1]
        f_score = cost + current_node.cost

        if f_score > limit:
            return 'NOT FOUND', None, None, f_score

        if self.goal_test(current_node):
            final_path = self.find_path(current_node)
            return 'FOUND', final_path, len(explored), None

        lowest_cost = float('inf')

        for child_node in self.get_children(current_node, heuristic):
            if child_node not in path:
                path.append(child_node)
                explored.add(child_node)
                found, final_path, no_of_nodes, cost = self.run_dls(path, cost + 1, limit, explored, heuristic)
                if found == 'FOUND':
                    return 'FOUND', final_path, len(explored), None
                if cost < lowest_cost:
                    lowest_cost = cost
                path.pop()

        if lowest_cost == float('inf'):
            return 'NOT FOUND', None, None, lowest_cost
        else:
            return 'NOT FOUND', None, None, lowest_cost + current_node.cost


    def goal_test(self, cur_tiles):
        return cur_tiles == ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '0']

    def get_goal():
        return ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','0']
    
    
    def solve(self, initial_state, heuristic = "manhattan"): # Format : "1 0 2 4 5 7 3 8 9 6 11 12 13 10 14 15"
        initial_list = initial_state.split(" ")
        """ 
        Please use this as a reference to run with gradescope autograder.
        """
        if heuristic == "manhattan":
            solution_moves = self.manhattanDistance(initial_list)
        if heuristic == "misplaced tiles":
            solution_moves = self.misplacedTiles(initial_list)
        
        print("Moves: " + " ".join(self.path))
        print("Number of expanded Nodes: " + str(""))
        print("Time Taken: " + str(""))
        print("Max Memory (Bytes): " + str(""))
        return "".join(self.path) # Get the list of moves to solve the puzzle. Format is "RDLDDRR"




if __name__ == '__main__':
    agent = Search()
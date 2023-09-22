import queue
import time
import psutil

class Search:

    def __init__(self):
        self.visited = set()

    def goal_test(self, cur_tiles):
        return cur_tiles == ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '0']

    def move_tiles(self, cur_tiles, direction):
        # Find the index of the 0 (empty space) tile
        idx = cur_tiles.index('0')

        if direction == 'U':
            if idx < 4:
                return None # Cannot move up, return None
            # Swap the empty space with the tile above it
            new_tiles = cur_tiles.copy()
            new_tiles[idx], new_tiles[idx - 4] = new_tiles[idx - 4], new_tiles[idx]
            return new_tiles
        
        if direction == 'D':
            if idx > 11:
                return None # Cannot move down, return None
            # Swap the empty space with the tile below it
            new_tiles = cur_tiles.copy()
            new_tiles[idx], new_tiles[idx + 4] = new_tiles[idx + 4], new_tiles[idx]
            return new_tiles

        if direction == 'L':
            if idx in [0, 4, 8, 12]:
                return None # Cannot move left, return None
            # Swap the empty space with the tile to the left
            new_tiles = cur_tiles.copy()
            new_tiles[idx], new_tiles[idx - 1] = new_tiles[idx - 1], new_tiles[idx]
            return new_tiles
        
        if direction == 'R':
            if idx in [3, 7, 11, 15]:
                return None # Cannot move right, return None
            # Swap the empty space with the tile to the right
            new_tiles = cur_tiles.copy()
            new_tiles[idx], new_tiles[idx + 1] = new_tiles[idx + 1], new_tiles[idx]
            return new_tiles
    
        return None


    def run_bfs(self, start):
        q = queue.Queue()
        q.put((start, [])) # (current state, moves to reach this state)
        self.visited.clear()
        self.visited.add(tuple(start))

        while not q.empty():
            cur_tiles, moves = q.get()
            if self.goal_test(cur_tiles):
                return moves
            
            for direction in ['U', 'D', 'L', 'R']:
                new_tiles = self.move_tiles(cur_tiles, direction)
                if new_tiles is not None and tuple(new_tiles) not in self.visited:
                    q.put((new_tiles, moves + [direction]))
                    self.visited.add(tuple(new_tiles))
        return None
    
    def solve(self, input): # Format : "1 0 2 4 5 7 3 8 9 6 11 12 13 10 14 15"
        initial_list = input.split(" ")
        start_time = time.time()
        solution_moves = self.run_bfs(initial_list)
        end_time = time.time()
        time_taken = end_time - start_time
        num_expanded_nodes = len(self.visited)
        process = psutil.Process()
        memory_info = process.memory_info()
        max_memory = memory_info.rss
        print("Moves: " + "".join(solution_moves))
        print("Number of expanded Nodes: " + str(num_expanded_nodes))
        print("Time Taken: " + str(time_taken))
        print("Max Memory (Bytes): " + str(max_memory))
        return "".join(solution_moves)
    
if __name__ == 'main':
    agent = Search()
    agent.solve("1 0 2 4 5 7 3 8 9 6 11 12 13 10 14 15")
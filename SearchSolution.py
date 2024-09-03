import heapq
from collections import deque


class SearchSolution:
    def __init__(self, maze_map, start, goal, max_rows, max_cols):
        self.maze = dict(maze_map)
        self.start = start
        self.goal = goal
        self.rows = max_rows
        self.cols = max_cols
        self.num_created = 0
        self.num_expanded = 0
        self.max_fringe = 0

    def get_directions(self, position):
        curr_row, curr_col = position
        direction_map = {
            'E': (0, 1),
            'W': (0, -1),
            'N': (-1, 0),
            'S': (1, 0)
        }
        result = []

        possible_directions = dict(self.maze.get((curr_row, curr_col)))
        for direction, isOpen in possible_directions.items():
            if isOpen == 1:
                row_to_add, col_to_add = direction_map.get(direction)
                new_row = curr_row + row_to_add
                new_col = curr_col + col_to_add
                if 0 <= new_row <= self.rows and 0 <= new_col <= self.cols:
                    result.append((new_row, new_col))
        return result

    def bfs(self):
        """
        Implement BFS to find the solution path
        """
        queue = deque([(self.start, [self.start])])
        visited = set()
        while queue:
            self.max_fringe = max(self.max_fringe, len(queue))
            current, path = queue.popleft()
            self.num_expanded += 1
            if current in visited:
                continue
            visited.add(current)
            if current == self.goal:
                return path, len(path) - 1
            for direction in self.get_directions(current):
                if direction not in visited:
                    self.num_created += 1
                    queue.append((direction, path + [direction]))
        return [], -1

    def dfs(self):
        """
        Implement DFS to find the solution path
        """
        queue = deque([(self.start, [self.start])])
        visited = set()
        while queue:
            self.max_fringe = max(self.max_fringe, len(queue))
            current, path = queue.popleft()
            self.num_expanded += 1
            if current in visited:
                continue
            visited.add(current)
            if current == self.goal:
                return path, len(path) - 1
            new_queue = deque()
            for direction in self.get_directions(current):
                if direction not in visited:
                    self.num_created += 1
                    new_queue.append((direction, path + [direction]))
            queue.extend(new_queue)
            print(queue)
        return [], -1

    def manhattan_distance(self, position):
        """
        Calculate the Manhattan Distance as the heuristic
        """
        return abs(position[0] - self.goal[0] + abs(position[1] - self.goal[1]))

    def greedy_search(self):
        """
        Implement Greedy Search to find the solution path
        """
        queue = []
        heapq.heappush(queue, (self.manhattan_distance(self.start), self.start, [self.start]))
        visited = set()
        while queue:
            self.max_fringe = max(self.max_fringe, len(queue))
            _, current, path = heapq.heappop(queue)
            self.num_expanded += 1
            if current in visited:
                continue
            visited.add(current)
            if current == self.goal:
                return path, len(path) - 1
            for direction in self.get_directions(current):
                if direction not in visited:
                    self.num_created += 1
                    heapq.heappush(queue, (self.manhattan_distance(direction), direction, path + [direction]))
        return [], -1

    def a_star(self):
        """
        Implement A* to find the solution path
        """
        cost = {self.start: 0}
        queue = []
        heapq.heappush(queue, (self.manhattan_distance(self.start), self.start, [self.start]))
        visited = set()
        while queue:
            self.max_fringe = max(self.max_fringe, len(queue))
            _, current, path = heapq.heappop(queue)
            self.num_expanded += 1
            if current in visited:
                continue
            visited.add(current)
            if current == self.goal:
                return path, len(path) - 1
            for direction in self.get_directions(current):
                if direction not in visited:
                    self.num_created += 1
                    new_cost = cost[current] + 1
                    cost[direction] = new_cost
                    total_cost = new_cost + self.manhattan_distance(direction)
                    heapq.heappush(queue, (total_cost, direction, path + [direction]))
        return [], -1

import argparse
import random
from pyamaze import maze, agent, COLOR
from SearchSolution import SearchSolution


# Create a maze
def create_maze(M, N, theme='light', pattern='horizontal'):
    m = maze(M, N)
    if theme == 'light':
        m.theme = COLOR.light
    else:
        m.theme = COLOR.dark
    if pattern == 'vertical':
        m.CreateMaze(loopPercent=100, pattern='v')
    else:
        m.CreateMaze(loopPercent=100, pattern='h')
    return m


# Generate random positions for the agent and goal
def generate_random_positions(M, N):
    agent_row, agent_col = random.randint(1, M), random.randint(1, N)
    goal_row, goal_col = random.randint(1, M), random.randint(1, N)
    while (agent_row, agent_col) == (goal_row, goal_col):
        agent_row, agent_col = random.randint(1, M), random.randint(1, N)
    return (agent_row, agent_col), (goal_row, goal_col)


def main():
    parser = argparse.ArgumentParser(description='Maze Runner')
    parser.add_argument('M', type=int, help='Total number of Maze rows')
    parser.add_argument('N', type=int, help='Total number of Maze columns')
    parser.add_argument('searchMethod', type=str, help='BFS, DFS, GS, AStar')
    args = parser.parse_args()

    my_maze = create_maze(args.M, args.N)
    (agent_row, agent_col), (goal_row, goal_col) = generate_random_positions(args.M, args.N)

    # Create agent and goal positions in the maze
    a = agent(my_maze, agent_row, agent_col, shape='arrow', color=COLOR.red, footprints=True)
    agent(my_maze, goal_row, goal_col, shape='square', color=COLOR.yellow)
    my_maze.markCells.append((goal_row, goal_col))

    # Initialize the SearchSolution with 0-based indexing for agent and goal positions
    search_solution = SearchSolution(my_maze.maze_map,
                                     (agent_row, agent_col),
                                     (goal_row, goal_col), args.M, args.N)

    # Execute the specified search method
    if args.searchMethod == 'BFS':
        path, depth = search_solution.bfs()
    elif args.searchMethod == 'DFS':
        path, depth = search_solution.dfs()
    elif args.searchMethod == 'GS':
        path, depth = search_solution.greedy_search()
    elif args.searchMethod == 'AStar':
        path, depth = search_solution.a_star()
    else:
        print("Unknown search method")
        return

    # Write results to Readme.txt
    with open("Readme.txt", "a") as file:
        file.write(
            f"{args.M}x{args.N} {args.searchMethod}: "
            f"{depth}, {search_solution.num_created}, "
            f"{search_solution.num_expanded}, {search_solution.max_fringe}\n")

    # Visualize the path in the maze with color fill
    if path:
        print(f"Path found: {path}")
        path = [(step[0], step[1]) for step in path]
        my_maze.tracePath({a: path}, delay=100)

        # Color fill each solution path location
        for step in path:
            my_maze.markCells.append((step[0], step[1], COLOR.cyan))
    else:
        print("Path not found")

    my_maze.run()


if __name__ == "__main__":
    main()

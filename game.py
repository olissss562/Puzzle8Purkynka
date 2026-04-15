import heapq
import random

N = 3

GOAL_POSITIONS = {
    1: (0, 0), 2: (0, 1), 3: (0, 2),
    4: (1, 0), 5: (1, 1), 6: (1, 2),
    7: (2, 0), 8: (2, 1), 0: (2, 2)
}

def manhattan_distance(board):
    distance = 0
    for r in range(N):
        for c in range(N):
            val = board[r][c]
            if val != 0:
                goal_r, goal_c = GOAL_POSITIONS[val]
                distance += abs(r - goal_r) + abs(c - goal_c)
    return distance

def is_solvable(board):
    flat_board = []             
    for row in board:            
        for num in row:          
            if num != 0:          
                flat_board.append(num)
    inversions = 0
    for i in range(len(flat_board)):
        for j in range(i + 1, len(flat_board)):
            if flat_board[i] > flat_board[j]:
                inversions += 1
    return inversions % 2 == 0

def generate_random_board():
    numbers = list(range(9))
    while True:
        random.shuffle(numbers)
        board = [numbers[0:3], numbers[3:6], numbers[6:9]]
        
        if is_solvable(board):
            for r in range(N):
                for c in range(N):
                    if board[r][c] == 0:
                        return board, r, c #algorhytm needs to know on which coordinates is zero

class PuzzleState:
    def __init__(self, board, x, y, depth, path):
        self.board = board
        self.x = x
        self.y = y
        self.depth = depth
        self.path = path
        self.cost = depth + manhattan_distance(board)

    def __lt__(self, other):
        return self.cost < other.cost

row = [0, 0, -1, 1]
col = [-1, 1, 0, 0]

def is_valid(x, y):
    return 0 <= x < N and 0 <= y < N

def solve_puzzle_astar_generator(start, x, y):
    queue = []
    visited = set()

    start_state = PuzzleState(start, x, y, 0, [start])
    heapq.heappush(queue, start_state)
    visited.add(tuple(map(tuple, start)))

    while queue:
        curr = heapq.heappop(queue)

        yield ("SEARCHING", curr.board)

        if manhattan_distance(curr.board) == 0:
            yield ("FOUND", curr.path)
            return

        for i in range(4):
            new_x = curr.x + row[i]
            new_y = curr.y + col[i]

            if is_valid(new_x, new_y):
                new_board = [r[:] for r in curr.board]
                new_board[curr.x][curr.y], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[curr.x][curr.y]

                board_tuple = tuple(map(tuple, new_board))
                if board_tuple not in visited:
                    visited.add(board_tuple)
                    new_path = curr.path + [new_board]
                    new_state = PuzzleState(new_board, new_x, new_y, curr.depth + 1, new_path)
                    
                    heapq.heappush(queue, new_state)
                    
    yield ("NOT_FOUND", [])
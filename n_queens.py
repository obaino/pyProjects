"""
The N-Queens problem involves placing N queens on an NxN chessboard such that no two queens threaten each other. 
This means no two queens can share the same row, column, or diagonal. Below is a Python solution using backtracking 
to solve the problem for a given board size N.
"""

def solve_n_queens(n):
    def create_board(positions):
        board = [['.' for _ in range(n)] for _ in range(n)]
        for row, col in enumerate(positions):
            board[row][col] = 'Q'
        return board

    def is_safe(row, col, queens):
        for prev_row, prev_col in enumerate(queens[:row]):
            if prev_col == col:
                return False
            if abs(prev_row - row) == abs(prev_col - col):
                return False
        return True

    def solve(row, queens, solutions):
        if row == n:
            solutions.append(create_board(queens))
            return
        for col in range(n):
            if is_safe(row, col, queens):
                queens[row] = col
                solve(row + 1, queens, solutions)
                queens[row] = 0

    queens = [0] * n
    solutions = []
    solve(0, queens, solutions)
    return solutions

def print_solutions(solutions):
    for i, solution in enumerate(solutions):
        print(f"Solution {i + 1}:")
        for row in solution:
            print(' '.join(row))
        print()

# Example usage for nxn board
n = int(input("Enter the value of n for the N-Queens problem: "))
solutions = solve_n_queens(n)
print(f"Found {len(solutions)} solutions for {n}-Queens problem:")
print_solutions(solutions)
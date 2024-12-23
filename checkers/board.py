import pygame
from .constants import ROWS, COLS, SQUARE_SIZE, RED, WHITE, DARK_BROWN, LIGHT_BROWN
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()

    def draw_squares(self, win):
        win.fill(LIGHT_BROWN)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, DARK_BROWN, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                pygame.draw.rect(win, (0, 0, 0), (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = 0, piece
        piece.move(row, col)

        if (row == 0 and piece.color == WHITE) or (row == ROWS - 1 and piece.color == RED):
            if not piece.king:
                piece.make_king()
                if piece.color == RED:
                    self.red_kings += 1
                else:
                    self.white_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if (row + col) % 2 == 1:
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED
        return None

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)] if piece.king else \
            [(-1, -1), (-1, 1)] if piece.color == WHITE else [(1, -1), (1, 1)]

        for dr, dc in directions:
            moves.update(self._traverse_direction(row + dr, piece.row, dr, piece.col + dc, dc, piece.color, [], piece.king))

        return moves

    def _traverse_direction(self, row, start, dr, col, dc, color, skipped, is_king):
        moves = {}
        last = []

        while 0 <= row < ROWS and 0 <= col < COLS:
            current = self.board[row][col]
            if current == 0:
                if skipped and not last:
                    break
                moves[(row, col)] = last + skipped
                if last:
                    next_row = row + dr
                    next_col = col + dc
                    moves.update(self._traverse_direction(next_row, start, dr, next_col, dc, color, skipped + last, is_king))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            row += dr
            col += dc

        return moves

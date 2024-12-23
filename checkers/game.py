import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE, WIDTH, HEIGHT, LIGHT_BROWN, DARK_BROWN, GOLD
from checkers.board import Board

class Game:
    def __init__(self, win):
        self.win = win
        self._init()

    def update(self, hover_pos=None):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        self.draw_turn_banner()
        if hover_pos:
            self.draw_hover_highlight(hover_pos)
        winner = self.winner()
        if winner:
            self.draw_winner(winner)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
            
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False
        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(
                self.win, BLUE,
                (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                15
            )

    def draw_turn_banner(self):
        font = pygame.font.SysFont('comicsans', 30)
        color = 'Red' if self.turn == RED else 'White'
        text = font.render(f"Turn: {color}", True, (255, 255, 255))
        pygame.draw.rect(self.win, (0, 0, 0), (10, 10, 140, 35))  # background box
        self.win.blit(text, (15, 15))

    def draw_hover_highlight(self, pos):
        x, y = pos
        col, row = x // SQUARE_SIZE, y // SQUARE_SIZE
        rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(self.win, GOLD, rect, 3)

    def draw_winner(self, color):
        font = pygame.font.SysFont('comicsans', 60)
        color_text = 'Red' if color == RED else 'White'
        text = font.render(f"{color_text} Wins!", True, (0, 255, 0))
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.win.blit(text, rect)

    def change_turn(self):
        self.valid_moves = {}
        self.turn = WHITE if self.turn == RED else RED

    def winner(self):
        return self.board.winner()

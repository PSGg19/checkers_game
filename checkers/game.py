import pygame
from .constants import MOVE_SOUND, CAPTURE_SOUND

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
        pygame.mixer.init()  # Initialize Pygame mixer for sound effects

    def _play_sound(self, sound):
        pygame.mixer.Sound(sound).play()

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
                self._play_sound(CAPTURE_SOUND)  # Play capture sound
            else:
                self._play_sound(MOVE_SOUND)  # Play move sound
            self.change_turn()
        else:
            return False

        return True


    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(
                self.win,
                BLUE,
                (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                15,
            )

    def draw_turn_indicator(self):
        text = "Turn: RED" if self.turn == RED else "Turn: WHITE"
        color = RED if self.turn == RED else WHITE
        pygame.draw.rect(self.win, (30, 30, 30), (10, 10, 150, 30), border_radius=5)
        label = self.font.render(text, True, color)
        self.win.blit(label, (20, 15))

    def draw_hover_highlight(self):
        mouse_pos = pygame.mouse.get_pos()
        row = mouse_pos[1] // SQUARE_SIZE
        col = mouse_pos[0] // SQUARE_SIZE
        pygame.draw.rect(
            self.win,
            (255, 255, 0),
            (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
            3,
        )

    def change_turn(self):
        self.valid_moves = {}
        self.turn = WHITE if self.turn == RED else RED

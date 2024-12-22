import pygame
from .constants import MOVE_SOUND, CAPTURE_SOUND

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
        self.timer_start = time.time()
        self.time_limit = 30  # Time limit for each turn (in seconds)
    
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        self._draw_timer()
        pygame.display.update()

    def _draw_timer(self):
        current_time = int(time.time() - self.timer_start)
        time_left = self.time_limit - current_time
        if time_left >= 0:
            font = pygame.font.Font(None, 36)
            timer_text = font.render(f"Time Left: {time_left}s", True, (255, 255, 255))
            self.win.blit(timer_text, (500, 10))  # Display at top-right

    def change_turn(self):
        self.timer_start = time.time()  # Reset timer when turn changes
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED
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

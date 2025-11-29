import pygame
import random
from collections import defaultdict

pygame.init()

GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30
GRID_X_OFFSET = 50
GRID_Y_OFFSET = 50

SCREEN_WIDTH = GRID_X_OFFSET * 2 + GRID_WIDTH * CELL_SIZE + 200
SCREEN_HEIGHT = GRID_Y_OFFSET * 2 + GRID_HEIGHT * CELL_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 215, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
]

SHAPE_COLORS = [CYAN, YELLOW, PURPLE, GREEN, RED, BLUE, ORANGE]


class TetrisGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("TetrisEsoLang")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = None
        self.current_x = 0
        self.current_y = 0
        self.current_shape = None
        self.current_color = None
        self.fall_time = 0
        self.fall_speed = 500
        self.score = 0
        self.game_over = False
        
        self.cleared_lines = {}
        self.line_counter = 0
        
        self.spawn_piece()
    
    def spawn_piece(self):
        """Spawn a new tetromino piece with binary values (1 or 0) for each block"""
        shape_idx = random.randint(0, len(SHAPES) - 1)
        self.current_shape = [row[:] for row in SHAPES[shape_idx]]
        self.current_color = SHAPE_COLORS[shape_idx]
        
        self.current_piece = []
        block_counter = 0
        for row in self.current_shape:
            piece_row = []
            for cell in row:
                if cell == 1:
                    piece_row.append(block_counter % 2)
                    block_counter += 1
                else:
                    piece_row.append(None)
            self.current_piece.append(piece_row)
        
        self.current_x = GRID_WIDTH // 2 - len(self.current_shape[0]) // 2
        self.current_y = 0
        
        if self.check_collision(self.current_x, self.current_y, self.current_shape, self.current_piece):
            self.game_over = True
    
    def rotate_piece(self):
        """Rotate the current piece 90 degrees clockwise, preserving binary values"""
        if self.current_shape is None:
            return
        
        rotated_shape = list(zip(*reversed(self.current_shape)))
        rotated_shape = [list(row) for row in rotated_shape]
        
        original_height = len(self.current_shape)
        
        rotated_piece = [[None for _ in range(len(rotated_shape[0]))] for _ in range(len(rotated_shape))]
        
        for orig_row in range(original_height):
            for orig_col in range(len(self.current_shape[orig_row])):
                if self.current_shape[orig_row][orig_col] == 1:
                    new_row = orig_col
                    new_col = original_height - 1 - orig_row
                    rotated_piece[new_row][new_col] = self.current_piece[orig_row][orig_col]
        
        if not self.check_collision(self.current_x, self.current_y, rotated_shape, rotated_piece):
            self.current_shape = rotated_shape
            self.current_piece = rotated_piece
    
    def check_collision(self, x, y, shape, piece_binary=None):
        """Check if the piece at position (x, y) collides with anything"""
        if piece_binary is None:
            piece_binary = self.current_piece
        
        for row_idx, row in enumerate(shape):
            for col_idx, cell in enumerate(row):
                if cell == 1:
                    grid_x = x + col_idx
                    grid_y = y + row_idx
                    
                    if grid_x < 0 or grid_x >= GRID_WIDTH or grid_y >= GRID_HEIGHT:
                        return True
                    
                    if grid_y >= 0 and self.grid[grid_y][grid_x] is not None:
                        existing_binary = self.grid[grid_y][grid_x]['binary']
                        current_binary = piece_binary[row_idx][col_idx]
                        if existing_binary == current_binary:
                            return True
        
        return False
    
    def place_piece(self):
        """Place the current piece on the grid"""
        for row_idx, row in enumerate(self.current_shape):
            for col_idx, cell in enumerate(row):
                if cell == 1:
                    grid_x = self.current_x + col_idx
                    grid_y = self.current_y + row_idx
                    
                    if grid_y >= 0:
                        binary_value = self.current_piece[row_idx][col_idx]
                        self.grid[grid_y][grid_x] = {
                            'color': self.current_color,
                            'binary': binary_value
                        }
        
        self.check_lines()
        
        self.spawn_piece()
    
    def check_lines(self):
        """Check and clear completed lines, storing binary values"""
        lines_to_clear = []
        
        for row_idx in range(GRID_HEIGHT):
            if all(cell is not None for cell in self.grid[row_idx]):
                lines_to_clear.append(row_idx)
        
        for row_idx in reversed(lines_to_clear):
            binary_line = []
            for cell in self.grid[row_idx]:
                if cell is not None:
                    binary_line.append(cell['binary'])
                else:
                    binary_line.append(0)
            
            self.line_counter += 1
            self.cleared_lines[f"line_{self.line_counter}"] = binary_line
            
            self.grid.pop(row_idx)
            self.grid.insert(0, [None for _ in range(GRID_WIDTH)])
            
            self.score += 100
    
    def move_piece(self, dx, dy):
        """Move the current piece"""
        if not self.check_collision(self.current_x + dx, self.current_y + dy, self.current_shape, self.current_piece):
            self.current_x += dx
            self.current_y += dy
            return True
        return False
    
    def drop_piece(self):
        """Drop the piece to the bottom"""
        while self.move_piece(0, 1):
            pass
        self.place_piece()
    
    def draw_grid(self):
        """Draw the game grid"""
        grid_rect = pygame.Rect(
            GRID_X_OFFSET,
            GRID_Y_OFFSET,
            GRID_WIDTH * CELL_SIZE,
            GRID_HEIGHT * CELL_SIZE
        )
        pygame.draw.rect(self.screen, BLACK, grid_rect)
        pygame.draw.rect(self.screen, WHITE, grid_rect, 2)
        
        for i in range(GRID_WIDTH + 1):
            x = GRID_X_OFFSET + i * CELL_SIZE
            pygame.draw.line(self.screen, GRAY, (x, GRID_Y_OFFSET), 
                           (x, GRID_Y_OFFSET + GRID_HEIGHT * CELL_SIZE))
        
        for i in range(GRID_HEIGHT + 1):
            y = GRID_Y_OFFSET + i * CELL_SIZE
            pygame.draw.line(self.screen, GRAY, 
                           (GRID_X_OFFSET, y),
                           (GRID_X_OFFSET + GRID_WIDTH * CELL_SIZE, y))
    
    def draw_placed_blocks(self):
        """Draw all placed blocks on the grid"""
        for row_idx, row in enumerate(self.grid):
            for col_idx, cell in enumerate(row):
                if cell is not None:
                    x = GRID_X_OFFSET + col_idx * CELL_SIZE
                    y = GRID_Y_OFFSET + row_idx * CELL_SIZE
                    
                    rect = pygame.Rect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2)
                    pygame.draw.rect(self.screen, cell['color'], rect)
                    
                    binary_text = self.small_font.render(str(cell['binary']), True, WHITE)
                    text_rect = binary_text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                    self.screen.blit(binary_text, text_rect)
    
    def draw_current_piece(self):
        """Draw the current falling piece"""
        if self.current_shape is None:
            return
        
        for row_idx, row in enumerate(self.current_shape):
            for col_idx, cell in enumerate(row):
                if cell == 1:
                    x = GRID_X_OFFSET + (self.current_x + col_idx) * CELL_SIZE
                    y = GRID_Y_OFFSET + (self.current_y + row_idx) * CELL_SIZE
                    
                    rect = pygame.Rect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2)
                    pygame.draw.rect(self.screen, self.current_color, rect)
                    
                    binary_value = self.current_piece[row_idx][col_idx]
                    binary_text = self.small_font.render(str(binary_value), True, WHITE)
                    text_rect = binary_text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                    self.screen.blit(binary_text, text_rect)
    
    def draw_info(self):
        """Draw game information"""
        info_x = GRID_X_OFFSET + GRID_WIDTH * CELL_SIZE + 20
        
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (info_x, GRID_Y_OFFSET))
        
        lines_text = self.font.render(f"Lines: {self.line_counter}", True, WHITE)
        self.screen.blit(lines_text, (info_x, GRID_Y_OFFSET + 40))
        
        controls_y = GRID_Y_OFFSET + 100
        controls = [
            "Controls:",
            "A/D - Move",
            "S - Soft Drop",
            "W - Rotate",
            "SPACE - Hard Drop"
        ]
        
        for i, control in enumerate(controls):
            control_text = self.small_font.render(control, True, WHITE)
            self.screen.blit(control_text, (info_x, controls_y + i * 25))
        
        dict_y = GRID_Y_OFFSET + 250
        dict_text = self.small_font.render("Cleared Lines:", True, WHITE)
        self.screen.blit(dict_text, (info_x, dict_y))
        
        if self.cleared_lines:
            display_y = dict_y + 30
            for i, (key, value) in enumerate(list(self.cleared_lines.items())[-5:]):
                line_str = f"{key}: {value}"
                line_text = self.small_font.render(line_str[:30], True, WHITE)
                self.screen.blit(line_text, (info_x, display_y + i * 20))
    
    def draw_game_over(self):
        """Draw game over screen"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font.render("GAME OVER", True, WHITE)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(game_over_text, text_rect)
        
        restart_text = self.small_font.render("Press R to restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        self.screen.blit(restart_text, restart_rect)
    
    def reset_game(self):
        """Reset the game"""
        self.grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = None
        self.current_x = 0
        self.current_y = 0
        self.current_shape = None
        self.current_color = None
        self.fall_time = 0
        self.score = 0
        self.game_over = False
        self.cleared_lines = {}
        self.line_counter = 0
        self.spawn_piece()
    
    def update(self, dt):
        """Update game state"""
        if self.game_over:
            return
        
        self.fall_time += dt
        if self.fall_time >= self.fall_speed:
            if not self.move_piece(0, 1):
                self.place_piece()
            self.fall_time = 0
    
    def draw(self):
        """Draw everything"""
        self.screen.fill((20, 20, 20))
        self.draw_grid()
        self.draw_placed_blocks()
        self.draw_current_piece()
        self.draw_info()
        
        if self.game_over:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            dt = self.clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if self.game_over:
                        if event.key == pygame.K_r:
                            self.reset_game()
                    else:
                        if event.key == pygame.K_a:
                            self.move_piece(-1, 0)
                        elif event.key == pygame.K_d:
                            self.move_piece(1, 0)
                        elif event.key == pygame.K_s:
                            if not self.move_piece(0, 1):
                                self.place_piece()
                        elif event.key == pygame.K_w:
                            self.rotate_piece()
                        elif event.key == pygame.K_SPACE:
                            self.drop_piece()
            
            self.update(dt)
            self.draw()
        
        pygame.quit()
        
        print("\nCleared Lines Dictionary:")
        print(self.cleared_lines)
        return self.cleared_lines


if __name__ == "__main__":
    game = TetrisGame()
    cleared_lines = game.run()


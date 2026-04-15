import pygame
import sys
from game import solve_puzzle_astar_generator, generate_random_board, N

def draw_board(screen, board, font, title_font, tile_size, margin, bg_color, tile_color, text_color, status_text, current_phase, button_rect):
    screen.fill(bg_color)
    
    title = title_font.render(status_text, True, text_color)
    screen.blit(title, (margin, margin))

    y_offset = 60

    for r in range(N):
        for c in range(N):
            val = board[r][c]
            if val != 0:
                pos_x = c * tile_size + (c + 1) * margin
                pos_y = r * tile_size + (r + 1) * margin + y_offset
                rect = pygame.Rect(pos_x, pos_y, tile_size, tile_size)
                
                pygame.draw.rect(screen, tile_color, rect, border_radius=10)

                text = font.render(str(val), True, text_color)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
                
    if current_phase == "IDLE":
        button_color = (46, 204, 113)
        pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
        
        button_text = title_font.render("Začni hledat řešení", True, (255, 255, 255))
        text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, text_rect)

    pygame.display.flip()

def main():
    start, x, y = generate_random_board()

    search_gen = solve_puzzle_astar_generator(start, x, y)

    pygame.init()
    
    TILE_SIZE = 100
    MARGIN = 10
    WINDOW_WIDTH = N * TILE_SIZE + (N + 1) * MARGIN
    WINDOW_HEIGHT = N * TILE_SIZE + (N + 1) * MARGIN + 130 
    
    BG_COLOR = (40, 44, 52)
    TILE_COLOR = (97, 175, 239)
    TEXT_COLOR = (255, 255, 255)
    
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("8-Puzzle (A* Visualizer)")
    font = pygame.font.Font(None, 60)
    title_font = pygame.font.Font(None, 36)

    clock = pygame.time.Clock()

    STEP_EVENT = pygame.USEREVENT + 1
    
    button_rect = pygame.Rect(MARGIN, WINDOW_HEIGHT - 60, WINDOW_WIDTH - 2 * MARGIN, 50)
    
    current_phase = "IDLE"
    solution_path = []
    step_index = 0
    current_board = start

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if current_phase == "IDLE" and button_rect.collidepoint(event.pos):
                    current_phase = "SEARCHING"

            elif event.type == STEP_EVENT and current_phase == "SHOWING_SOLUTION":
                if step_index < len(solution_path) - 1:
                    step_index += 1
                    current_board = solution_path[step_index]
                else:
                    current_phase = "DONE"
                    pygame.time.set_timer(STEP_EVENT, 0)

        if current_phase == "SEARCHING":
            STEPS_PER_FRAME = 20 
            
            for _ in range(STEPS_PER_FRAME):
                try:
                    status, data = next(search_gen)
                    if status == "SEARCHING":
                        current_board = data
                    elif status == "FOUND":
                        solution_path = data
                        current_phase = "SHOWING_SOLUTION"
                        current_board = solution_path[0]
                        pygame.time.set_timer(STEP_EVENT, 500)
                        break
                    elif status == "NOT_FOUND":
                        current_phase = "DONE"
                        break
                except StopIteration:
                    current_phase = "DONE"
                    break

        if current_phase == "IDLE":
            status_text = "Připraven. Stiskni tlačítko!"
        elif current_phase == "SEARCHING":
            status_text = "Fáze: A* hledá nejkratší cestu..."
        elif current_phase == "SHOWING_SOLUTION":
            status_text = f"Přehrávám řešení ({step_index + 1}/{len(solution_path)})"
        else:
            if solution_path:
                status_text = f"Vyřešeno! Počet tahů: {len(solution_path) - 1}"
            else:
                status_text = "Hotovo! Řešení neexistuje."

        draw_board(screen, current_board, font, title_font, TILE_SIZE, MARGIN, BG_COLOR, TILE_COLOR, TEXT_COLOR, status_text, current_phase, button_rect)
        
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
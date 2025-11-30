import pygame, sound, level, draw
currently_selecting = 1
currentle_pos_x = -99
currentle_pos_y = -99
running = True
dragging = False
admin_mode = True
rect_button_restart = None
rect_button_back = None
rect_button_solve = None
screen = None
surface_game = None
surface_game_function = None
game = None
current_game = 1

custom_map_mode = None

def initial(screen_current, surface_game_current, surface_game_function_current, game_initial):
    global screen, surface_game, surface_game_function, game,  game, custom_map_mode
    global rect_button_restart, rect_button_back, rect_button_solve, rect_button_next_level, rect_button_prev_level, rect_button_custom_map_mode
    game = game_initial
    if getattr(game, 'reset_hints', None):
        game.reset_hints()
    screen = screen_current
    surface_game = surface_game_current
    surface_game_function = surface_game_function_current
    custom_map_mode = False

    rect_button_restart = pygame.Rect(surface_game_function.get_width() - 50, 25, 50, 50)
    rect_button_back = pygame.Rect(surface_game_function.get_width() - 50, 75, 50, 50)
    rect_button_solve = pygame.Rect(surface_game_function.get_width() - 50, 125, 50, 50)
    
    rect_button_next_level = pygame.Rect(surface_game_function.get_width() - 50, 175, 50, 50)
    rect_button_prev_level = pygame.Rect(surface_game_function.get_width() - 50, 225, 50, 50)

    rect_button_custom_map_mode = pygame.Rect(surface_game_function.get_width() - 50, 275, 50, 50)


def next_game():
    global game, current_game
    game.restart_game()
    current_game = current_game + 1
    if current_game > len(level.levels):
        current_game = 1
    game = level.levels.get(current_game)
    if getattr(game, 'reset_hints', None):
        game.reset_hints()
    if game.len() == 0:
        next_game()
    draw.next_game(game)

def prev_game():
    global game, current_game
    game.restart_game()
    current_game = current_game - 1
    if current_game < 1:
        current_game = len(level.levels)
    game = level.levels.get(current_game)
    if getattr(game, 'reset_hints', None):
        game.reset_hints()
    draw.next_game(game)
    
def turn_on_custom_map_mode():
    global custom_map_mode
    custom_map_mode = not custom_map_mode

def check_win():
    global game, current_game
    if game.len() > 0 and game.get_vehicle(1).get_pos_last() == game.size_game - 1:
        print("Win")
        next_game()
def next_selecting(game):
    global currently_selecting
    currently_selecting = currently_selecting + 1
    if currently_selecting == game.len() + 1:
        currently_selecting = 1

def check_event_keyboard_game_main(surface_game, game, event):
    global dragging, admin_mode, currently_selecting, currentle_pos_x, currentle_pos_y
    # KEYBOARD
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_TAB:
            next_selecting(game)
            print(currently_selecting)

        if event.key == pygame.K_UP or event.key == pygame.K_w:
            game.move(currently_selecting,-1)
        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
            game.move(currently_selecting,1)
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            game.move(currently_selecting,-1)
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            game.move(currently_selecting, 1)
        if event.key == pygame.K_r:
            game.restart_game()
        if event.key == pygame.K_b:
            game.back_move()

        if event.key == pygame.K_c:
            for row in game.cells:
                print(row)
            print(custom_map_mode)
        if event.key == pygame.K_BACKSLASH:
            admin_mode = not admin_mode

        if admin_mode:
            if event.key == pygame.K_SLASH :
                game.solve()
            if event.key == pygame.K_COMMA :
                prev_game()

def check_event_mouse_game_main(surface_game, game, event):
    # MOUSE
    global dragging, currently_selecting, currentle_pos_x, currentle_pos_y
    unit_cell = int(surface_game.get_width()/game.size_game)
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = event.pos
        if 0 < mouse_x < surface_game.get_width() - 5 and 0 < mouse_y < surface_game.get_height() - 5:
            cell_y = mouse_x // unit_cell + 1
            cell_x = mouse_y // unit_cell + 1
            if game.cells[cell_x - 1][cell_y - 1] != 0:
                dragging = True
                currently_selecting = game.cells[cell_x - 1][cell_y - 1]
                currentle_pos_x = cell_x
                currentle_pos_y = cell_y
            print(event.pos)
            print(cell_x,cell_y)
            print(currentle_pos_x,currentle_pos_y)
    if event.type == pygame.MOUSEBUTTONUP:
        sound.play_sound_wood()
        dragging = False
    if event.type == pygame.MOUSEMOTION:
        if dragging:
            mouse_x, mouse_y = event.pos
            cell_y = mouse_x // unit_cell + 1
            cell_x = mouse_y // unit_cell + 1
            if game.vehicles.get(currently_selecting).versus > 0:
                if cell_y != currentle_pos_y:
                    game.move(currently_selecting, cell_y - currentle_pos_y)
                    currentle_pos_y = cell_y
            elif game.vehicles.get(currently_selecting).versus < 0:
                if cell_x != currentle_pos_x:
                    game.move(currently_selecting, cell_x - currentle_pos_x)
                    currentle_pos_x = cell_x

def check_event_quit(event):
    global running
    if event.type == pygame.QUIT:
                global running
                running = False

def check_event_game_function(surface_game, surface_game_function,game, event):
    global rect_button_restart, rect_button_back, rect_button_solve
    if event.type == pygame.MOUSEBUTTONDOWN:
        if rect_button_restart.collidepoint((event.pos[0] - surface_game.get_width(),event.pos[1] - 0)):
            game.restart_game()
        if rect_button_back.collidepoint((event.pos[0] - surface_game.get_width(),event.pos[1] - 0)):
            game.back_move()
        if admin_mode:
            if rect_button_solve.collidepoint((event.pos[0] - surface_game.get_width(),event.pos[1] - 0)):
                game.solve()
            if rect_button_next_level.collidepoint((event.pos[0] - surface_game.get_width(),event.pos[1] - 0)):
                next_game()
            if rect_button_prev_level.collidepoint((event.pos[0] - surface_game.get_width(),event.pos[1] - 0)):
                prev_game()
            if rect_button_custom_map_mode.collidepoint((event.pos[0] - surface_game.get_width(),event.pos[1] - 0)):
                turn_on_custom_map_mode()
        
        

def check_event():
    global surface_game,surface_game_function, game
    for event in pygame.event.get():
        check_event_quit(event)
        check_event_keyboard_game_main(surface_game, game, event)
        check_event_mouse_game_main(surface_game, game, event)
        check_event_game_function(surface_game, surface_game_function, game, event)
        

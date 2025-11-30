import pygame, color, event

pygame.init()

def initial(screen_current, surface_game_current, surface_game_function_current, game_initial):
    global screen, surface_game, surface_game_function, game
    game = game_initial
    screen = screen_current
    surface_game = surface_game_current
    surface_game_function = surface_game_function_current

    global image_grid
    image_grid = pygame.image.load("RushHour/resources/image/grid.png")

def next_game(game_current):
    global game
    game = game_current

def draw_vehicles(surface_game, game):
    unit_cell = int(surface_game.get_width()/game.size_game)
    surface_game.fill(color.colors["GREY"])
    surface_game.blit(image_grid, (0,0))
    
    # Draw white background for exit (to make hint visible)
    red_car = game.vehicles.get(1)
    if red_car and red_car.versus > 0:
        row = red_car.versus
        col = game.size_game
        exit_rect = pygame.Rect((col - 1) * unit_cell, (row - 1) * unit_cell, unit_cell, unit_cell)
        pygame.draw.rect(surface_game, color.colors["GREY"], exit_rect)
    for i in range(1, game.len() + 1):
        if game.vehicles.get(i).versus > 0:
            draw_vehicle(surface_game,unit_cell, i,((game.vehicles.get(i).versus),game.vehicles.get(i).get_pos_last()), (game.vehicles.get(i).versus, game.vehicles.get(i).get_pos_last() + game.vehicles.get(i).size - 1))
        else :
            draw_vehicle(surface_game, unit_cell, i, (game.vehicles.get(i).get_pos_last(), -game.vehicles.get(i).versus), (game.vehicles.get(i).get_pos_last() + game.vehicles.get(i).size - 1, -game.vehicles.get(i).versus))

def draw_vehicle(surface_game,unit_cell,name_vehicle, pos1, pos2):

    vehicle_rect = pygame.Rect(int((pos1[1] - 1) * unit_cell),int((pos1[0] - 1) * unit_cell),int((pos2[1] - pos1[1] + 1) * unit_cell),int((pos2[0] - pos1[0] + 1) * unit_cell))
    pygame.draw.rect(surface_game, color.colors.get(name_vehicle), vehicle_rect, border_radius= 25)

def draw_arrow(surface_game,unit_cell, pos, path_arrow):
    arrow_image = pygame.image.load(path_arrow)
    arrow_image = pygame.transform.scale(arrow_image, (unit_cell,unit_cell))
    arrow_image.set_alpha(150)
    surface_game.blit(arrow_image, (int((pos[1] - 1) * unit_cell), int((pos[0] - 1) * unit_cell)))


def draw_game_main():
    global surface_game, game
    if game.len() > 0:
        unit_cell = int(surface_game.get_width()/game.size_game)
        draw_vehicles(surface_game, game)
        draw_arrow(surface_game, unit_cell, (game.vehicles.get(1).versus, game.size_game), "RushHour/resources/image/arrow.png")
        draw_hint(surface_game, game)

def draw_hint(surface_game, game):
    solution = getattr(game, 'solution', None)
    if solution:
        vehicle_id, step = solution[0]
        vehicle = game.vehicles.get(vehicle_id)
        unit_cell = int(surface_game.get_width()/game.size_game)
        
        # Calculate new position
        new_pos_last = vehicle.get_pos_last() + step
        
        if vehicle.versus > 0:
            pos1 = (vehicle.versus, new_pos_last)
            pos2 = (vehicle.versus, new_pos_last + vehicle.size - 1)
        else:
            pos1 = (new_pos_last, -vehicle.versus)
            pos2 = (new_pos_last + vehicle.size - 1, -vehicle.versus)
            
        # Draw ghost
        vehicle_rect = pygame.Rect(int((pos1[1] - 1) * unit_cell),int((pos1[0] - 1) * unit_cell),int((pos2[1] - pos1[1] + 1) * unit_cell),int((pos2[0] - pos1[0] + 1) * unit_cell))
        
        # Create a surface for alpha blending
        # Create a surface for alpha blending
        s = pygame.Surface((vehicle_rect.width, vehicle_rect.height), pygame.SRCALPHA)
        
        # Get color and add alpha
        c = color.colors.get(vehicle_id)
        # if c is None:
        #     print(f"WARNING: Color not found for vehicle {vehicle_id}")
        #     c = (0, 0, 0) # Default to black if not found
        
        # print(f"Drawing hint for vehicle {vehicle_id} with color {c}")
        
        if len(c) == 3:
            c = (*c, 128)
        else:
            c = (c[0], c[1], c[2], 128)
            
        pygame.draw.rect(s, c, s.get_rect(), border_radius=25)
        surface_game.blit(s, (vehicle_rect.x, vehicle_rect.y))
        
    if getattr(game, 'calculating', False):
        font = pygame.font.Font(None, 36)
        text = font.render("Calculating...", True, color.colors.get("BLACK"))
        surface_game.blit(text, (10, 10))
        
        # Optional: Draw an outline or arrow to make it clearer? 
        # The ghost is good enough for now.

    

def draw_current_vehicle(surface_game_function, currrent_vehicle):
    surface_game_function.fill(color.colors.get(currrent_vehicle))

def draw_button_icon(surface_game_fuction, rect, path):
    icon = pygame.image.load(path)
    icon = pygame.transform.scale(icon, rect.size)
    surface_game_fuction.blit(icon, rect.topleft)

def draw_function_buttons(surface_game_function):
    pygame.draw.rect(surface_game_function, color.colors.get("BLUE_SKY"), event.rect_button_restart, border_radius=10)
    draw_button_icon(surface_game_function, event.rect_button_restart, "RushHour/resources/image/restart.png")
    pygame.draw.rect(surface_game_function, color.colors.get("BLUE_SKY"), event.rect_button_back, border_radius=10)
    draw_button_icon(surface_game_function, event.rect_button_back, "RushHour/resources/image/back.png")
    if event.admin_mode:
        pygame.draw.rect(surface_game_function, color.colors.get("BLUE_SKY"), event.rect_button_solve, border_radius=10)
        draw_button_icon(surface_game_function, event.rect_button_solve, "RushHour/resources/image/solve.png")
        pygame.draw.rect(surface_game_function, color.colors.get("BLUE_SKY"), event.rect_button_next_level, border_radius=10)
        draw_button_icon(surface_game_function, event.rect_button_next_level, "RushHour/resources/image/right_arrow.png")

        pygame.draw.rect(surface_game_function, color.colors.get("BLUE_SKY"), event.rect_button_prev_level, border_radius=10)
        draw_button_icon(surface_game_function, event.rect_button_prev_level, "RushHour/resources/image/left_arrow.png")

        pygame.draw.rect(surface_game_function, color.colors.get("BLUE_SKY"), event.rect_button_custom_map_mode, border_radius=10)
        draw_button_icon(surface_game_function, event.rect_button_custom_map_mode, "RushHour/resources/image/edit.png")







def draw_game_function():
    global surface_game_function
    draw_current_vehicle(surface_game_function, event.currently_selecting)
    draw_function_buttons(surface_game_function)
    
    # Draw current game number
    font = pygame.font.Font(None, 36)
    text = font.render(f"Level: {event.current_game}", True, color.colors.get("BLACK"))
    surface_game_function.blit(text, (10, 10))


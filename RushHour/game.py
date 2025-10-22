import pygame, resources
import vehicle, vehicles, color, draw, event, level, custom, sound

def main():
    pygame.init()
    clock = pygame.time.Clock()


    screen = pygame.display.set_mode((1000,800))
    pygame.display.set_caption("Rush Hour")



    surface_game = pygame.Surface((800,800))
    surface_game_x = 0
    surface_game_y = 0

    surface_game_function = pygame.Surface((200,800))
    surface_game_function_x = screen.get_width() - surface_game_function.get_width()
    surface_game_function_y = screen.get_height() - surface_game_function.get_height()
    surface_game_function.fill(color.colors.get("GREEN_PASTEL"))

    surface_game_custom = pygame.Surface((800,800))
    surface_game_custom.fill(color.colors.get("GREY"))
    surface_game_custom_function = pygame.Surface((200,800))
    surface_game_custom_function.fill(color.colors.get("GREEN_PASTEL"))



    def game_main():
        draw.draw_game_main()
        draw.draw_game_function()

        event.check_win()
        event.check_event()

        

        screen.blit(surface_game,(surface_game_x,surface_game_y))
        screen.blit(surface_game_function, (surface_game_function_x,surface_game_function_y))

    def game_custom():
        custom.draw_board()
        custom.draw_function()

        custom.check_event()

    level.import_levels_data()
    event.initial(screen, surface_game, surface_game_function, level.levels.get(1))
    draw.initial(screen, surface_game, surface_game_function, level.levels.get(1))
    custom.initial(screen, surface_game_custom, surface_game_custom_function)
    sound.play_background_music()
    while event.running:
        if not event.custom_map_mode:
            game_main()

        if event.custom_map_mode:
            game_custom()


        pygame.display.update()
        clock.tick(60)



    level.save_levels()
    print("Quited")
    pygame.quit()
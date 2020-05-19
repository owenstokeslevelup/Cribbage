import pygame

def SetUpTable(screen, height, width, col, row, background):
    
    # draw background
    screen.blit(background, (0,0))
    
    # Welcome message
    font = pygame.font.SysFont("lato", 48)
    welcome_text = font.render("Python Cottage Cribbage!!", 1, (255, 255, 255))
    text_rect = welcome_text.get_rect(center=(width/2, 30))
    screen.blit(welcome_text, text_rect)

    # load and draw the board
    board_height = 1200
    board_width = 3595
    board_ratio = board_height / board_width
    board_scale = 0.2
    the_board_pic = pygame.image.load("../assets/board.png")
    the_board_pic = pygame.transform.rotate(the_board_pic, 90)
    the_board_pic = pygame.transform.scale(the_board_pic, (int(board_width*board_scale),int(board_height*board_scale)))
    screen.blit(the_board_pic, (col, row))

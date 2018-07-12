from pygame import *
from random import *
import numpy as np
import ast

import os
import sys
import platform
sys.path.append('modules')  # Access my module folder for importing

from chess_ui import *
import chess_board as cb

if platform.system() == 'Windows':
    os.environ['SDL_VIDEODRIVER'] = 'windib'    # Ensure compatability
os.environ['SDL_VIDEO_CENTERED'] = '1'  # Centre game window

# ############################################################################ #
# #    Work in progress                                                      # #
# ############################################################################ #

def sign(x):
    if x != 0:
        return x / abs(x)
    else:
        return 0

def signToMove(x):
    if x == "white":
        return 1
    return -1

init()

screen = display.set_mode((600,600))

def reset_game():
    global game_board
    global board
    """Puts all of the pieces back"""
    board = cb.Board()
    game_board = board.board
    close_menu(win_menu)
    win_menu.event_off(5)
    win_menu.event_off(6)
    win_menu.event_off(7)
    win_menu.pressed_buttons = []

    
def select_piece(location):
    """Attempts to select the piece at location"""

    global selected,moves,captures, game_board, board
    x = location / 8
    y = location % 8

    # Notes:
    # this function is so complicated because it finds where the newly selected piece can move and capture

    # Remove illegal selections
    if game_board[x][y] == 0 or sign(game_board[x][y]) != signToMove(board.sideToMove):
        return None

    selected = location
    moves = board.legalMoves([x, y])
    game_board = board.board
    board.showBoard()
    print moves
    board_buttons[selected].event_on(5)
    return moves 

def deselect_piece():
    """Deselects the selected piece"""

    global captures,moves,selected

    if selected != None:
        board_buttons[selected].event_off(5)

        moves = []
        selected = None

def move_piece(destination):
    """Moves the selected piece"""
    global target
    target = destination
    print destination
    x = destination / 8
    y = destination % 8 
    print x
    print y
    print board.coordinates[x][y]
    print moves
    if abs(board.board[selected / 8][selected % 8]) == 1 and (x == 0 or x == 7):
        if x == 0:
            open_menu(bpromote_menu)
        else:
            open_menu(wpromote_menu)
        game_board = board.board
        return "Promoted"
    else:
        for move in moves:
            print board.coordinates[x][y] in move
        for move in moves:
            if board.coordinates[x][y] in move:
                board.makeMove(move)
                game_board = board.board
                return "Moved"
        if x == 0 or x == 7:
            if y == 2:
                board.makeMove("O-O-O")
                game_board = board.board
                return "Castled Long"
            board.makeMove("O-O")
            game_board = board.board
            return "Castled Short" 
    print "No move made!!! ERROR!!!"
    game_board = board.board  
    return False

""" Game variables """
# Notes:
# selected is a number representing where the selected piece is
# moves is a list of where the selected piece can move
# captures is a list of where the selected piece can capture
# game_board is a list of every space on the board and says what piece exists there
# turn is a number either 1 or 2 representing whose turn it is

turn = 1
wcastle = 0
bcastle = 0
selected = None
moves = []
wcaptured = []
bcaptured = []
game_board = np.zeros([8,8])
en_passent = None

""" Image Loading """
king1 = image.load("images/wking.png").convert_alpha()
king2 = image.load("images/bking.png").convert_alpha()
pawn1 = image.load("images/wpawn.png").convert_alpha()
pawn2 = image.load("images/bpawn.png").convert_alpha()
rook1 = image.load("images/wrook.png").convert_alpha()
rook2 = image.load("images/brook.png").convert_alpha()
queen1 = image.load("images/wqueen.png").convert_alpha()
queen2 = image.load("images/bqueen.png").convert_alpha()
bishop1 = image.load("images/wbishop.png").convert_alpha()
bishop2 = image.load("images/bbishop.png").convert_alpha()
knight1 = image.load("images/wknight.png").convert_alpha()
knight2 = image.load("images/bknight.png").convert_alpha()

""" Creation of game board """
# Notes:
# Event 5 represents a selected piece
# Event 6 represents a possible move for a piece
# Event 7 represents a possible capture of an enemy piece

font1 = font.Font('fonts/Alido.otf',18)
font2 = font.Font('fonts/LCALLIG.TTF',36)

win_bg = Surface((250,90))
win_bg.fill((0,0,0))
draw.rect(win_bg,(255,255,255),(5,5,240,80))

layer_hunter = Surface((50,50))
layer_hunter.fill((63,122,77))
layer_skyblue = Surface((50,50))
layer_skyblue.fill((230,230,250))
layer_hovered = Surface((50,50))
layer_hovered.fill((0,0,255))
layer_selected = Surface((50,50))
layer_selected.fill((0,255,0))
layer_is_move = Surface((50,50),SRCALPHA)
layer_is_move.fill((0,0,255,85))
layer_is_capture = Surface((50,50))
layer_is_capture.fill((255,0,0))

new_bg = Surface((100,20))
new_bg.fill((255,0,0))
new_bg2 = Surface((100,20))
new_bg2.fill((0,0,255))

promote_layer = Surface((120,120))
promote_layer.fill((255,255,255))
draw.rect(promote_layer,(0,0,0),(5,5,110,110))
draw.rect(promote_layer,(255,255,255),(10,10,100,100))
draw.line(promote_layer,(0,0,0),(10,60),(110,60),5)
draw.line(promote_layer,(0,0,0),(60,10),(60,110),5)

# In-game GUI
game_menu = make_menu((0,0,800,800),'game',0)
open_menu(game_menu)

board_buttons = [Button((100+(i%8)*50,450-(i//8)*50,50,50),i,(0,)) for i in range(64)]

for i in range(64):
    if (i+i//8)%2 == 0:
        board_buttons[i].add_layer(layer_hunter,(0,0),(0,))
    else:
        board_buttons[i].add_layer(layer_skyblue,(0,0),(0,))

new_game = Button((2,2,50,20),'new',(0,))
new_game.add_layer(new_bg,(0,0),(2,))
new_game.add_text("Reset",font1,(0,0,0),(25,10),1,0,(0,))

undo_move = Button((2,50,50,20),'undo',(0,))
undo_move.add_layer(new_bg,(0,0),(2,))
undo_move.add_text("Undo",font1,(0,0,0),(25,10),1,0,(0,))

quit_button = Button((548,2,50,20),'quit',(0,))
quit_button.add_layer(new_bg,(0,0),(2,))
quit_button.add_text("Quit",font1,(0,0,0),(25,10),1,0,(0,))

add_layer_multi(layer_hovered,(0,0),(2,-5,-6,-7),board_buttons)
add_layer_multi(layer_selected,(0,0),(5,),board_buttons)
add_layer_multi(layer_is_move,(0,0),(-5,6,-7),board_buttons)
add_layer_multi(layer_is_capture,(0,0),(-5,7),board_buttons)

add_objects(game_menu,board_buttons)
#add_objects(game_menu,(new_game, quit_button, undo_move))

# Win menu

win_menu = make_menu((175,270,250,90),'win',1)
win_menu.add_layer(win_bg,(0,0),(5,6,7))
win_menu.add_text("White wins!",font2,(0,0,0),(125,30),1,0,(5,))
win_menu.add_text("Black wins!",font2,(0,0,0),(125,30),1,0,(6,))
win_menu.add_text("Draw!",font2,(0,0,0),(125,30),1,0,(7,))
new_game2 = Button((10,60,100,20),'new',(0,))
new_game2.add_layer(new_bg,(0,0),(2,))
new_game2.add_layer(new_bg2,(0,0),(0,-2))
new_game2.add_text("New Game",font1,(255,255,255),(50,10),1,0,(0,))
win_menu.add_object(new_game2)
quit2 = Button((180,60,50,20),'quit',(0,))
quit2.add_layer(new_bg,(0,0),(2,))
quit2.add_layer(new_bg2,(0,0),(0,-2))
quit2.add_text("Quit",font1,(255,255,255),(25,10),1,0,(0,))
win_menu.add_object(quit2)      





# Promotion menus
wqueen_btn = Button((10,10,50,50),'Q',(0,))
wknight_btn = Button((60,10,50,50),'N',(0,))
wrook_btn = Button((10,60,50,50),'R',(0,))
wbishop_btn = Button((60,60,50,50),'B',(0,))

bqueen_btn = Button((10,10,50,50),'Q',(0,))
bknight_btn = Button((60,10,50,50),'N',(0,))
brook_btn = Button((10,60,50,50),'R',(0,))
bbishop_btn = Button((60,60,50,50),'B',(0,))

add_layer_multi(layer_hovered,(0,0),(2,),(wqueen_btn,wknight_btn,wrook_btn,wbishop_btn,
                                          bqueen_btn,bknight_btn,brook_btn,bbishop_btn))

wqueen_btn.add_layer(queen1,(0,0),(0,))
wrook_btn.add_layer(rook1,(0,0),(0,))
wknight_btn.add_layer(knight1,(0,0),(0,))
wbishop_btn.add_layer(bishop1,(0,0),(0,))
bqueen_btn.add_layer(queen2,(0,0),(0,))
brook_btn.add_layer(rook2,(0,0),(0,))
bknight_btn.add_layer(knight2,(0,0),(0,))
bbishop_btn.add_layer(bishop2,(0,0),(0,))

wpromote_menu = make_menu((240,240,120,120),'wpromote',1)
wpromote_menu.add_layer(promote_layer,(0,0),(0,))
add_objects(wpromote_menu,(wqueen_btn,wknight_btn,wrook_btn,wbishop_btn))

bpromote_menu = make_menu((240,240,120,120),'bpromote',1)
bpromote_menu.add_layer(promote_layer,(0,0),(0,))
add_objects(bpromote_menu,(bqueen_btn,bknight_btn,brook_btn,bbishop_btn))

reset_game()
 


""" Main Loop """
# Notes:
# My loops run in three main steps:
#   1. Get inputs for each menu along with general inputs
#   2. Handle inputs for each menu and update all running systems
#   3. Draw all of the objects to the screen for each menu
#
# Using my menuing system I'm able to easily organize every GUI including the
# main game itself into these three steps.

play_or_replay = raw_input("Would you like to play or replay a game? ")
print play_or_replay

if play_or_replay == 'replay':
    forward = Button((2,100,50,20),'fwd',(0,))
    forward.add_layer(new_bg,(0,0),(2,))
    forward.add_text("Forward",font1,(0,0,0),(25,10),1,0,(0,))
    backward = Button((2,150,50,20),'bwd',(0,))
    backward.add_layer(new_bg,(0,0),(2,))
    backward.add_text("Back",font1,(0,0,0),(25,10),1,0,(0,))
    add_objects(game_menu,(quit_button, backward, forward))
    file_or_string = raw_input("Would you like to replay from file or string? ")
    if file_or_string == 'string':
        move_list = raw_input("Give game as list: ")
        move_list = ast.literal_eval(move_list)
        print move_list
    else:
        with open(file_or_string, 'r+') as file:
            game_file = file.read()
        game_file = ast.literal_eval(game_file)
        game_keys = game_file.keys()
        print "Available games: " + str(min(game_keys)) + " through " + str(max(game_keys))
        game_key = raw_input("Choose game: ")
        try:
            move_list = game_file[game_key]
        except:
            move_list = game_file[int(game_key)]
        print move_list
    running = 1
    current_move = 0
    while running:
        
        """ STEP 1: Get inputs """
        chars = ''
        for evnt in event.get():
            if evnt.type == QUIT:
                running = 0
            elif evnt.type == KEYDOWN:
                if evnt.key == K_ESCAPE:
                    running = 0
                else:
                    chars += evnt.unicode

        lc,rc = mouse.get_pressed()[0:2]
        mx,my = mouse.get_pos()

        """ STEP 2: Handle inputs / update menus """

        update_menus(mx,my,lc,chars)


        if is_menu_open(game_menu):
            # Handle the game board and game menu
            for c in game_menu.get_pressed():
                if c == 'quit':   # Exit game button
                    running = 0
                elif c == 'fwd':
                    if current_move < len(move_list):
                        board.makeMove(move_list[current_move])
                        current_move += 1
                    game_board = board.board
                    #continue
                elif c == 'bwd':
                    if current_move > 0:
                        board.undoMove()
                        current_move -= 1
                    game_board = board.board
                    #continue
        update_menu_images()
        game_board = board.board
        for i in range(64):
            x = i / 8
            y = i % 8
            if game_board[x][y] == 0:
                continue
            elif game_board[x][y] == 1:
                game_menu.blit(pawn1,(100+(i%8)*50,450-(i//8)*50))
            elif game_board[x][y] == -1:
                game_menu.blit(pawn2,(100+(i%8)*50,450-(i//8)*50))
            elif game_board[x][y] == 6:
                game_menu.blit(king1,(100+(i%8)*50,450-(i//8)*50))
            elif game_board[x][y] == -6:
                game_menu.blit(king2,(100+(i%8)*50,450-(i//8)*50))
            elif game_board[x][y] == 5:
                game_menu.blit(queen1,(100+(i%8)*50,450-(i//8)*50))
            elif game_board[x][y] == -5:
                game_menu.blit(queen2,(100+(i%8)*50,450-(i//8)*50))
            elif game_board[x][y] == 4:
                game_menu.blit(rook1,(100+(i%8)*50,450-(i//8)*50))
            elif game_board[x][y] == -4:
                game_menu.blit(rook2,(100+(i%8)*50,450-(i//8)*50))
            elif game_board[x][y] == 3:
                game_menu.blit(bishop1,(100+(i%8)*50,450-(i//8)*50))
            elif game_board[x][y] == -3:
                game_menu.blit(bishop2,(100+(i%8)*50,450-(i//8)*50))
            elif game_board[x][y] == 2:
                game_menu.blit(knight1,(100+(i%8)*50,450-(i//8)*50))
            elif game_board[x][y] == -2:
                game_menu.blit(knight2,(100+(i%8)*50,450-(i//8)*50))

        screen.fill((255,255,255))
        draw.rect(screen,(0,0,0),(50,50,500,500))
        draw.rect(screen,(255,255,255),(100,100,400,400))
        draw_menus(screen)

        display.flip()
        time.wait(10)
else:

    opponent = raw_input("Would you like to play against AI or another player? ")
    if opponent == 'player':

        add_objects(game_menu,(new_game, quit_button, undo_move))




        running = 1
        while running:  
            """ STEP 1: Get inputs """
            chars = ''
            for evnt in event.get():
                if evnt.type == QUIT:
                    running = 0
                elif evnt.type == KEYDOWN:
                    if evnt.key == K_ESCAPE:
                        running = 0
                    else:
                        chars += evnt.unicode

            lc,rc = mouse.get_pressed()[0:2]
            mx,my = mouse.get_pos()

            """ STEP 2: Handle inputs / update menus """

            update_menus(mx,my,lc,chars)

            if is_menu_open(wpromote_menu):  # Promotion menus
                for i in wpromote_menu.get_pressed():   # Check selection
                    print "Menu returned " + str(i)
                    print str(target % 8)
                    print moves
                    close_menu(wpromote_menu)
                    for move in moves:
                        print move
                        print i
                        print board.coordinates[target / 8][target % 8]
                        print move.replace('+','').endswith(i)
                        print board.coordinates[target / 8][target % 8] in move
                        if move.replace('+','').endswith(i) and board.coordinates[target / 8][target % 8] in move:
                            board.makeMove(move)
                    deselect_piece()
                    game_over = board.gameOver() 
                    if game_over == "white":
                            open_menu(win_menu)
                            win_menu.event_on(5)
                    elif game_over == "black":
                        open_menu(win_menu)
                        win_menu.event_on(6)
                    elif game_over:
                        open_menu(win_menu)
                        win_menu.event_on(7)
            if  is_menu_open(bpromote_menu):
                for i in bpromote_menu.get_pressed():   # Check selection
                    print "Menu returned " + str(i)
                    print str(target % 8)
                    close_menu(bpromote_menu)
                    for move in moves:
                        print move
                        print i
                        print board.coordinates[target / 8][target % 8]
                        print move.replace('+','').endswith(i)
                        print board.coordinates[target / 8][target % 8] in move
                        if move.replace('+','').endswith(i) and board.coordinates[target / 8][target % 8] in move:
                            board.makeMove(move)
                    deselect_piece()
                    game_over = board.gameOver() 
                    if game_over == "white":
                            open_menu(win_menu)
                            win_menu.event_on(5)
                    elif game_over == "black":
                        open_menu(win_menu)
                        win_menu.event_on(6)
                    elif game_over:
                        open_menu(win_menu)
                        win_menu.event_on(7)


            elif is_menu_open(game_menu):
                # Handle the game board and game menu
                for c in game_menu.get_pressed():
                    if c == 'new':      # Reset game button
                        reset_game()
                    elif c == 'quit':   # Exit game button
                        running = 0
                    elif c == 'undo':
                        board.undoMove()
                        game_board = board.board
                        continue
                    else:
                        if selected == None:    # Select piece that was clicked on
                            print "Valitaan " + str(c)
                            select_piece(c)
                        else:
                            if selected == c:   # Deselect currently selected piece
                                print "Poistetaan valinta " + str(c)
                                deselect_piece()
                            else:
                                if not move_piece(c):
                                    deselect_piece()
                                    select_piece(c)
                                if not is_menu_open(wpromote_menu) and not is_menu_open(bpromote_menu):
                                    deselect_piece()
                                    game_over = board.gameOver() 
                                    if game_over == "white":
                                            open_menu(win_menu)
                                            win_menu.event_on(5)
                                    elif game_over == "black":
                                        open_menu(win_menu)
                                        win_menu.event_on(6)
                                    elif game_over:
                                        open_menu(win_menu)
                                        win_menu.event_on(7)
                                else:
                                    break


            if is_menu_open(win_menu):
                for i in win_menu.get_pressed():
                    if i == 'quit':
                        running = 0
                    elif i == 'new':
                        reset_game()
                    elif i == 'undo':
                        board.undoMove()

            """ STEP 3: Draw menus """

            update_menu_images()

            if is_menu_open(game_menu):
                """
                # Show which pieces are captured
                i = 0
                p = 0
                for piece in wcaptured:
                    if piece == "P":
                        if p == 0:
                            game_menu.blit(pawn2,(0,50))
                        p += 1
                    else:
                        i += 50
                    if piece == "B": game_menu.blit(bishop2,(0,50+i))
                    if piece == "N": game_menu.blit(knight2,(0,50+i))
                    if piece == "R": game_menu.blit(rook2,(0,50+i))
                    if piece == "Q": game_menu.blit(queen2,(0,50+i))
                if p != 0:
                    msg = font1.render(str(p),1,(255,255,255))
                    game_menu.blit(msg,(20,68))

                i = 0
                p = 0
                for piece in bcaptured:
                    if piece == "P":
                        if p == 0:
                            game_menu.blit(pawn1,(550,50))
                        p += 1
                    else:
                        i += 50
                    if piece == "B": game_menu.blit(bishop1,(550,50+i))
                    if piece == "N": game_menu.blit(knight1,(550,50+i))
                    if piece == "R": game_menu.blit(rook1,(550,50+i))
                    if piece == "Q": game_menu.blit(queen1,(550,50+i))
                if p != 0:
                    msg = font1.render(str(p),1,(0,0,0))
                    game_menu.blit(msg,(570,68))
                """
                # Draw the pieces on the game board
                game_board = board.board
                for i in range(64):
                    x = i / 8
                    y = i % 8
                    if game_board[x][y] == 0:
                        continue
                    elif game_board[x][y] == 1:
                        game_menu.blit(pawn1,(100+(i%8)*50,450-(i//8)*50))
                    elif game_board[x][y] == -1:
                        game_menu.blit(pawn2,(100+(i%8)*50,450-(i//8)*50))
                    elif game_board[x][y] == 6:
                        game_menu.blit(king1,(100+(i%8)*50,450-(i//8)*50))
                    elif game_board[x][y] == -6:
                        game_menu.blit(king2,(100+(i%8)*50,450-(i//8)*50))
                    elif game_board[x][y] == 5:
                        game_menu.blit(queen1,(100+(i%8)*50,450-(i//8)*50))
                    elif game_board[x][y] == -5:
                        game_menu.blit(queen2,(100+(i%8)*50,450-(i//8)*50))
                    elif game_board[x][y] == 4:
                        game_menu.blit(rook1,(100+(i%8)*50,450-(i//8)*50))
                    elif game_board[x][y] == -4:
                        game_menu.blit(rook2,(100+(i%8)*50,450-(i//8)*50))
                    elif game_board[x][y] == 3:
                        game_menu.blit(bishop1,(100+(i%8)*50,450-(i//8)*50))
                    elif game_board[x][y] == -3:
                        game_menu.blit(bishop2,(100+(i%8)*50,450-(i//8)*50))
                    elif game_board[x][y] == 2:
                        game_menu.blit(knight1,(100+(i%8)*50,450-(i//8)*50))
                    elif game_board[x][y] == -2:
                        game_menu.blit(knight2,(100+(i%8)*50,450-(i//8)*50))

            screen.fill((255,255,255))
            draw.rect(screen,(0,0,0),(50,50,500,500))
            draw.rect(screen,(255,255,255),(100,100,400,400))
            draw_menus(screen)

            display.flip()
            time.wait(10)

    else:
        add_objects(game_menu,(new_game, quit_button, undo_move))

        #Load engine here


        running = 1
        while running:  
            """ STEP 1: Get inputs """
            chars = ''
            for evnt in event.get():
                if evnt.type == QUIT:
                    running = 0
                elif evnt.type == KEYDOWN:
                    if evnt.key == K_ESCAPE:
                        running = 0
                    else:
                        chars += evnt.unicode

            if board.sideToMove == "black":
                moves = board.legalMoves()
                if len(moves) > 0:
                    move = randint(0, len(moves)-1)
                    board.makeMove(moves[move])
                    game_board = board.board

            lc,rc = mouse.get_pressed()[0:2]
            mx,my = mouse.get_pos()

            """ STEP 2: Handle inputs / update menus """

            update_menus(mx,my,lc,chars)

            if is_menu_open(wpromote_menu):  # Promotion menus
                for i in wpromote_menu.get_pressed():   # Check selection
                    print "Menu returned " + str(i)
                    print str(target % 8)
                    print moves
                    close_menu(wpromote_menu)
                    for move in moves:
                        print move
                        print i
                        print board.coordinates[target / 8][target % 8]
                        print move.replace('+','').endswith(i)
                        print board.coordinates[target / 8][target % 8] in move
                        if move.replace('+','').endswith(i) and board.coordinates[target / 8][target % 8] in move:
                            board.makeMove(move)
                    deselect_piece()
                    game_over = board.gameOver() 
                    if game_over == "white":
                            open_menu(win_menu)
                            win_menu.event_on(5)
                    elif game_over == "black":
                        open_menu(win_menu)
                        win_menu.event_on(6)
                    elif game_over:
                        open_menu(win_menu)
                        win_menu.event_on(7)
            if  is_menu_open(bpromote_menu):
                for i in bpromote_menu.get_pressed():   # Check selection
                    print "Menu returned " + str(i)
                    print str(target % 8)
                    close_menu(bpromote_menu)
                    for move in moves:
                        print move
                        print i
                        print board.coordinates[target / 8][target % 8]
                        print move.replace('+','').endswith(i)
                        print board.coordinates[target / 8][target % 8] in move
                        if move.replace('+','').endswith(i) and board.coordinates[target / 8][target % 8] in move:
                            board.makeMove(move)
                    deselect_piece()
                    game_over = board.gameOver() 
                    if game_over == "white":
                            open_menu(win_menu)
                            win_menu.event_on(5)
                    elif game_over == "black":
                        open_menu(win_menu)
                        win_menu.event_on(6)
                    elif game_over:
                        open_menu(win_menu)
                        win_menu.event_on(7)


            elif is_menu_open(game_menu):
                # Handle the game board and game menu
                for c in game_menu.get_pressed():
                    if c == 'new':      # Reset game button
                        reset_game()
                    elif c == 'quit':   # Exit game button
                        running = 0
                    elif c == 'undo':
                        board.undoMove()
                        game_board = board.board
                        continue
                    else:
                        if selected == None:    # Select piece that was clicked on
                            print "Valitaan " + str(c)
                            select_piece(c)
                        else:
                            if selected == c:   # Deselect currently selected piece
                                print "Poistetaan valinta " + str(c)
                                deselect_piece()
                            else:
                                if not move_piece(c):
                                    deselect_piece()
                                    select_piece(c)
                                if not is_menu_open(wpromote_menu) and not is_menu_open(bpromote_menu):
                                    deselect_piece()
                                    game_over = board.gameOver() 
                                    if game_over == "white":
                                            open_menu(win_menu)
                                            win_menu.event_on(5)
                                    elif game_over == "black":
                                        open_menu(win_menu)
                                        win_menu.event_on(6)
                                    elif game_over:
                                        open_menu(win_menu)
                                        win_menu.event_on(7)
                                else:
                                    break


            if is_menu_open(win_menu):
                for i in win_menu.get_pressed():
                    if i == 'quit':
                        running = 0
                    elif i == 'new':
                        reset_game()
                    elif i == 'undo':
                        board.undoMove()

            """ STEP 3: Draw menus """

            update_menu_images()

            if is_menu_open(game_menu):
                """
                # Show which pieces are captured
                i = 0
                p = 0
                for piece in wcaptured:
                    if piece == "P":
                        if p == 0:
                            game_menu.blit(pawn2,(0,50))
                        p += 1
                    else:
                        i += 50
                    if piece == "B": game_menu.blit(bishop2,(0,50+i))
                    if piece == "N": game_menu.blit(knight2,(0,50+i))
                    if piece == "R": game_menu.blit(rook2,(0,50+i))
                    if piece == "Q": game_menu.blit(queen2,(0,50+i))
                if p != 0:
                    msg = font1.render(str(p),1,(255,255,255))
                    game_menu.blit(msg,(20,68))

                i = 0
                p = 0
                for piece in bcaptured:
                    if piece == "P":
                        if p == 0:
                            game_menu.blit(pawn1,(550,50))
                        p += 1
                    else:
                        i += 50
                    if piece == "B": game_menu.blit(bishop1,(550,50+i))
                    if piece == "N": game_menu.blit(knight1,(550,50+i))
                    if piece == "R": game_menu.blit(rook1,(550,50+i))
                    if piece == "Q": game_menu.blit(queen1,(550,50+i))
                if p != 0:
                    msg = font1.render(str(p),1,(0,0,0))
                    game_menu.blit(msg,(570,68))
                """
                # Draw the pieces on the game board
                game_board = board.board
                for i in range(64):
                    x = i / 8
                    y = i % 8
                    if game_board[x][y] == 0:
                        continue
                    elif game_board[x][y] == 1:
                        game_menu.blit(pawn1,(100+(i%8)*50,450-(i//8)*50))
                    elif game_board[x][y] == -1:
                        game_menu.blit(pawn2,(100+(i%8)*50,450-(i//8)*50))
                    elif game_board[x][y] == 6:
                        game_menu.blit(king1,(100+(i%8)*50,450-(i//8)*50))
                    elif game_board[x][y] == -6:
                        game_menu.blit(king2,(100+(i%8)*50,450-(i//8)*50))
                    elif game_board[x][y] == 5:
                        game_menu.blit(queen1,(100+(i%8)*50,450-(i//8)*50))
                    elif game_board[x][y] == -5:
                        game_menu.blit(queen2,(100+(i%8)*50,450-(i//8)*50))
                    elif game_board[x][y] == 4:
                        game_menu.blit(rook1,(100+(i%8)*50,450-(i//8)*50))
                    elif game_board[x][y] == -4:
                        game_menu.blit(rook2,(100+(i%8)*50,450-(i//8)*50))
                    elif game_board[x][y] == 3:
                        game_menu.blit(bishop1,(100+(i%8)*50,450-(i//8)*50))
                    elif game_board[x][y] == -3:
                        game_menu.blit(bishop2,(100+(i%8)*50,450-(i//8)*50))
                    elif game_board[x][y] == 2:
                        game_menu.blit(knight1,(100+(i%8)*50,450-(i//8)*50))
                    elif game_board[x][y] == -2:
                        game_menu.blit(knight2,(100+(i%8)*50,450-(i//8)*50))

            screen.fill((255,255,255))
            draw.rect(screen,(0,0,0),(50,50,500,500))
            draw.rect(screen,(255,255,255),(100,100,400,400))
            draw_menus(screen)

            display.flip()
            time.wait(10)    

quit()
import pygame as py
import asyncio
import game
import moves
import sys
from multiprocessing import Process, Queue
from const import *


def loadPieces():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = py.transform.scale(py.image.load("images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE)) 


async def main():
    py.init()
    py.display.set_caption('AI Chess Program (White) - Vasishta Malisetty')
    screen = py.display.set_mode((BOARD_WIDTH + NOTATION_PANEL_WIDTH, BOARD_HEIGHT))
    clock = py.time.Clock()
    game_state = game.Game()
    valid_moves = game_state.getValidMoves()
    move_made = False  
    animate = False  
    loadPieces()  
    running = True
    square_selected = ()  
    player_clicks = []  
    game_over = False
    ai_thinking = False
    move_undone = False
    move_finder_process = None
    notation_font = py.font.SysFont("Times New Roman", 16, False, False)

    
    player_one = True
    player_two = False 

    
    global x 
    x = "beige" 
    global y 
    y = "dark olive green"

    while running:
        human_turn = (game_state.white_to_move and player_one) or (not game_state.white_to_move and player_two)
        for e in py.event.get():
            if e.type == py.QUIT:
                py.quit()
                sys.exit()
           
            elif e.type == py.MOUSEBUTTONDOWN:
                if not game_over:
                    location = py.mouse.get_pos()  
                    col = location[0] // SQUARE_SIZE
                    row = location[1] // SQUARE_SIZE
                    if square_selected == (row, col) or col >= 8:  
                        square_selected = ()  
                        player_clicks = []  
                    else:
                        square_selected = (row, col)
                        player_clicks.append(square_selected)  
                    if len(player_clicks) == 2 and human_turn:  
                        move = game.Move(player_clicks[0], player_clicks[1], game_state.board)
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                game_state.makeMove(valid_moves[i])
                                move_made = True
                                animate = True
                                square_selected = ()  
                                player_clicks = []
                        if not move_made:
                            player_clicks = [square_selected]

           
            elif e.type == py.KEYDOWN:
                if e.key == py.K_u:  
                    game_state.undoMove()
                    move_made = True
                    animate = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True
                if e.key == py.K_r:  
                    game_state = game.Game()
                    valid_moves = game_state.getValidMoves()
                    square_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    game_over = False
                    player_one = True 
                    player_two = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True
                if e.key == py.K_b:
                    py.display.set_caption('AI Chess Program (Black) - Vasishta Malisetty')
                    game_state = game.Game()
                    valid_moves = game_state.getValidMoves()
                    square_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    game_over = False
                    player_one = False 
                    player_two = True
                if e.key == py.K_w:
                    py.display.set_caption('AI Chess Program (White) - Vasishta Malisetty')
                    game_state = game.Game()
                    valid_moves = game_state.getValidMoves()
                    square_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    game_over = False
                    player_one = True 
                    player_two = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True
                if e.key == py.K_p:
                    py.display.set_caption('AI Chess Program (PvP) - Vasishta Malisetty')
                    game_state = game.Game()
                    valid_moves = game_state.getValidMoves()
                    square_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    game_over = False
                    player_one = True 
                    player_two = True
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True
                if e.key == py.K_1:
                    x = "white"
                    y = "dark blue"
                if e.key == py.K_2:
                    x = "white"
                    y = "gray"
                if e.key == py.K_3:
                    x = "brown"
                    y = "beige"
                if e.key == py.K_4:
                    x = "beige"
                    y = "dark olive green"
                if e.key == py.K_f:
                    pass

        if not game_over and not human_turn and not move_undone:
            if not ai_thinking:
                ai_thinking = True
                return_queue = Queue()  
                move_finder_process = Process(target=moves.findBestMove, args=(game_state, valid_moves, return_queue))
                move_finder_process.start()

            if not move_finder_process.is_alive():
                ai_move = return_queue.get()
                if ai_move is None:
                    ai_move = moves.findRandomMove(valid_moves)
                game_state.makeMove(ai_move)
                move_made = True
                animate = True
                ai_thinking = False

        if move_made:
            if animate:
                animateMove(game_state.notation[-1], screen, game_state.board, clock)
            valid_moves = game_state.getValidMoves()
            move_made = False
            animate = False
            move_undone = False

        drawGameState(screen, game_state, valid_moves, square_selected)

        if not game_over:
            drawMoveLog(screen, game_state, notation_font)

        if game_state.checkmate:
            game_over = True
            if game_state.white_to_move:
                drawEndGameText(screen, "Black wins by checkmate")
            else:
                drawEndGameText(screen, "White wins by checkmate")

        elif game_state.stalemate:
            game_over = True
            drawEndGameText(screen, "Stalemate")

        clock.tick(MAX_FPS)
        py.display.flip()
        await asyncio.sleep(0)


def drawGameState(screen, game_state, valid_moves, square_selected):
    """
    Responsible for all the graphics within current game state.
    """
    drawBoard(screen)  
    highlightSquares(screen, game_state, valid_moves, square_selected)
    drawPieces(screen, game_state.board)  


def drawBoard(screen):
    """
    Draw the squares on the board.
    The top left square is always light.
    """
    global colors
    colors = [py.Color(x), py.Color(y)]
    for row in range(NUM_ROWS):
        for column in range(NUM_COLS):
            color = colors[((row + column) % 2)]
            py.draw.rect(screen, color, py.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def highlightSquares(screen, game_state, valid_moves, square_selected):
    """
    Highlight square selected and moves for piece selected.
    """
    if (len(game_state.notation)) > 0:
        last_move = game_state.notation[-1]
        s = py.Surface((SQUARE_SIZE, SQUARE_SIZE))
        s.set_alpha(100)
        s.fill(py.Color('green'))
        screen.blit(s, (last_move.end_col * SQUARE_SIZE, last_move.end_row * SQUARE_SIZE))
    if square_selected != ():
        row, col = square_selected
        if game_state.board[row][col][0] == (
                'w' if game_state.white_to_move else 'b'):  
           
            s = py.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100)  
            s.fill(py.Color('blue'))
            screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            s.fill(py.Color('yellow'))
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    screen.blit(s, (move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE))


def drawPieces(screen, board):
    for row in range(NUM_ROWS):
        for column in range(NUM_COLS):
            piece = board[row][column]
            if piece != "--":
                screen.blit(IMAGES[piece], py.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def drawMoveLog(screen, game_state, font):
    notation_rect = py.Rect(BOARD_WIDTH, 0, NOTATION_PANEL_WIDTH, NOTATION_PANEL_HEIGHT)
    py.draw.rect(screen, py.Color('white'), notation_rect)
    notation = game_state.notation
    move_texts = []
    for i in range(0, len(notation), 2):
        move_string = str(i // 2 + 1) + '. ' + str(notation[i]) + " "
        if i + 1 < len(notation):
            move_string += str(notation[i + 1]) + "  "
        move_texts.append(move_string)

    moves_per_row = 3
    padding = 5
    line_spacing = 2
    text_y = padding
    for i in range(0, len(move_texts), moves_per_row):
        text = ""
        for j in range(moves_per_row):
            if i + j < len(move_texts):
                text += move_texts[i + j]

        text_object = font.render(text, True, py.Color('black'))
        text_location = notation_rect.move(padding, text_y)
        screen.blit(text_object, text_location)
        text_y += text_object.get_height() + line_spacing


def drawEndGameText(screen, text):
    font = py.font.SysFont("Helvetica", 32, True, False)
    text_object = font.render(text, False, py.Color("gray"))
    text_location = py.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - text_object.get_width() / 2,
                                                                 BOARD_HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, False, py.Color('black'))
    screen.blit(text_object, text_location.move(2, 2))


def animateMove(move, screen, board, clock):
    """
    Animating a move
    """
    global colors
    d_row = move.end_row - move.start_row
    d_col = move.end_col - move.start_col
    frames_per_square = 10  
    frame_count = (abs(d_row) + abs(d_col)) * frames_per_square
    for frame in range(frame_count + 1):
        row, col = (move.start_row + d_row * frame / frame_count, move.start_col + d_col * frame / frame_count)
        drawBoard(screen)
        drawPieces(screen, board)
        
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = py.Rect(move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        py.draw.rect(screen, color, end_square)
        
        if move.piece_captured != '--':
            if move.is_enpassant_move:
                enpassant_row = move.end_row + 1 if move.piece_captured[0] == 'b' else move.end_row - 1
                end_square = py.Rect(move.end_col * SQUARE_SIZE, enpassant_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            screen.blit(IMAGES[move.piece_captured], end_square)
        
        screen.blit(IMAGES[move.piece_moved], py.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        py.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    asyncio.run( main() )

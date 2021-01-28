import pygame as p
import ChessEngine

WIDTH = 704
HEIGHT = 768
DIMENSION = 12
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ['bG', 'bB', 'bT', 'bD', 'bC', 'bP', 'bF', 'bL', 'bK', 'bH', 'bS',
              'rG', 'rB', 'rT', 'rD', 'rC', 'rP', 'rF', 'rL', 'rK', 'rH', 'rS']
    grids = ['TLconner', 'Lconner', 'BLconner', 'Tconner1', 'Tconner2', 'Tconner3', 'TRconner']
    for grid in grids:
        IMAGES[grid] = p.transform.scale(p.image.load("images/titles/" + grid + ".png"), (SQ_SIZE, SQ_SIZE))
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/pieces/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('White'))
    gs = ChessEngine.GameState()
    loadImages()
    validMoves = gs.getValidMoves()
    moveMade = False #flag for when a move is made

    running = True
    sqSelected = () #(row, col)
    playerClicks = [] #[(6, 4), (4, 4)]

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE

                if len(playerClicks) == 0 and gs.validPiece(row, col):
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                elif len(playerClicks) == 1:
                    if sqSelected == (row, col): #player clicked the same square twice
                        sqSelected == () #deselect
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)

                if len(playerClicks) == 2: #after 2nd click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = ()
                    playerClicks = []

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs):
    drawBoard(screen)
    #drawGrid(screen)
    drawImgGrid(screen)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    for r in range(DIMENSION):
        for c in range(DIMENSION-1):
            p.draw.rect(screen, p.Color('white'), p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawGrid(screen):
    for r in range(DIMENSION):
        for c in range(DIMENSION-1):
            if c == 0:
                p.draw.line(screen, p.Color('brown'), (c * SQ_SIZE + SQ_SIZE // 2, r * SQ_SIZE + SQ_SIZE // 2), ((c + 1) * SQ_SIZE, r * SQ_SIZE + SQ_SIZE // 2), 1)
            elif c == 10:
                p.draw.line(screen, p.Color('brown'), (c * SQ_SIZE, r * SQ_SIZE + SQ_SIZE // 2), (c * SQ_SIZE + SQ_SIZE // 2, r * SQ_SIZE + SQ_SIZE // 2), 1)
            else:
                p.draw.line(screen, p.Color('brown'), (c * SQ_SIZE, r * SQ_SIZE + SQ_SIZE // 2), ((c + 1) * SQ_SIZE, r * SQ_SIZE + SQ_SIZE // 2), 1)

    for c in range(DIMENSION-1):
        for r in range(DIMENSION):
            if r == 0:
                p.draw.line(screen, p.Color('brown'), (c * SQ_SIZE + SQ_SIZE // 2, r * SQ_SIZE + SQ_SIZE // 2), (c * SQ_SIZE + SQ_SIZE // 2, (r + 1) * SQ_SIZE), 1)
            elif r == 11:
                p.draw.line(screen, p.Color('brown'), (c * SQ_SIZE + SQ_SIZE // 2, r * SQ_SIZE + SQ_SIZE // 2), (c * SQ_SIZE + SQ_SIZE // 2, r * SQ_SIZE), 1)
            else:
                p.draw.line(screen, p.Color('brown'), (c * SQ_SIZE + SQ_SIZE // 2, r * SQ_SIZE), (c * SQ_SIZE + SQ_SIZE // 2, (r + 1) * SQ_SIZE), 1)

def drawImgGrid(screen):
    for r in range(DIMENSION):
        for c in range(DIMENSION-1):
            if r == 0 and c == 0:
                screen.blit(IMAGES['TLconner'], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            elif r == DIMENSION - 1 and c == 0:
                screen.blit(IMAGES['BLconner'], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            elif c == 0:
                screen.blit(IMAGES['Lconner'], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            elif r == 0 and c == 1:
                screen.blit(IMAGES['Tconner1'], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            elif r == 0 and c == 2:
                screen.blit(IMAGES['Tconner2'], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            elif r == 0 and c == DIMENSION - 2:
                screen.blit(IMAGES['TRconner'], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            elif r == 0:
                screen.blit(IMAGES['Tconner3'], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION-1):
            piece = board[r][c]
            if piece not in ['--', '*-', '**', '#-']:
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == '__main__':
    main()
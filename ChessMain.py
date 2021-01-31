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
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/pieces/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    IMAGES['board'] = p.transform.scale(p.image.load('images/map/map.png'), (WIDTH, HEIGHT))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('White'))
    gs = ChessEngine.GameState()
    loadImages()
    validMoves = gs.getValidMoves()
    moveMade = False  # flag for when a move is made

    running = True
    sqSelected = ()  # (row, col)
    playerClicks = []  # [(6, 4), (4, 4)]

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
                    if sqSelected == (row, col):  # player clicked the same square twice
                        sqSelected == ()  # deselect
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)

                if len(playerClicks) == 2:  # after 2nd click
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
    drawMap(screen)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    for r in range(DIMENSION):
        for c in range(DIMENSION - 1):
            p.draw.rect(screen, p.Color('white'), p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawMap(screen):
    screen.blit(IMAGES['board'], p.Rect(0, 0, WIDTH, HEIGHT))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION - 1):
            piece = board[r][c]
            if piece not in ['--', '*-', '**', '#-']:
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == '__main__':
    main()

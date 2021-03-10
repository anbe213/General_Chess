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
                    gs.generateROF()  # generate ring of fire before make a move
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = ()
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]

                gs.victoryCondition()
                if gs.gameEnd:
                    gs.claimVictory()
                    running = False

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs, validMoves, sqSelected)
        clock.tick(MAX_FPS)
        p.display.flip()
        if not running and gs.gameEnd:
            p.time.delay(5000)


def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('r' if gs.redToMove else 'b'):  # square selected is a piece that can be moved
            # highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            # highlight the move from that square
            s = p.Surface((SQ_SIZE // 4, SQ_SIZE // 4))
            s.fill(p.Color('red'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol * SQ_SIZE + 24, move.endRow * SQ_SIZE + 24))


def drawGameState(screen, gs, validMoves, sqSelected):
    # drawBoard(screen)
    drawMap(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
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


def animateMove(move, screen, board, clock):
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10  # frames to move one square
    framesCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(framesCount + 1):
        r, c = (move.startRow + dR * frame / framesCount, move.startCol + dC * frame / framesCount)
        drawMap(screen)
        drawPieces(screen, board)
        # erase the pieced moved from its ending square
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, p.Color(255, 255, 255, 128), endSquare)
        # draw captured piece onto rectangle
        if move.pieceCaptured not in ['--', '*-', '#-', '**']:
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(100)


if __name__ == '__main__':
    main()

class GameState():
    def __init__(self):
        self.board = [
            ['**', '**', '*-', '--', '--', '--', 'bG', '--', '--', '--', '--'],
            ['**', 'bH', '*-', '--', 'bK', 'bS', '--', 'bS', 'bK', '--', '--'],
            ['**', '**', '*-', 'bP', '--', '--', 'bL', '--', '--', 'bP', '--'],
            ['**', '**', 'bH', '--', 'bF', 'bT', '--', 'bT', 'bF', '--', '--'],
            ['**', '**', 'bB', 'bC', '--', '--', 'bD', '--', '--', 'bC', 'bB'],
            ['**', '**', '*-', '*-', '*-', '#-', '*-', '#-', '*-', '*-', '*-'],
            ['**', '**', '*-', '*-', '*-', '#-', '*-', '#-', '*-', '*-', '*-'],
            ['**', '**', 'rB', 'rC', '--', '--', 'rD', '--', '--', 'rC', 'rB'],
            ['**', '**', 'rH', '--', 'rF', 'rT', '--', 'rT', 'rF', '--', '--'],
            ['**', '**', '*-', 'rP', '--', '--', 'rL', '--', '--', 'rP', '--'],
            ['**', 'rH', '*-', '--', 'rK', 'rS', '--', 'rS', 'rK', '--', '--'],
            ['**', '**', '*-', '--', '--', '--', 'rG', '--', '--', '--', '--']
        ]
        self.terran = [
            ['**', '**', '*-', '--', '--', '--', '--', '--', '--', '--', '--'],
            ['**', '**', '*-', '--', '--', '--', '--', '--', '--', '--', '--'],
            ['**', '**', '*-', '--', '--', '--', '--', '--', '--', '--', '--'],
            ['**', '**', '*-', '--', '--', '--', '--', '--', '--', '--', '--'],
            ['**', '**', '*-', '--', '--', '--', '--', '--', '--', '--', '--'],
            ['**', '**', '*-', '*-', '*-', '#-', '*-', '#-', '*-', '*-', '*-'],
            ['**', '**', '*-', '*-', '*-', '#-', '*-', '#-', '*-', '*-', '*-'],
            ['**', '**', '*-', '--', '--', '--', '--', '--', '--', '--', '--'],
            ['**', '**', '*-', '--', '--', '--', '--', '--', '--', '--', '--'],
            ['**', '**', '*-', '--', '--', '--', '--', '--', '--', '--', '--'],
            ['**', '**', '*-', '--', '--', '--', '--', '--', '--', '--', '--'],
            ['**', '**', '*-', '--', '--', '--', '--', '--', '--', '--', '--']
        ]
        self.moveFunctions = {'B': self.getInfantryMoves, 'C': self.getEngineerMoves, 'D': self.getMilitiaMoves,
                              'F': self.getAntiAirCraftMoves,
                              'G': self.getGeneralMoves, 'H': self.getNavyMoves, 'K': self.getAirCraftMoves,
                              'L': self.getRocketMoves,
                              'P': self.getCanonMoves, 'S': self.getHQMoves, 'T': self.getTankMoves}
        self.redToMove = True
        self.moveLog = []

    def makeMove(self, move):
        if self.board[move.startRow][move.startCol][1] not in ['H', 'K'] and self.terran[move.endRow][move.endCol] == '**':
            self.board[move.endRow][move.endCol] = '**'  # land unit capture enemy at sea
        elif self.board[move.startRow][move.startCol][1] == 'H' and self.terran[move.endRow][move.endCol] in ['--', '#-']:
            self.board[move.endRow][move.endCol] = self.terran[move.endRow][move.endCol]  # navy capture enemy at land
        else:
            self.board[move.startRow][move.startCol] = self.terran[move.startRow][move.startCol]
            self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.redToMove = not self.redToMove

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.redToMove = not self.redToMove

    def getValidMoves(self):
        return self.getAllPossibleMoves()

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'r' and self.redToMove) or (turn == 'b' and not self.redToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves

    def enemyToCapture(self, r, c):
        if (self.redToMove and self.board[r][c][0] == 'b') or (not self.redToMove and self.board[r][c][0] == 'r'):
            return True
        else:
            return False

    # (x1, y1): Current location; (x2, y2): Destination
    def streamAcross(self, x1, y1, x2, y2):
        if abs(x1 - x2) != 1:  # not moving up or down
            return False
        # across stream by diagonal line is not allowed
        if (self.terran[x1][y1] == '#-' and self.terran[x2][y2] == '*-') or (
                self.terran[x1][y1] == '*-' and self.terran[x2][y2] == '#-'):
            return True
        if self.terran[x1][y1] == '*-' and self.terran[x2][y2] == '*-':
            if self.terran[x1][y1 - 1] in ['*-', '#-'] and self.terran[x2][y2 - 1] in ['*-', '#-']:
                return True
            elif self.terran[x1][y1 + 1] in ['*-', '#-'] and self.terran[x2][y2 + 1] in ['*-', '#-']:
                return True
        return False

    def getInfantryMoves(self, r, c, moves):
        if r != 0:  # not at top conner
            if self.board[r - 1][c] in ['*-', '--', '#-'] and not self.streamAcross(r, c, r - 1, c):
                moves.append(Move((r, c), (r - 1, c), self.board))
            elif self.enemyToCapture(r - 1, c):
                moves.append(Move((r, c), (r - 1, c), self.board))

        if r != len(self.board) - 1:  # not at bot conner
            if self.board[r + 1][c] in ['*-', '--', '#-'] and not self.streamAcross(r, c, r + 1, c):
                moves.append(Move((r, c), (r + 1, c), self.board))
            elif self.enemyToCapture(r + 1, c):
                moves.append(Move((r, c), (r + 1, c), self.board))

        if c != 0:  # not at left conner
            if self.board[r][c - 1] in ['*-', '--', '#-'] and not self.streamAcross(r, c, r, c - 1):
                moves.append(Move((r, c), (r, c - 1), self.board))
            elif self.enemyToCapture(r, c - 1):
                moves.append(Move((r, c), (r, c - 1), self.board))

        if c != len(self.board[0]) - 1:  # not at right conner

            if self.board[r][c + 1] in ['*-', '--', '#-'] and not self.streamAcross(r, c, r, c + 1):
                moves.append(Move((r, c), (r, c + 1), self.board))
            elif self.enemyToCapture(r, c + 1):
                moves.append(Move((r, c), (r, c + 1), self.board))

    def getEngineerMoves(self, r, c, moves):
        if r != 0:  # not at top conner
            if self.board[r - 1][c] in ['*-', '--', '#-']:
                moves.append(Move((r, c), (r - 1, c), self.board))
            elif self.enemyToCapture(r - 1, c):
                moves.append(Move((r, c), (r - 1, c), self.board))

        if r != len(self.board) - 1:  # not at bot conner
            if self.board[r + 1][c] in ['*-', '--', '#-']:
                moves.append(Move((r, c), (r + 1, c), self.board))
            elif self.enemyToCapture(r + 1, c):
                moves.append(Move((r, c), (r + 1, c), self.board))

        if c != 0:  # not at left conner
            if self.board[r][c - 1] in ['*-', '--', '#-']:
                moves.append(Move((r, c), (r, c - 1), self.board))
            elif self.enemyToCapture(r, c - 1):
                moves.append(Move((r, c), (r, c - 1), self.board))

        if c != len(self.board[0]) - 1:  # not at right conner
            if self.board[r][c + 1] in ['*-', '--', '#-']:
                moves.append(Move((r, c), (r, c + 1), self.board))
            elif self.enemyToCapture(r, c + 1):
                moves.append(Move((r, c), (r, c + 1), self.board))

    def getMilitiaMoves(self, r, c, moves):
        for i in [r - 1, r, r + 1]:
            for j in [c - 1, c, c + 1]:  # square around (r, c)
                if i == r and j == c:  # stay exception
                    continue
                if 0 <= (i and j) <= len(self.board[0]) - 1:  # conner exception
                    if self.board[i][j] in ['*-', '--', '#-'] and not self.streamAcross(r, c, i, j):  # move
                        moves.append(Move((r, c), (i, j), self.board))
                    elif self.enemyToCapture(i, j):
                        moves.append(Move((r, c), (i, j), self.board))  # capture

    def getAntiAirCraftMoves(self, r, c, moves):
        if r != 0:  # not at top conner
            if self.board[r - 1][c] in ['*-', '--', '#-'] and not self.streamAcross(r, c, r - 1, c):
                moves.append(Move((r, c), (r - 1, c), self.board))
            elif self.enemyToCapture(r - 1, c):
                moves.append(Move((r, c), (r - 1, c), self.board))

        if r != len(self.board) - 1:  # not at bot conner
            if self.board[r + 1][c] in ['*-', '--', '#-'] and not self.streamAcross(r, c, r + 1, c):
                moves.append(Move((r, c), (r + 1, c), self.board))
            elif self.enemyToCapture(r + 1, c):
                moves.append(Move((r, c), (r + 1, c), self.board))

        if c != 0:  # not at left conner
            if self.board[r][c - 1] in ['*-', '--', '#-'] and not self.streamAcross(r, c, r, c - 1):
                moves.append(Move((r, c), (r, c - 1), self.board))
            elif self.enemyToCapture(r, c - 1):
                moves.append(Move((r, c), (r, c - 1), self.board))

        if c != len(self.board[0]) - 1:  # not at right conner
            if self.board[r][c + 1] in ['*-', '--', '#-'] and not self.streamAcross(r, c, r, c + 1):
                moves.append(Move((r, c), (r, c + 1), self.board))
            elif self.enemyToCapture(r, c + 1):
                moves.append(Move((r, c), (r, c + 1), self.board))

    def getGeneralMoves(self, r, c, moves):
        for i in range(r + 1, len(self.board)):  # downward move
            if i == r + 1 and self.enemyToCapture(i, c):  # capture in 1 range
                moves.append(Move((r, c), (i, c), self.board))
            elif self.board[i][c] in ['*-', '--', '#-'] and not self.streamAcross(i - 1, c, i, c):
                moves.append(Move((r, c), (i, c), self.board))
            else:
                break
        for i in range(r - 1, -1, -1):  # upward move
            if i == r - 1 and self.enemyToCapture(i, c):
                moves.append(Move((r, c), (i, c), self.board))
            elif self.board[i][c] in ['*-', '--', '#-'] and not self.streamAcross(i + 1, c, i, c):
                moves.append(Move((r, c), (i, c), self.board))
            else:
                break
        for i in range(c + 1, len(self.board[0])):  # right move
            if i == c + 1 and self.enemyToCapture(r, i):
                moves.append(Move((r, c), (r, i), self.board))
            elif self.board[r][i] in ['*-', '--', '#-']:
                moves.append(Move((r, c), (r, i), self.board))
            else:
                break
        for i in range(c - 1, -1, -1):  # left move
            if i == c - 1 and self.enemyToCapture(r, i):
                moves.append(Move((r, c), (r, i), self.board))
            elif self.board[r][i] in ['*-', '--', '#-']:
                moves.append(Move((r, c), (r, i), self.board))
            else:
                break

    def getNavyMoves(self, r, c, moves):
        for i in range(r + 1, r + 5):  # downward move
            if i > len(self.board) - 1:
                continue
            if self.board[i][c] in ['*-', '**']:
                moves.append(Move((r, c), (i, c), self.board))
            elif self.enemyToCapture(i, c) and self.board[i][c][1] == 'H':  # capture Navy only
                moves.append(Move((r, c), (i, c), self.board))
            else:
                break
        for i in range(r - 1, r - 5, -1):  # upward move
            if i < 0:
                continue
            if self.board[i][c] in ['*-', '**']:
                moves.append(Move((r, c), (i, c), self.board))
            elif self.enemyToCapture(i, c) and self.board[i][c][1] == 'H':  # capture Navy only
                moves.append(Move((r, c), (i, c), self.board))
            else:
                break
        for i in range(c + 1, c + 5):  # right move
            if i > len(self.board[0]) - 1:
                continue
            if self.board[r][i] in ['*-', '**']:
                moves.append(Move((r, c), (r, i), self.board))
            elif self.enemyToCapture(r, i) and self.board[r][i][1] == 'H':  # capture Navy only
                moves.append(Move((r, c), (r, i), self.board))
            else:
                break
        for i in range(c - 1, c - 5, -1):  # left move
            if i < 0:
                continue
            if self.board[r][i] in ['*-', '**']:
                moves.append(Move((r, c), (r, i), self.board))
            elif self.enemyToCapture(r, i) and self.board[r][i][1] == 'H':  # capture Navy only
                moves.append(Move((r, c), (r, i), self.board))
            else:
                break

        for i in range(-3, 4):  # capture enemy by onboard canon
            if i == 0:
                continue
            if -1 < r + i < len(self.board):
                if self.enemyToCapture(r + i, c):
                    moves.append(Move((r, c), (r + i, c), self.board))
            if -1 < c + i < len(self.board[0]):
                if self.enemyToCapture(r, c + i):
                    moves.append(Move((r, c), (r, c + i), self.board))
            if -1 < r + i < len(self.board) and -1 < c + i < len(self.board[0]):
                if self.enemyToCapture(r + i, c + i):
                    moves.append(Move((r, c), (r + i, c + i), self.board))
            if -1 < r - i < len(self.board) and -1 < c + i < len(self.board[0]):
                if self.enemyToCapture(r - i, c + i):
                    moves.append(Move((r, c), (r - i, c + i), self.board))


    def getAirCraftMoves(self, r, c, moves):
        pass

    def getRocketMoves(self, r, c, moves):
        for i in range(r + 1, r + 3):  # downward move
            if i > len(self.board) - 1:
                continue
            if self.board[i][c] in ['*-', '--', '#-'] and not self.streamAcross(i - 1, c, i, c):
                moves.append(Move((r, c), (i, c), self.board))
            else:
                break
        for i in range(r - 1, r - 3, -1):  # upward move
            if i < 0:
                continue
            if self.board[i][c] in ['*-', '--', '#-'] and not self.streamAcross(i + 1, c, i, c):
                moves.append(Move((r, c), (i, c), self.board))
            else:
                break
        for i in range(c + 1, c + 3):  # right move
            if i > len(self.board[0]) - 1:
                continue
            if self.board[r][i] in ['*-', '--', '#-'] and not self.streamAcross(r, i - 1, r, i):
                moves.append(Move((r, c), (r, i), self.board))
            else:
                break
        for i in range(c - 1, c - 3, -1):  # left move
            if i < 0:
                continue
            if self.board[r][i] in ['*-', '--', '#-'] and not self.streamAcross(r, i + 1, r, i):
                moves.append(Move((r, c), (r, i), self.board))
            else:
                break
        for i in range(-2, 3):
            if i == 0:
                continue
            if -1 <= i <= 1:
                if 0 <= r + i <= len(self.board) - 1 and 0 <= c + i <= len(self.board[0]) - 1:
                    if self.board[r + i][c + i] in ['*-', '--', '#-'] and not self.streamAcross(r, c, r + i, c + i):  # diagonal move
                        moves.append(Move((r, c), (r + i, c + i), self.board))
                    elif self.enemyToCapture(r + i, c + i):  # capture in diagonal line
                        moves.append(Move((r, c), (r + i, c + i), self.board))
                if 0 <= r + i <= len(self.board) - 1 and 0 <= c - i <= len(self.board[0]) - 1:
                    if self.board[r + i][c - i] in ['*-', '--', '#-'] and not self.streamAcross(r, c, r + i, c - i):  # diagonal move
                        moves.append(Move((r, c), (r + i, c - i), self.board))
                    elif self.enemyToCapture(r + i, c - i):  # capture in diagonal line
                        moves.append(Move((r, c), (r + i, c - i), self.board))
            if 0 <= r + i <= len(self.board) - 1:
                if self.enemyToCapture(r + i, c):
                    moves.append(Move((r, c), (r + i, c), self.board))
            if 0 <= c + i <= len(self.board[0]) - 1:
                if self.enemyToCapture(r, c + i):
                    moves.append(Move((r, c), (r, c + i), self.board))

    def getCanonMoves(self, r, c, moves):
        pass

    def getHQMoves(self, r, c, moves):
        pass

    def getTankMoves(self, r, c, moves):
        pass

    def validPiece(self, r, c):
        if self.board[r][c] not in ['**', '*-', '#-', '--']:
            return True
        else:
            return False


class Move():
    rankToRows = {"1": 11, "2": 10, "3": 9, "4": 8, "5": 7, "6": 6,
                  "7": 5, "8": 4, "9": 3, "10": 2, "11": 1, "12": 0}
    rowsToRanks = {v: k for k, v in rankToRows.items()}
    filesToCol = {"a": 10, "b": 9, "c": 8, "d": 7, "e": 6,
                  "f": 5, "g": 4, "h": 3, "i": 2, "j": 1, "k": 0}
    colsToFiles = {v: k for k, v in filesToCol.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000000 + self.startCol * 10000 + self.endRow * 100 + self.endCol

    """
    Overriding the equals method
    """

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

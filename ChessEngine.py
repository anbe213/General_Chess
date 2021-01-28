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
        self.moveFunctions = {'B': self.getInfantryMoves, 'C': self.getEngineerMoves, 'D': self.getMilitiaMoves, 'F': self.getAntiAirCraftMoves,
                              'G': self.getGeneralMoves, 'H': self.getNavyMoves, 'K': self.getAirCraftMoves, 'L': self.getRocketMoves,
                              'P': self.getCanonMoves, 'S': self.getHQMoves, 'T': self.getTankMoves}
        self.redToMove = True
        self.moveLog = []

    def makeMove(self, move):
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

    def getInfantryMoves(self, r, c, moves):
        try:
            if self.board[r-1][c] in ['*-', '--', '#-']:
                moves.append(Move((r, c), (r-1, c), self.board))
            if self.board[r+1][c] in ['*-', '--', '#-']:
                moves.append(Move((r, c), (r+1, c), self.board))
            if self.board[r][c-1] in ['*-', '--', '#-']:
                moves.append(Move((r, c), (r, c-1), self.board))
            if self.board[r][c+1] in ['*-', '--', '#-']:
                moves.append(Move((r, c), (r, c+1), self.board))
        except IndexError:
            return()

    def getEngineerMoves(self, r, c, moves):
        pass

    def getMilitiaMoves(self, r, c, moves):
        pass

    def getAntiAirCraftMoves(self, r, c, moves):
        pass

    def getGeneralMoves(self, r, c, moves):
        pass

    def getNavyMoves(self, r, c, moves):
        pass

    def getAirCraftMoves(self, r, c, moves):
        pass

    def getRocketMoves(self, r, c, moves):
        pass

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

    rankToRows = {"1" : 11, "2" : 10, "3" : 9, "4" : 8, "5" : 7, "6" : 6,
                  "7" : 5, "8" : 4, "9" : 3, "10" : 2, "11" : 1, "12" : 0}
    rowsToRanks = {v: k for k, v in rankToRows.items()}
    filesToCol = {"a" : 10, "b" : 9, "c" : 8, "d" : 7, "e" : 6,
                  "f" : 5, "g" : 4, "h" : 3, "i" : 2, "j" : 1, "k" : 0}
    colsToFiles = {v: k for k, v in filesToCol.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000000 + self.startCol * 10000 + self.endRow * 100 + self.endCol
        print(self.moveID)

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
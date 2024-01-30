'''An interactive chess-game module to handle creation of board, squares, and pieces, as well as game flow
(moving pieces, checking legality of moves, checkmate, stalemate, resignation, etc.)'''
import copy

class Piece:
    '''A general piece class (subclasses exist for each piece).
    Color must be specified as an argument.
    '''

    def __init__(self, color):
        while True:
            if color == 'white' or 'black':
                self.color = color
                break
            else:
                color = input('Invalid color. Please enter "white" or "black": ')
        self.hasMoved = False

    def __str__(self):
        '''Returns first letter of the piece subclass ('n' is used for knight).
        White pieces are represented as an uppercase letter, and black pieces as a lowercase letter.
        '''
        if self.color == 'white':
            return self.singleLetterRep.upper()
        elif self.color == 'black':
            return self.singleLetterRep.lower()

    def getColor(self):
        '''Returns color of piece.'''
        return self.color
    def getHasMoved(self):
        '''Returns Boolean value stating whether the piece has been moved.'''
        return self.hasMoved
    def markAsMoved(self):
        '''Marks a piece as moved.'''
        self.hasMoved = True
    
class King(Piece):
    '''King Piece subclass. Color must be specified as an argument.'''
    def __init__(self, color):
        Piece.__init__(self, color)
        self.singleLetterRep = 'k'
class Queen(Piece):
    '''Queen Piece subclass. Color must be specified as an argument.'''
    def __init__(self, color):
        Piece.__init__(self, color)
        self.singleLetterRep = 'q'
class Rook(Piece):
    '''Rook Piece subclass. Color must be specified as an argument.'''
    def __init__(self, color):
        Piece.__init__(self, color)
        self.singleLetterRep = 'r'
class Bishop(Piece):
    '''Bishop Piece subclass. Color must be specified as an argument.'''
    def __init__(self, color):
        Piece.__init__(self, color)
        self.singleLetterRep = 'b'
class Knight(Piece):
    '''Bishop Piece subclass. Color must be specified as an argument.'''
    def __init__(self, color):
        Piece.__init__(self, color)
        self.singleLetterRep = 'n'
class Pawn(Piece):
    '''Pawn Piece subclass. Color must be specified as an argument.'''
    def __init__(self, color):
        Piece.__init__(self, color)
        self.singleLetterRep = 'p'

class Square:
    '''A square class that has file, rank, color, and occupying piece data.
    Full board or game information is not stored in the square object.'''
    def __init__(self, file, rank):
        self.file = file
        self.rank = rank

        fileMap = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
        if (fileMap[file] % 2 == 0 and rank % 2 == 0) or (fileMap[file] % 2 != 0 and rank % 2 != 0):
            self.color = 'dark'
        else:
            self.color = 'light'
        
        self.occupyingPiece = None
        
    def getFile(self):
        '''Returns the file of the square ('a' thru 'h')'''
        return self.file
    def getRank(self):
        '''Returns the rank of the square (1 thru 9)'''
        return self.rank
    def getFileRank(self):
        '''Returns full position of the square ('a1' thru 'h8')'''
        return f'{self.file}{self.rank}'
    def getColor(self):
        '''Returns the color of the square (light or dark)'''
        return self.color
    def getOccupyingPiece(self):
        '''Returns the occupying piece of the square.
        Note: this returns the full piece object.'''
        return self.occupyingPiece

    def addPiece(self, piece):
        '''Adds a piece to the square.
        Note: this will replace an existing piece.'''
        self.occupyingPiece = piece
    def removePiece(self):
        '''Removes a piece from the square.'''
        self.occupyingPiece = None

    def __str__(self):
        '''Prints a square icon with the first letter of the piece inside.'''
        if self.occupyingPiece is None:
            return'[ ]'
        else:
            return f'[{self.occupyingPiece}]'

# Board class that contains many squares.
class Board:
    '''A board class that contains 64 squares. Takes an optional 'fen' argument to initialize pieces.
    In the absense of a fen argument, or if fen = 'standard', the board will be populated with the traditional piece setup.'''
    def __init__(self, fen = 'standard'):
        #Initialize all of the squares.
        self.squares = []
        for rank in range(1,9):
            for file in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
                self.squares.append(Square(file, rank))

        #Initialize all pieces based on fen and add them to squares.
        if fen == 'standard':
            self.startingPosition = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
        elif fen == 'empty':
            self.startingPosition = '8/8/8/8/8/8/8/8'
        else:
            self.startingPosition = fen

        fenFormat1 = list(reversed(self.startingPosition.split('/')))
        fenFormat1 = ''.join(fenFormat1)

        fenFormat2 = []
        for character in fenFormat1:
            try:
                numBlanks = int(character)
                for i in range(numBlanks):
                    fenFormat2.append(' ')
            except:
                fenFormat2.append(character)

        #Finally, time to assign pieces to each square.

        pieceMap = {'k': King, 'q': Queen, 'r': Rook, 'n': Knight, 'b': Bishop,
                    'p': Pawn}

        for square, pieceLetter in zip(self.squares, fenFormat2):
            if pieceLetter == ' ':
                continue
            elif pieceLetter.isupper():
                square.addPiece( pieceMap[pieceLetter.lower()](color = 'white') )
            elif pieceLetter.islower():
                square.addPiece( pieceMap[pieceLetter.lower()](color = 'black') )


    # Method that maps a square location input (ie. e1 or f7) to its correct square object.
    # This could be used to edit a board using Board.accessSquare('piece_coordinate').addPiece()
    def accessSquare(self, position):
        '''Takes a position argument (eg. 'a1' thru 'h8') and returns the full square object.'''
        fileMap = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        coordinate = [character for character in position]
        rankMultiplier = int(coordinate[1]) - 1
        fileAdder = fileMap[coordinate[0]]
        squaresIdx = (8 * rankMultiplier) + fileAdder
        return self.squares[squaresIdx]

    def __str__(self):
        '''Prints the current full board setup, with each square represented as '[p]', where p is the first letter
        representation of the occupying piece.'''
        boardList = []
        for rank in range(8, 0, -1):
            thisRankList = []

            for square in self.squares:
                if square.getRank() == rank:
                    thisRankList.append(str(square))

            thisRankList.append('\n')
            for square in thisRankList:
                boardList.append(square)

        boardStr = ''.join(boardList)

        return boardStr

class Move:
    '''Takes 'board' and 'UCImove' (eg. 'e2e4' or 'h7h8q') arguments and creates a move object.
    Note: move is not executed until .execute() is run.'''
    def __init__(self, board, UCImove):
        self.board = board
        self.UCImove = UCImove
        self.boardBeforeMove = copy.deepcopy(board)
        self.fromSquare = self.board.accessSquare(UCImove[:2])
        self.fromPiece = self.fromSquare.getOccupyingPiece()
        self.toSquare = self.board.accessSquare(UCImove[2:4])

    def execute(self):
        '''Executes the move on the specified board.'''
        self.toSquare.addPiece(self.fromPiece)
        self.fromSquare.removePiece()
        self.fromPiece.markAsMoved()

    def getMovedPiece(self):
        '''Returns the piece object that occupies the 'from' square at the time of creation of the move object.'''
        return self.fromPiece

class enPassant(Move):
    '''Move subclass for en-passant moves.'''
    def __init__(self, board, UCImove):
        Move.__init__(self, board, UCImove)

    def execute(self):
        super().execute()
        squareModifier = {'white': -1, 'black': 1}
        capturedSquareFile = self.toSquare.getFile()
        capturedSquareRank = int(self.toSquare.getRank()) + squareModifier[self.fromPiece.getColor()]
        capturedSquare = self.board.accessSquare(f'{capturedSquareFile}{capturedSquareRank}')
        capturedSquare.removePiece()

class castle(Move):
    '''Move subclass for castling moves.'''
    def __init__(self, board, UCImove):
        Move.__init__(self, board, UCImove)

    def execute(self):
        super().execute()
        kingMovement = ( ord(self.toSquare.getFile()) - ord(self.fromSquare.getFile()) )
        directionToRook = kingMovement / abs(kingMovement)      # results in +1 or -1 lateral direction
        distanceToRook = -2 if directionToRook == -1 else 1
        castlingRookRank = self.toSquare.getRank()

        castlingRookFromFile = chr(ord(self.toSquare.getFile()) + int(distanceToRook))
        castlingRookFromSquare = self.board.accessSquare(f'{castlingRookFromFile}{castlingRookRank}')
        castlingRook = castlingRookFromSquare.getOccupyingPiece()

        castlingRookToFile = chr(ord(self.toSquare.getFile()) - int(directionToRook))
        castlingRookToSquare = self.board.accessSquare(f'{castlingRookToFile}{castlingRookRank}')

        castlingRookToSquare.addPiece(castlingRook)
        castlingRookFromSquare.removePiece()
        castlingRook.markAsMoved()

class promote(Move):
    '''Move subclass for promotion moves.'''
    def __init__(self, board, UCImove):
        Move.__init__(self, board, UCImove)
        if len(self.UCImove) > 4:
            self.promotionChoice = UCImove[4]
        else:
            self.promotionChoice = 'q'

    def execute(self):
        super().execute()
        promotionPieceMap = {'q': Queen, 'r': Rook, 'n': Knight, 'b': Bishop}
        self.toSquare.addPiece(promotionPieceMap[self.promotionChoice](self.fromPiece.getColor()))

class chessGame:
    '''Game class that takes a board argument and takes an optional 'toMove' argument of 'white' or 'black'.
    If no 'toMove' is specified, 'white' will be chosen as default.'''
    def __init__(self, board, toMove = 'white'):
        self.board = board
        self.toMove = toMove
        self.firstMove = toMove
        self.movesList = []
        self.movesObjects = []
        self.scoreWhite = None
        self.scoreBlack = None
        self.resultType = None
        self.FiftyMoveCount = 0
        self.pastPositions = [f'{self.board}']
        self.whiteProposesDraw = False
        self.blackProposesDraw = False
        self.whiteKingPos = 'e1'
        self.blackKingPos = 'e8'

    def getTurn(self):
        '''Returns the current player to move ('white' or 'black').'''
        return self.toMove

    def __switchToMove(self):
        '''Switches the current player to move ('white' -> 'black' or vice versa).'''
        switchMoveMap = {'white': 'black', 'black': 'white'}
        self.toMove = switchMoveMap[self.toMove]
    def getMoves(self):
        '''Returns a formatted list of all moves that have been played in the game.'''
        movesStrList = []
        if self.firstMove == 'white':
            startingIdx = 0
        else:
            movesStrList.append(f'1. ?, {self.movesList[0]}')
            startingIdx = 1

        for index, move in enumerate(self.movesList[startingIdx:]):
            thisAppend = []
            if index % 2 == 0:
                thisAppend.append(f'{int(index/2 + 1)}. {move}, ')
            else:
                thisAppend.append(f'{move}\n')
            movesStrList.append(''.join(thisAppend))
        return ''.join(movesStrList)

    def move(self, UCImove):
        '''Takes a 'UCImove' argument and attempts to execute a move.
        If the move is legal, the move will execute.
        .move() automatically tests for the fifty-move-rule, threefold-repetition, insufficient material, checkmate, and stalemate. '''
        if self.resultType is not None:
            return 'Move is invalid. The game has already ended.'

        move = Move(self.board, UCImove)

        if self.movesObjects != []:
            lastMove = self.movesObjects[-1]
        else:
            lastMove = None

        # if UCImove not in self.legalMoves:
        if not testMoveLegality(move, self.toMove, lastMove):
            return 'This move is illegal'

        # 50 move rule.
        if move.toSquare.getOccupyingPiece() is None and not isinstance(move.getMovedPiece(), Pawn):    # If the move is not a capture and the piece moved is not a pawn
            FiftyMoveAdd = True
        else:
            FiftyMoveAdd = False

        def normalMove():
            executableMove = move
            return executableMove

        if isinstance(move.fromPiece, Pawn):
            if ord(move.UCImove[0])-ord(move.UCImove[2]) != 0 and move.toSquare.getOccupyingPiece() is None:
                executableMove = enPassant(move.board, move.UCImove)
            elif (move.UCImove[3] == '8' and move.fromPiece.getColor() == 'white') or (move.UCImove[3] == '1' and move.fromPiece.getColor() == 'black'):
                if len(move.UCImove)==5:
                    executableMove = promote(move.board, move.UCImove)
                else:
                    executableMove = promote(move.board, move.UCImove+'q')
            else:
                executableMove = normalMove()
        elif isinstance(move.fromPiece, King):
            if abs(ord(move.UCImove[0]) - ord(move.UCImove[2])) == 2:
                executableMove = castle(move.board, move.UCImove)
            else:
                executableMove = normalMove()
        else:
            executableMove = normalMove()

        executableMove.execute()
        self.__switchToMove()
        self.movesList.append(UCImove)
        self.movesObjects.append(executableMove)

        currentStatus = isCheckMateOrStaleMate(self)
        if currentStatus == 'checkmate':
            print(f'Game over! {self.toMove} is in checkmate!')
            if self.toMove == 'white':
                self.scoreWhite = 0
                self.scoreBlack = 1
            else:
                self.scoreWhite = 1
                self.scoreBlack = 0
            self.resultType = 'checkmate'
        elif currentStatus == 'stalemate':
            print(f'Game over! {self.toMove} is in stalemate!')
            self.scoreWhite = self.scoreBlack = 0.5
            self.resultType = 'stalemate'

        if FiftyMoveAdd is True:
            self.FiftyMoveCount += 1
            if self.FiftyMoveCount == 100:  # Count as 100 because it is 50 moves for white and black.
                self.scoreWhite = self.scoreBlack = 0.5
                self.resultType = ('50 move')
                print(f'Game over! The game is drawn by the fifty move rule.')
        else:
            self.FiftyMoveCount = 0

        # Threefold repetition
        self.pastPositions.append(f'{self.board}')
        if self.pastPositions.count(f'{self.board}') == 3:
            self.scoreWhite = self.scoreBlack = 0.5
            self.resultType = 'threefold repetition'
            print(f'Game over! The game is drawn by threefold repetition!')

        # Insufficient material
        if isInsufficientMaterial(self) is True:
            self.scoreBlack = self.scoreWhite = 0.5
            self.resultType = 'insufficient material'
            print(f'Game over! The game is drawn by threefold repetition!')

    def agreeToDraw(self):
        '''Ends the game, sets result to 'agreement' and sets both player's scores to 0.5.'''
        self.scoreWhite = self.scoreBlack = 0.5
        self.resultType = 'agreement'
        print(f'Game over! The players have agreed to a draw!')

    def resign(self, color):
        '''Ends the game, sets result to 'resignation', sets winner's score to 1, and sets loser's score to 0.'''
        self.resultType = 'resignation'
        if color == 'white':
            self.scoreBlack = 1
            self.scoreWhite = 0
        elif color == 'black':
            self.scoreBlack = 0
            self.scoreWhite = 1
        print(f'Game over! {color} has resigned!')

    def proposeDraw(self, color: str = 'white' or 'black'):
        '''Allows specified player to propose a draw. If both players propose a draw, .agreeToDraw() is run automatically, which
        ends the game, sets result to 'agreement' and sets both player's scores to 0.5.'''
        if color == 'white':
            self.whiteProposesDraw = True
        elif color == 'black':
            self.blackProposesDraw = True

        if self.whiteProposesDraw and self.blackProposesDraw:
            self.agreeToDraw()

def pieceSees(board, pieceFrom, lastMove = None):   #   Find the squares that a piece sees.
    '''Takes arguments 'board', 'pieceFrom', and lastMove (default=None), and finds what squares 'pieceFrom' 'sees' on the board.
    In other words, it finds a piece's pseudo-legal moves.
    Note: 'pieceFrom' must be the piece position, not the piece object.'''
    squareFrom = board.accessSquare(pieceFrom)
    fileFrom = squareFrom.getFile()
    fileFromOrd = ord(fileFrom)
    rankFrom = int(squareFrom.getRank())
    piece = squareFrom.getOccupyingPiece()
    pieceSight = []

    if isinstance(piece, Pawn):
        colorModifier = 1 if piece.getColor() == 'white' else -1
        if rankFrom not in [1,8] and board.accessSquare(f'{fileFrom}{rankFrom+colorModifier}').getOccupyingPiece() is None:
            pieceSight.append(f'{fileFrom}{rankFrom+colorModifier}')    # pawn can move 1 square
        if piece.getHasMoved() is False and board.accessSquare(f'{fileFrom}{rankFrom+(2*colorModifier)}').getOccupyingPiece() is None:  # If the piece hasn't moved...
            pieceSight.append(f'{fileFrom}{rankFrom + (2 * colorModifier)}')  # pawn can move 2 squares.
        try:
            if board.accessSquare(f'{chr(fileFromOrd + 1)}{rankFrom + colorModifier}').getOccupyingPiece() is not None:
                pieceSight.append(f'{chr(fileFromOrd + 1)}{rankFrom + colorModifier}')    # pawn can move 1 square diagonally
        except:
            pass
        try:
            if board.accessSquare(f'{chr(fileFromOrd - 1)}{rankFrom + colorModifier}').getOccupyingPiece() is not None:
                pieceSight.append(f'{chr(fileFromOrd - 1)}{rankFrom + colorModifier}')  # pawn can move 1 square diagonally
        except:
            pass
        if lastMove is not None:    # Logic to allow en passant: last moved piece is pawn, absolute value of file difference is 1, and same rank.
            if isinstance(lastMove.getMovedPiece(), Pawn) and (abs(ord(lastMove.toSquare.getFile())-fileFromOrd) == 1 and lastMove.toSquare.getRank()-rankFrom == 0):
                captureDirection = ord(lastMove.toSquare.getFile())-fileFromOrd
                pieceSight.append(f'{chr(fileFromOrd + captureDirection)}{rankFrom + colorModifier}')
    elif isinstance(piece, Knight):     # Add all combos of 2x1 moves.
        for vertMove in [2,-2]:
            for horiMove in [1,-1]:
                pieceSight.append(f'{chr(fileFromOrd+horiMove)}{rankFrom+vertMove}')
        for vertMove in [1,-1]:
            for horiMove in [2,-2]:
                pieceSight.append(f'{chr(fileFromOrd+horiMove)}{rankFrom+vertMove}')
    elif isinstance(piece, Bishop):     # Add all combos of x by x moves.
        for moveLength in range(1,8):
            pieceSight.append(f'{chr(fileFromOrd+moveLength)}{rankFrom + moveLength}')
            pieceSight.append(f'{chr(fileFromOrd + moveLength)}{rankFrom - moveLength}')
            pieceSight.append(f'{chr(fileFromOrd - moveLength)}{rankFrom + moveLength}')
            pieceSight.append(f'{chr(fileFromOrd - moveLength)}{rankFrom - moveLength}')
    elif isinstance(piece, Rook):
        for moveLength in range(1, 8):  # Add all combos of x by 0 moves.
            pieceSight.append(f'{chr(fileFromOrd + moveLength)}{rankFrom}')
            pieceSight.append(f'{chr(fileFromOrd - moveLength)}{rankFrom}')
            pieceSight.append(f'{fileFrom}{rankFrom + moveLength}')
            pieceSight.append(f'{fileFrom}{rankFrom - moveLength}')
    elif isinstance(piece, Queen):  # Add all moves that would be added to a rook or bishop.
        for moveLength in range(1, 8):  # Add all combos of x by 0 moves.
            pieceSight.append(f'{chr(fileFromOrd + moveLength)}{rankFrom}')
            pieceSight.append(f'{chr(fileFromOrd - moveLength)}{rankFrom}')
            pieceSight.append(f'{fileFrom}{rankFrom + moveLength}')
            pieceSight.append(f'{fileFrom}{rankFrom - moveLength}')
            pieceSight.append(f'{chr(fileFromOrd + moveLength)}{rankFrom + moveLength}')
            pieceSight.append(f'{chr(fileFromOrd + moveLength)}{rankFrom - moveLength}')
            pieceSight.append(f'{chr(fileFromOrd - moveLength)}{rankFrom + moveLength}')
            pieceSight.append(f'{chr(fileFromOrd - moveLength)}{rankFrom - moveLength}')
    elif isinstance(piece, King):
        pieceSight.append(f'{chr(fileFromOrd + 1)}{rankFrom}')
        pieceSight.append(f'{chr(fileFromOrd - 1)}{rankFrom}')
        pieceSight.append(f'{fileFrom}{rankFrom + 1}')
        pieceSight.append(f'{fileFrom}{rankFrom - 1}')
        pieceSight.append(f'{chr(fileFromOrd + 1)}{rankFrom + 1}')
        pieceSight.append(f'{chr(fileFromOrd + 1)}{rankFrom - 1}')
        pieceSight.append(f'{chr(fileFromOrd - 1)}{rankFrom + 1}')
        pieceSight.append(f'{chr(fileFromOrd - 1)}{rankFrom - 1}')
        if piece.getHasMoved() is False:
            if board.accessSquare(f'h{rankFrom}').getOccupyingPiece() is not None and board.accessSquare(f'h{rankFrom}').getOccupyingPiece().getHasMoved() is False:
                pieceSight.append(f'{chr(fileFromOrd + 2)}{rankFrom}')
            if board.accessSquare(f'a{rankFrom}').getOccupyingPiece() is not None and board.accessSquare(f'a{rankFrom}').getOccupyingPiece().getHasMoved() is False:
                pieceSight.append(f'{chr(fileFromOrd - 2)}{rankFrom}')

    pieceSight2 = []    # remove non-existent squares
    for square in pieceSight:
        if square[0] in ['a','b','c','d','e','f','g','h'] and int(square[1:]) in range(1,9):
            pieceSight2.append(square)

    pieceSight3 = []
    if not (isinstance(piece, Knight) or isinstance(piece, King)):
        for squareTo in pieceSight2:   # remove squares whose path is blocked.
            try:
                vertDirection = int( (int(squareTo[1]) - rankFrom)/abs(int(squareTo[1]) - rankFrom) )  # Need to be 1 or -1
            except:
                vertDirection = 0
            try:
                horiDirection = int( (ord(squareTo[0]) - fileFromOrd)/abs(ord(squareTo[0]) - fileFromOrd) )
            except:
                horiDirection = 0

            blocked = False
            thisSquare = f'{chr(fileFromOrd + horiDirection)}{int(rankFrom) + vertDirection}'

            while blocked is False and thisSquare != squareTo:
                if board.accessSquare(thisSquare).getOccupyingPiece() is not None:
                    blocked = True
                    break
                thisSquare = f'{chr(ord(thisSquare[0]) + horiDirection)}{int(thisSquare[1]) + vertDirection}'

            if blocked is False:
                pieceSight3.append(squareTo)
    else:
        pieceSight3=pieceSight2

    pieceSight4 = []
    for square in pieceSight3:  # remove squares that are occupied by a piece of the same color.
        if board.accessSquare(square).getOccupyingPiece() is None or board.accessSquare(square).getOccupyingPiece().getColor() != piece.getColor():
            pieceSight4.append(square)

    return pieceSight4

def isCheck(board: Board, colorToMove):
    '''Takes a 'board' and 'colorToMove' argument and determines if the player to move is in check.'''
    for square in board.squares:
        if isinstance(square.getOccupyingPiece(), King) and square.getOccupyingPiece().getColor() == colorToMove:
            squareInQuestion = f'{square.getFile()}{square.getRank()}'
            break
    for square in board.squares:
        if squareInQuestion in pieceSees(board, f'{square.getFile()}{square.getRank()}'):
            return True
    return False

def testMoveLegality(move: Move, colorToMove, lastMove = None):
    '''Takes a move object, the current player to move, and the last move played, and returns a Boolean value stating
    whether a move is legal.'''
    testBoard = copy.deepcopy(move.board)

    if move.fromPiece.getColor() != colorToMove:    # illegal to move opponent's piece
        return False

    if move.toSquare.getFileRank() not in pieceSees(move.board, move.fromSquare.getFileRank(), lastMove):   # illegal if the piece does not see the square it moves to
        return False

    testMove = Move(testBoard, move.UCImove)
    testMove.execute()
    if isCheck(testBoard, colorToMove) is True:     # illegal if the move results in a position where moving player is in check.
        return False

    # Now, to return False if the King is castling through check.
    fileToOrd = ord(move.toSquare.getFileRank()[0])
    fileFromOrd = ord(move.fromSquare.getFileRank()[0])
    distance = fileToOrd - fileFromOrd

    if isinstance(move.getMovedPiece(), King) and abs(fileToOrd-fileFromOrd) == 2:
        direction = int(distance / abs(distance))

        checkTestBoard = copy.deepcopy(move.board)
        currentKingPos = move.UCImove[:2]
        nextSquare = f'{chr(fileFromOrd + direction)}{move.fromSquare.getFileRank()[1]}'

        while currentKingPos != move.toSquare.getFileRank():
            if isCheck(checkTestBoard, colorToMove) is True:
                return False
            else:
                testMove = Move(checkTestBoard, f'{currentKingPos}{nextSquare}')
                testMove.execute()
                currentKingPos = nextSquare
                nextSquare = f'{chr(ord(currentKingPos[0]) + direction)}{currentKingPos[1]}'

    return True

def hasLegalMoves(game: chessGame):
    '''Takes a game object and returns a Boolean value stating whether there are any legal moves for the current player to move.'''
    lastMove = game.movesObjects[-1] if game.movesObjects != [] else None

    testableFromSquares = [square for square in game.board.squares if square.getOccupyingPiece() is not None and square.getOccupyingPiece().getColor() == game.toMove]
    for square in testableFromSquares:
        testableToSquares = pieceSees(game.board, square.getFileRank(), lastMove = lastMove)
        for squareTo in testableToSquares:
            squareToObject = game.board.accessSquare(squareTo)
            testMove = Move(game.board, f'{square.getFileRank()}{squareToObject.getFileRank()}')
            if testMoveLegality(testMove, game.toMove, lastMove = lastMove) is True:
                return True
    return False

def isCheckMateOrStaleMate(game: chessGame):
    '''Takes a game object and returns 'checkmate', 'stalemate', or None for the current player to move.'''
    if isCheck(game.board, game.toMove) is True:
        if not hasLegalMoves(game):
            return 'checkmate'
        else:
            return False
    else:
        if not hasLegalMoves(game):
            return 'stalemate'

def isInsufficientMaterial(game: chessGame):
    '''Takes a game object and returns Boolean value stating whether or not the players have insufficient material
    to checkmate.'''
    pieces = []
    for square in game.board.squares:
        if square.getOccupyingPiece() is not None:
            pieces.append(f'{square.getOccupyingPiece()}')

    conditions = [
        'p' not in pieces,
        'P' not in pieces,
        'r' not in pieces,
        'R' not in pieces,
        'q' not in pieces,
        'Q' not in pieces,
        (pieces.count('b') < 2 and 'n' not in pieces) and (pieces.count('B') < 2 and 'N' not in pieces) or (
            (pieces.count('n') < 2 and 'b' not in pieces) and (pieces.count('N') < 2 and 'B' not in pieces)
        )
    ]
    if all(conditions):
        return True
    else:
        return False
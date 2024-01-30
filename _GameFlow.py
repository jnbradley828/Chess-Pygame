'''Basic game-flow script used to test handling of rules in ChessObjects.'''

import ChessObjects as co

board = co.Board('standard')
game = co.chessGame(board)
print(board)

while game.resultType is None:
    currentMove = game.toMove
    UCImove = input(f'{currentMove} to move: ')
    if UCImove == 'draw':
        game.agreeToDraw()
    elif UCImove == 'resign':
        game.resign(game.toMove)
    game.move(UCImove)
    print(board)

print(game.getMoves())
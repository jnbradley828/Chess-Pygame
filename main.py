# Creates a playable pygame window. Compatible with pygbag to display in browser.

import pygame
import ChessObjects as co
import asyncio

async def main():
    boardLength = 704
    sideBarWidth = 120
    windowLength = boardLength + sideBarWidth
    windowHeight = boardLength
    squareLength = boardLength // 8

    colorPOV = None
    board = co.Board('standard')
    game = co.chessGame(board)

    clickedSquare = None
    promotionWaiting = False
    scrollPosition: int = 28  # For scrolling through moves.

    pygame.init()
    screen = pygame.display.set_mode((windowLength, windowHeight))
    clock = pygame.time.Clock()

    rectanglePairsWhitePOV = []
    rectanglePairsBlackPOV = []
    for square in board.squares:
        thisFile = square.getFile()
        thisRank = square.getRank()
        fileMultiplier = ord(thisFile) - 97

        thisSquareBlack = pygame.Rect((
            (boardLength - ((fileMultiplier + 1) * squareLength)), ((thisRank - 1) * squareLength),
            squareLength,
            squareLength
        ))
        rectanglePairsBlackPOV.append((thisSquareBlack, square))

        thisSquareWhite = pygame.Rect((
            (fileMultiplier * squareLength), boardLength - (thisRank * squareLength), squareLength,
            squareLength
        ))
        rectanglePairsWhitePOV.append((thisSquareWhite, square))

    # All rectangles to draw later:
    playWhiteRect = pygame.Rect((0, 0, windowLength // 2, windowHeight))
    playBlackRect = pygame.Rect((windowLength // 2, 0, windowLength // 2, windowHeight))

    buttonHeight = squareLength / 2
    buttonLength = sideBarWidth

    resignWhiteRect = pygame.Rect((boardLength, boardLength - buttonHeight, buttonLength, buttonHeight))
    resignBlackRect = pygame.Rect((boardLength, 0, buttonLength, buttonHeight))

    drawWhiteRect = pygame.Rect((boardLength, boardLength - (2 * buttonHeight), buttonLength, buttonHeight))
    drawBlackRect = pygame.Rect((boardLength, buttonHeight, buttonLength, buttonHeight))

    # Fonts
    fontPick = pygame.font.Font(None, 30)
    fontPieces = pygame.font.Font('CONDFONT.TTF', 80)
    fontResignDraw = pygame.font.Font(None, 25)
    fontMoves = pygame.font.Font(None, 18)

    # Text boxes
    textContentPW = 'Play as WHITE'
    textWhiteSelect = fontPick.render(textContentPW, True, 'black')
    textContentPB = 'Play as BLACK'
    textBlackSelect = fontPick.render(textContentPB, True, 'white')
    textContentResign = 'Resign'
    textResign = fontResignDraw.render(textContentResign, True, 'black')
    textContentDraw = 'Propose draw'
    textDraw = fontResignDraw.render(textContentDraw, True, 'black')

    pygame.draw.rect(screen, (255, 255, 255), playWhiteRect)
    pygame.draw.rect(screen, (0, 0, 0), playBlackRect)
    textRectWhite = textWhiteSelect.get_rect(center=playWhiteRect.center)
    textRectBlack = textBlackSelect.get_rect(center=playBlackRect.center)

    while True:
        if colorPOV is None:
            screen.blit(textWhiteSelect, textRectWhite)
            screen.blit(textBlackSelect, textRectBlack)
            pygame.display.set_caption("Select your piece color.")

        else:
            # Shows result at the top of the screen if the game has ended.
            if game.resultType is None:
                pygame.display.set_caption("Chess_Game")
            if game.resultType is not None:
                pygame.display.set_caption(f"Chess_Game... {game.scoreWhite}-{game.scoreBlack} by {game.resultType}")

            # Creates clickable squares with movable pieces.

            if colorPOV == 'white':
                rectanglePairs = rectanglePairsWhitePOV
            elif colorPOV =='black':
                rectanglePairs = rectanglePairsBlackPOV

            for thisSquare in rectanglePairs:
                thisSquareRect = thisSquare[0]
                thisSquareObj = thisSquare[1]
                if clickedSquare == f'{thisSquareObj.getFileRank()}':
                    pygame.draw.rect(screen, (190, 190, 0), thisSquareRect)
                elif co.isCheck(game.board, game.toMove) and (isinstance(thisSquareObj.getOccupyingPiece(),
                                                                         co.King) and thisSquareObj.getOccupyingPiece().getColor() == game.toMove):
                    pygame.draw.rect(screen, (190, 0, 0), thisSquareRect)
                elif thisSquare[1].getColor() == 'light':
                    pygame.draw.rect(screen, (250, 249, 246), thisSquareRect)
                else:
                    pygame.draw.rect(screen, (130, 65, 0), thisSquareRect)

                # Add piece symbols to squares.
                if thisSquareObj.getOccupyingPiece() is not None:
                    pieceMap = {'K': 'k', 'k': 'l', 'Q': 'q', 'q': 'w', 'R': 'r', 'r': 't', 'N': 'n', 'n': 'm',
                                'B': 'b',
                                'b': 'v', 'P': 'p', 'p': 'o'}
                    pieceStr = f'{thisSquareObj.getOccupyingPiece()}'
                    textContent = pieceMap[pieceStr]
                    text = fontPieces.render(textContent, True, 'black')
                    textRect = text.get_rect(center=thisSquareRect.center)
                    screen.blit(text, textRect)

            pygame.draw.rect(screen, (150, 75, 75), resignWhiteRect)
            pygame.draw.rect(screen, (150, 75, 75), resignBlackRect)

            textRectWhite = textResign.get_rect(center=resignWhiteRect.center)
            textRectBlack = textResign.get_rect(center=resignBlackRect.center)
            screen.blit(textResign, textRectWhite)
            screen.blit(textResign, textRectBlack)

            if game.whiteProposesDraw:
                pygame.draw.rect(screen, (190, 190, 0), drawWhiteRect)
            else:
                pygame.draw.rect(screen, (50, 75, 150), drawWhiteRect)
            if game.blackProposesDraw:
                pygame.draw.rect(screen, (190, 190, 0), drawBlackRect)
            else:
                pygame.draw.rect(screen, (50, 75, 150), drawBlackRect)

            textDrawRectWhite = textDraw.get_rect(center=drawWhiteRect.center)
            textDrawRectBlack = textDraw.get_rect(center=drawBlackRect.center)
            screen.blit(textDraw, textDrawRectWhite)
            screen.blit(textDraw, textDrawRectBlack)

            # Creates running move list.
            moveListHeight = (boardLength * 3) // 4
            moveListTop = (boardLength - moveListHeight) // 2
            moveListRect = pygame.Rect((boardLength, moveListTop, sideBarWidth, moveListHeight))
            pygame.draw.rect(screen, (75, 75, 100), moveListRect)

            moveList = game.getMoves().split('\n')
            try:
                moveList.remove('')
            except:
                pass
            if game.resultType is not None:
                moveList.append(f'{game.scoreWhite}-{game.scoreBlack} by')
                moveList.append(f'{game.resultType}')
            if len(moveList) > 28:
                endIndex = 28 - scrollPosition
                moveListDisplayed = moveList[-scrollPosition:endIndex] if scrollPosition >= 29 else moveList[-scrollPosition:]
            else:
                moveListDisplayed = moveList

            for index, move in enumerate(moveListDisplayed):
                textContent = move
                text = fontMoves.render(textContent, True, 'black')

                centerIndex = (len(moveListDisplayed) - 1) / 2
                indexDistance = index - centerIndex
                moveListCenter = moveListRect.center
                thisRectCenter = (moveListCenter[0], moveListCenter[1] + (indexDistance * 18))

                textMoveList = text.get_rect(center=thisRectCenter)
                screen.blit(text, textMoveList)

        # Event handler!
        eventBreak = False

        for event in pygame.event.get():
            if game.resultType is not None:
                if event.type != pygame.QUIT:
                    continue
                else: quit()

            if event.type == pygame.QUIT:
                quit()

            elif colorPOV is None:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if textRectWhite.collidepoint(mouse_x, mouse_y):
                        colorPOV = 'white'
                        break
                    elif textRectBlack.collidepoint(mouse_x, mouse_y):
                        colorPOV = 'black'
                        break

            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    for pair in rectanglePairs:
                        if pair[0].collidepoint(mouse_x, mouse_y):
                            if clickedSquare is None:
                                if pair[1].getOccupyingPiece() is not None:
                                    clickedSquare = f'{pair[1].getFileRank()}'
                            else:
                                moveToSquare = f'{pair[1].getFileRank()}'
                                if isinstance(board.accessSquare(clickedSquare).getOccupyingPiece(), co.Pawn) and \
                                        moveToSquare[1] in ['1', '8']:
                                    promotionWaiting = True
                                else:
                                    game.move(f'{clickedSquare}{moveToSquare}')
                                    clickedSquare = None
                            eventBreak = True
                            break
                    if eventBreak:
                        break

                    if resignWhiteRect.collidepoint(mouse_x, mouse_y):
                        game.resign('white')
                        break
                    elif resignBlackRect.collidepoint(mouse_x, mouse_y):
                        game.resign('black')
                        break
                    elif drawWhiteRect.collidepoint(mouse_x, mouse_y):
                        if game.whiteProposesDraw:
                            game.whiteProposesDraw = False
                        else:
                            game.proposeDraw('white')
                        break
                    elif drawBlackRect.collidepoint(mouse_x, mouse_y):
                        if game.blackProposesDraw:
                            game.blackProposesDraw = False
                        else:
                            game.proposeDraw('black')
                        break

                elif event.type == pygame.KEYDOWN:
                    if len(moveList) > 28:
                        if event.key == pygame.K_DOWN:
                            scrollPosition = scrollPosition - 1 if scrollPosition > 29 else 28
                        elif event.key == pygame.K_UP:
                            scrollPosition = scrollPosition + 1 if scrollPosition < len(moveList) else len(moveList)
                    else:
                        if event.key == pygame.K_q:
                            promotionChoice = 'q'
                        elif event.key == pygame.K_r:
                            promotionChoice = 'r'
                        elif event.key == pygame.K_b:
                            promotionChoice = 'b'
                        elif event.key == pygame.K_n:
                            promotionChoice = 'n'
                        else:
                            clickedSquare = None
                            moveToSquare = None
                            promotionWaiting = False

                    if promotionWaiting:
                        game.move(f'{clickedSquare}{moveToSquare}{promotionChoice}')
                        clickedSquare = None
                        promotionWaiting = False

        clock.tick(30)
        pygame.display.update()
        await asyncio.sleep(0)

asyncio.run(main())

# Chess unicode font found at https://www.fonts4free.net/chess-condal-font.html
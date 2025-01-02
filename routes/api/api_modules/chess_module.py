import chess

async def get_board():
    board = chess.Board()
    return board

async def 

if __name__ == "__main__":
    board = chess.Board()
    print(board)

    move = chess.Move.from_uci("e2e4")
    board.set_piece_at(chess.E2, board.re)

    print(board)
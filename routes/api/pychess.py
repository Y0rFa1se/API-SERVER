from fastapi import APIRouter, HTTPException
from typing import Optional
from .api_modules.pychess import Chess
from .api_modules.gpt import render_system_requests, openai_request

import os

async def request_move(password, board):
    board_state, turn, board_fen, san_history, legal_moves = board.get_info()

    system_query = f"""You are playing as {turn}.
You MUST answer in following format:

SAN(Standard Algebraic Notation) of the move you want to make.
short comment about the move.

Example:

Nf3
Developed the pawn to control the center and opened the path for the bishop.

This is current state of the board:

{board_state}

This is fen of the board:

{board_fen}

This is the history of the moves:

{san_history}
"""
    
    system_query = await render_system_requests(system_query)
    response = await openai_request(password, system_query)

    move, comment = response.split("\n")
    move = move.strip()

    return move, comment

router = APIRouter()

@router.get("/san_history/{san_history}")
async def san_history(password: str, san_history: str, guide: Optional[bool]=False, ascii: Optional[bool]=False):
    if password != os.getenv("GUEST_PASSWORD"):
        return "Invalid password"
    
    board = Chess(guide=guide, ascii=ascii)

    for san in san_history.split(" "):
        board.play_with_illegal(san)

    return str(board)

@router.get("/san_history_to_fen/{san_history}")
async def san_history_to_fen(password: str, san_history: str):
    if password != os.getenv("GUEST_PASSWORD"):
        return "Invalid password"
    
    board = Chess()

    for san in san_history.split(" "):
        board.play_with_illegal(san)

    return board.get_fen()

@router.get("/play_with_gpt")
async def play_with_gpt(password: str, uci_move: str, san_history: Optional[str]=None):
    if password != os.getenv("GUEST_PASSWORD"):
        return "Invalid password"
    
    board = Chess()
    if san_history:
        san_history = san_history.split(" ")
    else:
        san_history = []

    print(san_history)
    print(len(san_history))
    for idx in range(len(san_history)):
        if idx % 2 == 0:
            try:
                board.play_uci_with_auto_promotion(san_history[idx])
            except:
                raise HTTPException(status_code=400, detail="Illegal move history")
        else:
            board.play_with_illegal(san_history[idx])

    try:
        board.play_uci_with_auto_promotion(uci_move)
    except:
        raise HTTPException(status_code=400, detail="Illegal move")

    move, comment = await request_move(password, board)
    board.play_with_illegal(move)

    return {"board_fen": board.get_fen(), "san_history": board.get_san(), "comment": comment, "raw_san_history": board.get_raw_san()}

@router.get("/gpt_move/{san_history}")
async def gpt_move(password: str, san_history: str):
    if password != os.getenv("GUEST_PASSWORD"):
        return "Invalid password"
    
    board = Chess()

    for san in san_history.split(" "):
        board.play_with_illegal(san)

    move, comment = await request_move(password, board)

    return {"move": move, "comment": comment}
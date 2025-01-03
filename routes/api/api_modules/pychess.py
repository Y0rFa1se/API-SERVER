import chess
import re

class Chess:
    guide = True
    ascii = False
    board = None
    san_history = []
    fen_history = []
    san_pattern = re.compile(r"([pRNBQK])?([a-h])?([1-8])?(x)?([a-h])([1-8])( ?e\.?p\.? ?)?(=[RNBQ])?([+#])?", re.IGNORECASE)
    rank = {"1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6, "8": 7}
    file = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

    def __init__(self, init_fen: str = None, guide: bool=False, ascii: bool=False) -> None:
        self.guide = guide
        self.ascii = ascii
        if init_fen:
            self.board = chess.Board(init_fen)
        else:
            self.board = chess.Board()

    def __str__(self) -> str:
        board_str_ret = ""
        board_str = self.board.unicode() if not self.ascii else str(self.board)
        for idx, rank in enumerate(board_str.split("\n")):
            if self.guide:
                board_str_ret += f"{8-idx} | "
            
            for idx, square in enumerate(rank.split(" ")):
                board_str_ret += square + " "
            board_str_ret += "\n"

        if self.guide:
            cur_fen = self.board.fen()
            _, turn, castling_rights, en_passant_square, halfmove_counter, fullmove_counter = cur_fen.split(" ")
            board_str_ret += "   ----------------\n"
            board_str_ret += "    A B C D E F G H\n\n"
            board_str_ret += f"Turn:{turn:>15}\n"
            board_str_ret += f"Castling:{castling_rights:>11}\n"
            board_str_ret += f"En Passant:{en_passant_square:>9}\n"
            board_str_ret += f"Halfmove:{halfmove_counter:>11}\n"
            board_str_ret += f"Fullmove:{fullmove_counter:>11}\n\n"
            board_str_ret += f"FEN: {cur_fen}\n\n"
            board_str_ret += f"SAN: {self.get_san()}\n"

        return board_str_ret
    
    def reset(self) -> None:
        self.board.reset()
        self.san_history = []
        self.fen_history = []
    
    def get_fen(self) -> str:
        return self.board.fen()
    
    def get_san(self) -> str:
        san = ""

        for idx, move in enumerate(self.san_history):
            if idx % 2:
                san += f"{str((idx // 2) + 1)}...{move} "
            else:
                san += f"{str((idx // 2) + 1)}.{move} "

        return san
    
    def get_raw_san(self) -> str:
        ret = ""
        for san in self.san_history:
            ret += san + " "

        return ret
    
    def get_fen_history(self, idx: int) -> str:
        return self.fen_history[idx]
    
    def render_fen(self, fen: str) -> str:
        return chess.Board(fen).unicode() if not self.ascii else str(chess.Board(fen))

    def get_info(self, contain_legal_moves: bool=False) -> tuple:
        board_state = str(self.board.unicode())
        turn = "white" if self.board.turn else "black"
        board_fen = self.board.fen()
        san_history = self.get_san()

        if contain_legal_moves:
            legal_moves = self.legal_move()
        else:
            legal_moves = None

        return (board_state, turn, board_fen, san_history, legal_moves)

    def legal_move(self) -> list:
        legal_moves = self.board.legal_moves

        return [move.uci() for move in legal_moves]
    
    def is_legal(self, move: str) -> bool:
        try:
            move = self.board.parse_san(move)
            return move in self.board.legal_moves

        except:
            return False
    
    def decode_san(self, san: str) -> tuple:
        move = ""
        encoded_san = ""

        match = self.san_pattern.match(san)
        
        piece = match.group(1)
        file = match.group(2)
        rank = match.group(3)
        capture = match.group(4)
        dest_file = match.group(5)
        dest_rank = match.group(6)
        ep = match.group(7)
        promotion = match.group(8)
        check = match.group(9)

        if not piece:
            piece = ""
            move_piece = self.turn_piece("p")
            move = self.turn_piece("p")
        else:
            move_piece = self.turn_piece(piece)
            move = self.turn_piece(piece)
        if not promotion:
            promotion = ""
            move_promotion = ""
        else:
            move_promotion = self.turn_piece(promotion[1])
            move = self.turn_piece(piece)+dest_file+dest_rank+move_promotion
        if not capture:
            capture = ""
        if ep:
            ep = "e.p."
        else:
            ep = ""

        move += dest_file+dest_rank

        if not file:
            file = ""
            if not rank:
                rank = ""
                move_coord = self.find_piece(move_piece, chess.parse_square(dest_file+dest_rank))
            
            else:
                move_coord = self.find_piece_rank(move_piece, rank)

        elif not rank:
            rank = ""
            move_coord = self.find_piece_file(move_piece, file)

        else:
            move = piece+file+rank+dest_file+dest_rank+move_promotion

        if self.board.piece_at(chess.parse_square(dest_file+dest_rank)):
            capture = "x"

        encoded_san = piece+file+rank+capture+dest_file+dest_rank+ep+promotion+self.check()

        return move_coord, move, encoded_san
    
    def play(self, san: str) -> None:
        move = self.board.parse_san(san)
        move = self.board.san(move)
        self.san_history.append(move)

        self.board.push_san(san)
        self.fen_history.append(self.board.fen())

    def play_uci(self, uci: str) -> None:
        move = chess.Move.from_uci(uci)
        move = self.board.san(move)
        self.san_history.append(move)

        self.board.push_uci(uci)
        self.fen_history.append(self.board.fen())

    def play_uci_with_auto_promotion(self, uci: str) -> None:
        if self.board.piece_at(chess.parse_square(uci[:2])) == chess.Piece.from_symbol(self.turn_piece("p")) and (uci[3] == "1" or uci[3] == "8"):
            uci += "q"

        self.play_uci(uci)

    def play_uci_with_illegal(self, uci: str) -> None:
        if uci[:2] == uci[2:]:
            return

        uci = chess.Move.from_uci(uci)
        self.board.push(uci)

        self.turn_end()

    def turn_piece(self, piece: str) -> str:
        return piece.upper() if self.board.turn else piece.lower()

    def castling(self, move: str) -> None:
        if move.startswith("O-O-O") or move.startswith("0-0-0") or move.startswith("o-o-o"):
            if self.board.turn:
                king_coord = self.find_piece(self.turn_piece("K"), chess.E1)
                rook_coord = self.find_piece(self.turn_piece("R"), chess.A1)

                self.delete_piece(king_coord)
                self.delete_piece(rook_coord)
                self.board.set_piece_at(chess.C1, chess.Piece.from_symbol(self.turn_piece("K")))
                self.board.set_piece_at(chess.D1, chess.Piece.from_symbol(self.turn_piece("R")))

            else:
                king_coord = self.find_piece(self.turn_piece("K"), chess.E8)
                rook_coord = self.find_piece(self.turn_piece("R"), chess.A8)

                self.delete_piece(king_coord)
                self.delete_piece(rook_coord)
                self.board.set_piece_at(chess.C8, chess.Piece.from_symbol(self.turn_piece("K")))
                self.board.set_piece_at(chess.D8, chess.Piece.from_symbol(self.turn_piece("R")))

            self.fen_history.append(self.board.fen())
            self.san_history.append("O-O-O"+self.check())

        else:
            if self.board.turn:
                king_coord = self.find_piece(self.turn_piece("K"), chess.E1)
                rook_coord = self.find_piece(self.turn_piece("R"), chess.H1)

                self.delete_piece(king_coord)
                self.delete_piece(rook_coord)
                self.board.set_piece_at(chess.G1, chess.Piece.from_symbol(self.turn_piece("K")))
                self.board.set_piece_at(chess.F1, chess.Piece.from_symbol(self.turn_piece("R")))

            else:
                king_coord = self.find_piece(self.turn_piece("K"), chess.E8)
                rook_coord = self.find_piece(self.turn_piece("R"), chess.H8)

                self.delete_piece(king_coord)
                self.delete_piece(rook_coord)
                self.board.set_piece_at(chess.G8, chess.Piece.from_symbol(self.turn_piece("K")))
                self.board.set_piece_at(chess.F8, chess.Piece.from_symbol(self.turn_piece("R")))

            self.fen_history.append(self.board.fen())
            self.san_history.append("O-O"+self.check())

        self.turn_end()

    def play_with_illegal(self, move: str) -> bool:
        if move.startswith("O-O") or move.startswith("0-0") or move.startswith("o-o"):
            self.castling(move)
            
            return True
        
        try:
            move_coord, move, encoded_san = self.decode_san(move)
        except:
            return False

        self.delete_piece(move_coord)
        self.board.set_piece_at(chess.parse_square(move[1:]), chess.Piece.from_symbol(self.turn_piece(move[0])))

        self.fen_history.append(self.board.fen())
        self.san_history.append(encoded_san)
        self.turn_end()

        return True
        
    def check(self) -> str:
        if self.board.is_checkmate():
            return "#"
        
        if self.board.is_check():
            return "+"
        
        return ""

    def find_piece(self, piece: str, center: chess.Square) -> chess.Square:
        nearest_square = None
        min_distance = 1000000

        center_rank, center_file = divmod(center, 8)

        for square in chess.SQUARES:
            if str(self.board.piece_at(square)) == piece:
                square_rank, square_file = divmod(square, 8)
                distance = (center_rank - square_rank) ** 2 + (center_file - square_file) ** 2

                if distance < min_distance:
                    min_distance = distance
                    nearest_square = square

        return nearest_square
    
    def find_piece_rank(self, piece: str, rank: str) -> chess.Square:
        for square in chess.SQUARES:
            if str(self.board.piece_at(square)) == piece and square // 8 == self.rank[rank]:
                return square
        
        return None
    
    def find_piece_file(self, piece: str, file: str) -> chess.Square:
        for square in chess.SQUARES:
            if str(self.board.piece_at(square)) == piece and square % 8 == self.file[file]:
                return square
        
        return None
    
    def delete_piece(self, square: chess.Square) -> bool:
        if square:
            self.board.remove_piece_at(square)
            return True
        
        return False

    def turn_end(self) -> None:
        self.board.push(chess.Move.null())

    def make_illegal_move(self, move: str) -> None:
        self.play_with_illegal(move)
        print(self)

    def make_move(self, move: str) -> None:
        self.play(move)
        print(self)

    def make_uci_move(self, move: str) -> None:
        self.play_uci(move)
        print(self)

    def game_result(self):
        if self.find_piece("K", chess.E1) is None:
            return "0-1"
        elif self.find_piece("k", chess.E8) is None:
            return "1-0"
        
        return self.board.result()
    
    def is_ended(self):
        if self.find_piece("K", chess.E1) is None or self.find_piece("k", chess.E8) is None:
            return True
        
        return self.board.is_game_over()
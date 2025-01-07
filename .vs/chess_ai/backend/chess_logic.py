from typing import Any
import chess
import chess.engine
from stockfish import Stockfish


class ChessGame:
    def __init__(self):
        self.board = chess.Board()

    def make_move(self, move: str):
        try:
            move_obj = chess.Move.from_uci(move)  # Corrected typo
            if move_obj in self.board.legal_moves:
                self.board.push(move_obj)
                return True, self.board.fen()
            else:
                return False, "Illegal move"
        except Exception as e:
            return False, f"Invalid move format: {e}"

    def get_board_state(self):
        return self.board.fen()  # FEN represents the board state


def evaluate_board(board: chess.Board) -> int:
    if board.is_checkmate():
        return -9999 if board.turn else 9999
    elif board.is_stalemate() or board.is_insufficient_material():
        return 0
    else:
        return sum(piece_value.get(piece.piece_type, 0) for piece in board.piece_map().values())


piece_value = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0,
}


def minimax(board: chess.Board, depth: int, maximizing: bool) -> int:
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing:
        max_eval = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, False)
            board.pop()
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, True)
            board.pop()
            min_eval = min(min_eval, eval)
        return min_eval


# Stockfish Integration
stockfish = Stockfish(path="/path/to/stockfish")  # Update with actual path

# Example Usage with Stockfish
game = ChessGame()
stockfish.set_fen_position(game.board.fen())  # Corrected reference to self.board
best_move = stockfish.get_best_move()
print(f"Best move by Stockfish: {best_move}")

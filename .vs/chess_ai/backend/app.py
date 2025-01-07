from flask import Flask, request, jsonify
from chess_logic import ChessGame, minimax  # Import minimax function
from stockfish import Stockfish

app = Flask(__name__)
game = ChessGame()

# Initialize Stockfish (if used)
stockfish = Stockfish(path="/path/to/stockfish")  # Update with the actual path


@app.route('/make-move', methods=['POST'])
def make_move():
    data = request.json
    move = data.get("move")
    
    # Validate input
    if not move or not isinstance(move, str):
        return jsonify({"success": False, "error": "Invalid move format"}), 400

    # Attempt to make the move
    success, state = game.make_move(move)
    if success:
        return jsonify({"success": success, "state": state})
    else:
        return jsonify({"success": success, "error": state}), 400


@app.route('/ai-move', methods=['GET'])
def ai_move():
    try:
        # Example: Using minimax for AI decision (adjust depth as needed)
        best_move = None
        depth = 2  # Set minimax search depth
        max_score = float('-inf')

        for move in game.board.legal_moves:
            game.board.push(move)
            score = minimax(game.board, depth - 1, False)
            game.board.pop()

            if score > max_score:
                max_score = score
                best_move = move

        if not best_move:
            return jsonify({"error": "No legal moves available"}), 400

        # Make the move on the game board
        game.board.push(best_move)

        # Return the updated board state
        return jsonify({"success": True, "state": game.get_board_state()})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)



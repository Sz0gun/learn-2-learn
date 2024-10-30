import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import chess
import chess.svg
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

import cairosvg

TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

if TELEGRAM_API_TOKEN is None:
    raise ValueError("No TELEGRAM_API_TOKEN provided")
# Setting up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize chess board
game_board = chess.Board()

# Chat environments
environment_white_ai_chat = []
environment_black_ai_chat = []
shared_chat = []

# Start command - initiates the chess game and presents the user with the option to start using WebApp.
def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    web_app_url = "https://github.com/Sz0gun/learn-2-learn.git"  # Using GitHub to host the HTML5 chess game
    keyboard = [
        [InlineKeyboardButton("Start Chess Game", web_app=WebAppInfo(url=web_app_url))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Hi! Ready for a game of chess?', reply_markup=reply_markup)

# Button click handler for starting game - handles the button click event to start the game.
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    if query.data == 'start_game':
        # Show initial board state once the game is started
        await send_board_state(query)

# Function to get the current board state in SVG format and convert it to PNG for display in Telegram.
def get_board_image() -> str:
    svg_data = chess.svg.board(game_board)
    cairosvg.svg2png(bytestring=svg_data, write_to="current_board.png")
    return "current_board.png"

# Function to send the current board state - displays the board state as an image.
async def send_board_state(query):
    # Note: Now, the board state is displayed as an image using Telegram's send_photo method.
    board_image_path = get_board_image()
    await query.message.reply_photo(photo=open(board_image_path, 'rb'), caption=f"Your move, {query.from_user.first_name}!")

# Handle chess moves submitted by users via command - takes a user's move, validates it, and updates the board.
async def move(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_move = ' '.join(context.args)
    try:
        # Convert the user's input to a chess move
        move = chess.Move.from_uci(user_move)
        # Check if the move is legal in the current board state
        if move in game_board.legal_moves:
            game_board.push(move)  # Make the move on the board
            await update.message.reply_text(f"Move {user_move} has been made.")
            # Update the board state after the move
            await send_board_state(update.message)
        else:
            await update.message.reply_text("Illegal move. Try again.")
    except ValueError:
        await update.message.reply_text("Invalid move format. Use UCI format, e.g., e2e4.")

# Handle chat messages for different environments - supports different chat environments (White AI, Black AI, Shared).
async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    user_name = update.message.from_user.first_name
    
    # Determine which chat environment is active for the user
    if context.chat_data.get('environment') == 'white_ai':
        environment_white_ai_chat.append(f"{user_name}: {user_message}")
        await update.message.reply_text(f"(White AI Chat) {user_name}: {user_message}")
    elif context.chat_data.get('environment') == 'black_ai':
        environment_black_ai_chat.append(f"{user_name}: {user_message}")
        await update.message.reply_text(f"(Black AI Chat) {user_name}: {user_message}")
    else:
        shared_chat.append(f"{user_name}: {user_message}")
        await update.message.reply_text(f"(Shared Chat) {user_name}: {user_message}")


# Command to switch chat environment - allows the user to change between different chat environments.
async def set_chat_environment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    environment = ' '.join(context.args).lower()
    if environment == 'white':
        context.chat_data['environment'] = 'white_ai'
        await update.message.reply_text("You are now in the White AI Chat environment.")
    elif environment == 'black':
        context.chat_data['environment'] = 'black_ai'
        await update.message.reply_text("You are now in the Black AI Chat environment.")
    elif environment == 'shared':
        context.chat_data['environment'] = 'shared'
        await update.message.reply_text("You are now in the Shared Chat environment.")
    else:
        await update.message.reply_text("Unknown environment. Please use 'white', 'black', or 'shared'.")

# Main function to add handlers and run the bot - sets up command handlers and starts the bot.
async def main() -> None:
    application = ApplicationBuilder().token("TELEGRAM_API_TOKEN").build()
    
    # Command handler to start the game
    application.add_handler(CommandHandler('start', start))
    # Callback handler for buttons (e.g., start game button)
    application.add_handler(CallbackQueryHandler(button_handler))
    # Command handler to handle moves
    application.add_handler(CommandHandler('move', move))
    # Command handler to set chat environment
    application.add_handler(CommandHandler('set_chat', set_chat_environment))
    # Message handler to handle chat messages in different environments
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_handler))
    
    # Start polling to interact with Telegram
    await application.run_polling()

# Run the main function in the current event loop
if __name__ == '__main__':
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.get_event_loop()
        asyncio.set_event_loop(loop)
        
    loop.run_until_complete(main())
    # Placeholder for additional functionality or handlers if needed in the future.
# Note:
# The `logging` module is part of Python's standard library, so no additional dependency is required for this.
# To render SVG images of the chess board as PNG for Telegram, we use `cairosvg`.
# You can add `cairosvg` to your dependencies with Poetry using:
#   `poetry add cairosvg`
# Dependencies to add:
# - `python-telegram-bot`: Required to interact with Telegram's Bot API.
# - `python-chess`: Required for handling chess logic.
# - `cairosvg`: Used for rendering SVG images of the chess board to PNG.

# If you are experiencing issues with Pylance not resolving imports such as `telegram`, ensure you have installed `python-telegram-bot` using:
#   `poetry add python-telegram-bot`
# Also, make sure your Python environment in VSCode matches the environment in which dependencies are installed.

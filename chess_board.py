import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import os
from dotenv import load_dotenv
import nest_asyncio
import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# Load environment variables
load_dotenv()

TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

if TELEGRAM_API_TOKEN is None:
    raise ValueError("No TELEGRAM_API_TOKEN provided")

# Setting up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app setup
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def serve_chess():
    return HTMLResponse(content="<h1>Welcome to the Chess Game!</h1><p>Game is currently under construction.</p>", status_code=200)

# Chat environments
environment_white_ai_chat = []
environment_black_ai_chat = []
shared_chat = []

# Start command - initiates the chess game and presents the user with the option to start using WebApp.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    web_app_url = "https://szogun.github.io/learn-2-learn/chess_index.html"  # Update with the HTTPS URL hosted on GitHub Pages
    keyboard = [
        [InlineKeyboardButton("Start Chess Game", web_app=WebAppInfo(url=web_app_url))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Hi! Ready for a game of chess?', reply_markup=reply_markup)

# Button click handler for starting game - handles the button click event to start the game.
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    if query.data == 'start_game':
        # Show initial board state once the game is started
        await update.message.reply_text("Game started! Use /move to make your move.")

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
    application = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()
    
    # Command handler to start the game
    application.add_handler(CommandHandler('start', start))
    # Callback handler for buttons (e.g., start game button)
    application.add_handler(CallbackQueryHandler(button_handler))
    # Command handler to set chat environment
    application.add_handler(CommandHandler('set_chat', set_chat_environment))
    # Message handler to handle chat messages in different environments
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_handler))
    
    # Ensure the event loop can be nested
    nest_asyncio.apply()
    
    # Start polling to interact with Telegram
    await application.run_polling()

# Run FastAPI server
if __name__ == "__main__":
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:  # No running event loop
        loop = None

    if loop and loop.is_running():
        print('Async event loop already running. Using existing event loop.')
        loop.create_task(main())  # Use the existing event loop
    else:
        # Start FastAPI server in a separate task
        loop = asyncio.get_event_loop()
        loop.create_task(main())
        uvicorn.run(app, host="0.0.0.0", port=8000)

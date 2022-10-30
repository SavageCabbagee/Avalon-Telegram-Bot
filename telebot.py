from game import Game
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from dotenv import dotenv_values

config = dotenv_values(".env")
BOT_KEY = config['BOT_API']

async def creategame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global game
    if 'game' not in globals() or game == None:
        game = Game(0)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Game created!")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Game already exists!")

async def cancelgame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global game
    if 'game' not in globals() or game == None:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Game does not exist")
    else:
        game = None
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Game canceled!")    

def main():
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = ApplicationBuilder().token(BOT_KEY).build()
    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("creategame", creategame))
    application.add_handler(CommandHandler("cancelgame", cancelgame))
    application.add_handler(CommandHandler("startgame", startgame))
    # application.add_handler(CommandHandler("join", removealert))
    # application.add_handler(CommandHandler("leave", getalert))
    
    #bot = application.bot
    # Run the bot until the user presses Ctrl-C
    application.run_polling()



if __name__ == '__main__':    
    main()
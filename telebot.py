from game import Game
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

from dotenv import dotenv_values
# split up new_leader and voting into its own function
config = dotenv_values(".env")
BOT_KEY = config['BOT_API']

def board_state(wins, rejects):
    global game
    return(
        f"--- Quests ---\n"
        f"{' '.join([chr(9989) if i == 1 else chr(10060) if i==0 else chr(11036) for i in wins])}\n"
        f"--- Reject count ---\n"
        f"{' '.join([chr(10060) for i in range(rejects)])} {' '.join([chr(11036) for i in range(5 - rejects)])}\n"
        f"--- Order of leaders ---\n"
        f"{chr(10145).join([player.name for player in game.players])} {chr(128260)}"
        f"--- Current Leader ---\n"
        f"{game.current_leader.name}\n"
    )

def inline_keyboard_for_choosing_players(chosen):
    global game
    keyboard = [ #should be index 
        [InlineKeyboardButton(f"{player.name}", callback_data='choose_player {idx}')]  for idx,player in enumerate(game.players) if player not in game.chosen_players
    ]

    return(InlineKeyboardMarkup(keyboard))

def inline_keyboard_for_voting():
    global game
    keyboard = [ #should be index 
        [InlineKeyboardButton(f"Yes", callback_data='voting {index} 1')],
        [InlineKeyboardButton(f"No", callback_data='voting {index} 0')]
    ]

    return(InlineKeyboardMarkup(keyboard)) 

def inline_keyboard_for_quest():
    global game
    keyboard = [ 
        [InlineKeyboardButton(f"Success", callback_data='quest 1')],
        [InlineKeyboardButton(f"Failure", callback_data='quest 0')]
    ]

    return(InlineKeyboardMarkup(keyboard)) 

def inline_keyboard_for_assassin():
    global game
    keyboard = [ #should be index 
        [InlineKeyboardButton(f"{player.name}", callback_data='assassin {idx}')]  for idx,player in enumerate(game.players)
    ]

    return(InlineKeyboardMarkup(keyboard))

async def new_leader(index, update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_leader = game.determine_leader(index)
    newline_char = '\n'
    if new_leader == True:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text=f"Game Over! The forces of Evil has won by causing 3 Quests to fail!\n\n{newline_char.join([f'{player.name}{chr(39)}s secret role was {player.role}' for player in game.players])}"
            )
    elif new_leader == False:
        # assassin trigger
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text=f"Good has completed 3 quests successfully but Evil has 1 last chance to win.\nAssassin {game.assassin.name}, choose who you think is Merlin"
        )
        await context.bot.send_message(
            chat_id=game.assassin.id, 
            text=f"Choose who you think is Merlin.",
            reply_markup= inline_keyboard_for_assassin()
        )
    else:
        await context.bot.send_message(
                chat_id=game.currrent_leader.id, 
                text=f"You are the current leader.\nFor Quest {game.game_phase+1}, {game.players_needed} players are needed. Please choose player {len(game.chosen_players)+1}",
                reply_markup=inline_keyboard_for_choosing_players(game.chosen_players)
                )

async def quest_success_failure(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for player in game.chosen_players:
        await context.bot.send_message(
            chat_id=game.player.id,
            text=f"You have embarked Quest {game.game_phase + 1}\n Please choose whether you want the quest to succeed or fail.",
            reply_markup=inline_keyboard_for_quest()
        )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    global game
    global chatid

    query = update.callback_query

    data = query.data
    text = data.split(" ")

    await query.answer()

    if text[0] == 'choose_player':
        game.choose_player(int(text[1]))
        if len(game.chosen_players) == game.player_needed:
            await context.bot.send_message(chat_id=chatid, text=f"{game.current_leader.id} has chosen {' '.join([player.name for player in game.chosen_players])}\nPlease vote for the choice!")
            await query.edit_message_text(text=f"You have chosen {' '.join([player.name for player in game.chosen_players])}")
            for idx, player in enumerate(game.players):
                await context.bot.send_message(
                    chat_id=player.id, 
                    text=f"{game.current_leader.id} has chosen {' '.join([player.name for player in game.chosen_players])}\nPlease vote for the choice!",
                    reply_markup=inline_keyboard_for_voting(idx)
                )
        else:
            await query.edit_message_text(
                text=f"You are the current leader.\nFor Quest {game.game_phase+1}, {game.players_needed} players are needed. Please choose player {len(game.chosen_players)+1}",
                reply_markup=inline_keyboard_for_choosing_players(game.chosen_players)
            )

    if text[0] == 'voting':
        game.voting(int(text[1],int(text[2])))
        await query.edit_message_text(text=f"You have voted {'Yes' if text[2]== 1 else 'No'}")
        newline_char = '\n'
        if None not in game.votes:
            await context.bot.send_message(
                chat_id=chatid, 
                text=f"{newline_char.join([f'{game.players[idx].name} voted Yes!' if vote == 1 else f'{game.players[idx].name} voted No!' for idx,vote in game.votes])}"
                )
            if sum(game.votes)/len(game.votes) > 0.5:
                await context.bot.send_message(
                chat_id=chatid, 
                text=f'Vote passed!\nStarting Quest {game.game_phase + 1}'
                )
            else:
                await context.bot.send_message(
                chat_id=chatid, 
                text=f'Vote failed! Moving to next leader in line!'
                )
                await context.bot.send_message(chat_id=update.effective_chat.id, text=board_state(game.quest_count,game.reject_count))
                new_leader(game.players.index(game.current_leader)+1)
                await context.bot.send_message(
                    chat_id=game.currrent_leader.id, 
                    text=f"You are the current leader.\nFor Quest {game.game_phase+1}, {game.players_needed} players are needed. Please choose player {len(game.chosen_players)+1}",
                    reply_markup=inline_keyboard_for_choosing_players(game.chosen_players)
                    )
            game._votes = [None for i in game.players]
    
    if text[0] == "quest":
        await query.edit_message_text(text=f"You have chosen {'Success' if text[1]== 1 else 'Failure'}")
        if len(game._quest_success) == game.player_needed:
            if game._quest_success.count(0) >= game.failure_needed:
                await context.bot.send_message(
                    chat_id=chatid,
                    text=f"There were {game._quest_success.count(1)} success and {game._quest_success.count(0)} failures.\nQuest {game.game_phase + 1} Failed"
                )
                print(game._quest_success)
                print(f'Quest {game.game_phase + 1} Failed')
                game.determine_leader(game.players.index(game.current_leader)+1)
            else:
                print(game._quest_success)
                await context.bot.send_message(
                    chat_id=chatid,
                    text=f"There were {game._quest_success.count(1)} success and {game._quest_success.count(0)} failures.\nQuest {game.game_phase + 1} Succeeded"
                )
                print(f'Quest {game.game_phase + 1} Succeeded')
                game.determine_leader(game.players.index(game.current_leader)+1)

    if text[0] == "assassin":
        await query.edit_message_text(text=f"You have chosen {game.players[int(text[1])].name}")
        newline_char = '\n'
        if game.assassin_trigger(int(text[1])):
            await context.bot.send_message(
            chat_id=chatid, 
            text=f"Game Over! The forces of Evil has won by killing Merlin!\n\n{newline_char.join([f'{player.name}{chr(39)}s secret role was {player.role}' for player in game.players])}"
            )
        else:
            await context.bot.send_message(
            chat_id=chatid, 
            text=f"Game Over! Good has triumphed over Evil by completing 3 Quests successfully!\n\n{newline_char.join([f'{player.name}{chr(39)}s secret role was {player.role}' for player in game.players])}"
            )
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery

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
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No game to cancel!")
    else:
        game = None
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Game canceled!")    

async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global game
    if 'game' not in globals() or game == None:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No game to join!")
    else:
        print(update.message)
        added = game.add_player(update.message['from']['id'],update.message['from']['first_name'])
        if added == 0:
            if game.number_of_players >= 5:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{update.message['from']['first_name']} has joined the game. Type /startgame if this was the last player and you want to start with {game.number_of_players} players!")
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{update.message['from']['first_name']} has joined the game. There is currently {game.number_of_players} players in the game and you need 5-10 players.")
            await context.bot.send_message(chat_id=update.message['from']['id'], text=f"You joined a game in {update.message['chat']['title']}. I will soon tell you your secret role.")
        elif added == 1:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"You already joined the game, {update.message['from']['first_name']}!")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Sorry {update.message['from']['first_name']}, the game is already full.")
 
async def remove_player(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global game
    if 'game' not in globals() or game == None:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No game to leave!")
    else:
        lefted = game.remove_player(update.message['from']['id'])
        if lefted:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{update.message['from']['first_name']} left the game")
        elif lefted == 2:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"You are not in the game, {update.message['from']['first_name']}!")

async def startgame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global game
    global chatid
    if 'game' not in globals() or game == None:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No game to start!")
    else:
        started = game.start_game()
        chatid = update.effective_chat.id
        if not started:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Not enough players! At least 5 players is needed to start the game. Current player count: {game.number_of_players}")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Game Started!")
            for player in game.players:
                if player.side == 'Evil':
                    await context.bot.send_message(chat_id=player.id, text=f"Your secret role is {player.role}\nYour side is {player.side}\nYour fellow Minions of Modred are: {' '.join([player_.name for player_ in game.players if player_.side == 'Evil' and player_ != player])}")
                if player.role == 'Merlin':
                    await context.bot.send_message(chat_id=player.id, text=f"Your secret role is {player.role}\nYour side is {player.side}\nThe Minions of Modred are: {' '.join([player_.name for player_ in game.players if player.side == 'Evil'])}")
                else:
                    await context.bot.send_message(chat_id=player.id, text=f"Your secret role is {player.role}\nYour side is {player.side}")
            await context.bot.send_message(chat_id=update.effective_chat.id, text=board_state(game.quest_count,game.reject_count))
            new_leader(0, update=update, context=context)

async def board(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global game
    if 'game' not in globals() or game == None or game.game_phase == None:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No running game!")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=board_state(game.quest_count,game.reject_count))

def main():
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = ApplicationBuilder().token(BOT_KEY).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("creategame", creategame))
    application.add_handler(CommandHandler("cancelgame", cancelgame))
    application.add_handler(CommandHandler("startgame", startgame))
    application.add_handler(CommandHandler("join", join))
    application.add_handler(CommandHandler("leave", remove_player))
    application.add_handler(CommandHandler("board", board))
    application.add_handler(CallbackQueryHandler(button))

    #bot = application.bot
    # Run the bot until the user presses Ctrl-C
    application.run_polling()



if __name__ == '__main__':    
    main()
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, InlineQueryHandler, ConversationHandler
from handlers import start, convstarthandler, MessagesInConv, end_conversation, daily_backup, randomwisdom, daily_vaultprikol, pathtoids, vaultsubscription, unsubscribe
import datetime
bot = Bot(token="6448384941:AAEw1q8FTJrzyNPgu44_f_VAWkseFx--clo")
bot_token = "6448384941:AAEw1q8FTJrzyNPgu44_f_VAWkseFx--clo"


def main():
    updater = Updater(bot_token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler("convstart", convstarthandler)],
        states={'started': [MessageHandler(Filters.text & ~Filters.command, MessagesInConv)]},
        fallbacks=[MessageHandler(Filters.command, end_conversation)],
    ))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("subscribe_vault", vaultsubscription))
    dp.add_handler(CommandHandler("unsubscribe", unsubscribe))
    updater.start_polling()
    updater.job_queue.run_repeating(daily_backup, context=(updater.bot), interval=3600*24, first=1)
    updater.job_queue.run_repeating(daily_vaultprikol, context=(updater.bot), interval=3600 * 24)
    updater.idle()

if __name__ == '__main__':
    main()

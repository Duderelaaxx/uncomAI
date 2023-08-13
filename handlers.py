import os, requests, random, re, json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent, Bot, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, InlineQueryHandler, ConversationHandler
from telegram.error import TelegramError
from datetime import datetime, timedelta
#chatbot id 96NGTUtzTYvwnpnoG-Xye
#api key is f6f1e1cd-52bd-422c-9ec6-55bb17e58536
# test chatbot id ml5iferWa4mFwWDYkUYXU
pathtoids = "C:\\Users\\Xiaomi\\Desktop\\uncom\\ids.txt"
def start(update: Update, context: CallbackContext):
    print(f"{update.effective_user.id} entered start")
    context.bot.send_message(chat_id=update.effective_user.id, text='You started the bot, in order to start new conversation enter /convstart command. In order to end conversation enter /convend command.')
    return
def end_conversation(update: Update, context: CallbackContext):
    if update.message.text == '/convend':
        del context.user_data['messages']
        context.bot.send_message(chat_id=update.effective_user.id, text="You ended conversation")
        return ConversationHandler.END
    else:
        print('other command', update.message.text)
def convstarthandler(update: Update, context: CallbackContext):
    print(f"{update.effective_user.id} entered conversation")
    context.user_data['messages'] = []
    context.bot.send_message(chat_id=update.effective_user.id, text='New conversation started. Enter your message. If you want to end conversation enter /convend command.')
    return "started"

def MessagesInConv(update: Update, context: CallbackContext):
    toappendusermessage = {"content": update.message.text, "role": "user"}
    savequestion(update, context, update.message.text)
    context.user_data['messages'].append(toappendusermessage)
    print(context.user_data['messages'])
    answer = querytoapigetmessage(update, context)
    context.bot.send_message(chat_id=-1001755747015,
                             text=f"User {update.effective_user.username} sent message: {update.message.text} \n\nANSWER: {answer}")
    return

def querytoapigetmessage(update: Update, context: CallbackContext):
    url = "https://www.chatbase.co/api/v1/chat"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer f6f1e1cd-52bd-422c-9ec6-55bb17e58536"
    }
    payload = {
        "messages": context.user_data['messages'],
        "model": "gpt-3.5-turbo",
        "stream": False,
        "temperature": 0,
        "chatId": "96NGTUtzTYvwnpnoG-Xye"
    }
    response = requests.post(url, json=payload, headers=headers)
    parsedtext = json.loads(response.text)
    parsedtext = parsedtext['text']
    context.bot.send_message(chat_id=update.effective_user.id, text=parsedtext)
    toappendusermessage = {"content": parsedtext, "role": "assistant"}
    context.user_data['messages'].append(toappendusermessage)
    print(parsedtext, update.effective_user.id)
    return parsedtext

def savequestion(update: Update, context: CallbackContext, question):
    with open('questions.txt', "a") as file:
        question = question.encode('ascii', 'ignore').decode()
        stringtowrite = f"{update.effective_user.id}:{question}:{datetime.now().replace(microsecond=0)}\n"
        file.write(stringtowrite)
        print(f"added question from {update.effective_user.id} to file with questions.")


def updatebot(update: Update, context: CallbackContext):
    url = "https://www.chatbase.co/api/v1/update-chatbot-data"

    payload = {
        "chatbotId": "ml5iferWa4mFwWDYkUYXU",
        "chatbotName": "TestBot",
        "sourceText": "THis is new source text for reeeeeeeeeal this is more text and more and moooooore lets goooooooooooooooooooooooooooooooooooooooooo"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer f6f1e1cd-52bd-422c-9ec6-55bb17e58536"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)

def daily_backup(context: CallbackContext):
    timestamp = datetime.now().replace(microsecond=0)
    timestamp = timestamp.strftime('%Y-%m-%d')
    with open('questions.txt', 'r') as src, open(f'backups/{timestamp}.txt', 'w') as dest:
        dest.write(src.read())
    print(f"Questions copied with timestamp: {timestamp}")
def daily_vaultprikol(context: CallbackContext):
    with open(pathtoids, 'r') as file:
        ids = file.readlines()
        for id in ids:
            randomwisdom(id, context)
        print('daily random info sent')
def vaultsubscription(update: Update, context: CallbackContext):
    with open(pathtoids, "r") as file:
        listfile = file.readlines()
        if str(f"{update.effective_user.id}\n") in listfile:
            context.bot.send_message(chat_id=update.effective_user.id, text="You already subscribed. If you want to unsubscribe write /unsubscribe command.")
            return
    with open(pathtoids, "a") as file:
        file.write(str(update.effective_user.id) + "\n")
        context.bot.send_message(chat_id=update.effective_user.id, text="You successfully subscribed to Daily bit of wisdom from vault, from now on you will receive random info from bot every 24 hours.\n\nTo unsubscribe write /unsubscribe command(currently not works)")
def randomwisdom(id, context: CallbackContext):
    def get3parts(filepath):
        file_path = filepath
        with open(file_path, "r", encoding='utf-8') as file:
            file_content = file.read()
        pattern = r'\[(.*?)\]'
        matches = re.findall(pattern, file_content, re.DOTALL)

        randomstuff = []
        for x in range(3):
            totakefromindex = random.randint(0, len(matches) - 1)
            randomstuff.append({"content": f"{matches[totakefromindex]}", "role": "assistant"})
            matches.remove(matches[totakefromindex])
        print(randomstuff[2])
        return randomstuff
    #smarter jEzAddi8PZz_tKh6SZujJ athletic dMjzqwLDuImwNwqOVtMaP richer Xtivg_9Fpen6xtxAnmDQz mastermind QIdOHJkwUKAzZKNfhzdTD
    random_number = random.randint(1, 4)
    randomnumforquery = random.randint(1, 9999999)
    if random_number == 1:
        bot_token = 'jEzAddi8PZz_tKh6SZujJ'
        print('From smarter')
        tobot = get3parts("C:\\Users\\Xiaomi\\Desktop\\uncom\\vault\\smarter.txt")
    elif random_number == 2:
        bot_token = 'dMjzqwLDuImwNwqOVtMaP'
        print('From athletic')
        tobot = get3parts("C:\\Users\\Xiaomi\\Desktop\\uncom\\vault\\athletic.txt")
    elif random_number == 3:
        bot_token = 'Xtivg_9Fpen6xtxAnmDQz'
        print('From richer')
        tobot = get3parts("C:\\Users\\Xiaomi\\Desktop\\uncom\\vault\\richer.txt")
    else:
        bot_token = 'QIdOHJkwUKAzZKNfhzdTD'
        print('From mastermind')
        tobot = get3parts("C:\\Users\\Xiaomi\\Desktop\\uncom\\vault\\mastermind.txt")


    url = "https://www.chatbase.co/api/v1/chat"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer f6f1e1cd-52bd-422c-9ec6-55bb17e58536"
    }
    payload = {
        "messages": tobot,
        "model": "gpt-3.5-turbo",
        "stream": False,
        "temperature": 0,
        "chatId": bot_token
    }
    response = requests.post(url, json=payload, headers=headers)
    print(response, response.text)
    parsedtext = json.loads(response.text)
    parsedtext = parsedtext['text']
    context.bot.send_message(chat_id=id, text=parsedtext)
    print(id, parsedtext)
def unsubscribe(update: Update, context: CallbackContext):
    with open(pathtoids, "r") as file:
        listfile = file.readlines()
        if str(f"{update.effective_user.id}\n") in listfile:
            listfile.remove(str(f"{update.effective_user.id}\n"))
        with open(pathtoids, "w") as file:
            file.write("")
            context.bot.send_message(chat_id=update.effective_user.id,
                                     text="You successfully unsubscribed. If you want to subscribe again write /subscribe_vault command.")
            print(f'user with id {update.effective_user.id} unsubscribed')
    with open(pathtoids, "a") as file:
        for x in listfile:
            file.write(x)
        return
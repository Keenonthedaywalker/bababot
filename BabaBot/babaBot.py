from datetime import datetime, timedelta
from threading import Timer, Thread
from flask import Flask, request
from telegram.ext import Updater, CommandHandler
from time import sleep
import telebot
import schedule
import random
import os

#The Token of your bot
TOKEN = "1153795040:AAGTgpa0PmCVnk2CoDK_FWC-Xlam6mfrCxQ"
#A variable for that token
bot = telebot.TeleBot(TOKEN)
#A Flask Server
server = Flask(__name__)
#Gets bot info
botInfo = bot.get_me()

#Prints that bot info
print(botInfo)

#Not quite sure what these do, but they are needed...
@bot.message_handler()
def babaIntro(intro):
    #intro.chat.id gets the user's id and with that it can send him/her messages.
    bot.send_message(intro.chat.id, "Tester")

#commands=['tasks'] will be used as a special command on Telegram, i.e. /tasks, /start, /whatever
@bot.message_handler(commands=['tasks'])
def babaTasks(tasks):
    #reply_to replies to the users message
    bot.reply_to(tasks.chat.id, "/sit\n/sleep\n/speak")
    bot.reply_to(tasks.chat.id, "Use /info to see info on the tasks")

@bot.message_handler(commands=['info'])
def babaInfo(info):
    bot.reply_to(info.chat.id, "/sit Makes BabaBot sit. \n/sleep Makes BabaBot sleep.\n/speak Makes BabaBot speak.")

@bot.message_handler(commands=['sit'])
def babaSit(sit):
    photo = open('babaSit.png', 'rb')
    #send_photo sends a photo
    bot.send_photo(sit.chat.id, photo)
   
@bot.message_handler(commands=['sleep'])
def babaSleep(sleep):
    photo = open('babaSlaap.jpg', 'rb')
    bot.send_photo(sleep.chat.id, photo)

@bot.message_handler(commands=['speak'])
def babaSpeak(speak):
    bot.reply_to(speak, "Woef")
    audio = open('babaBlaf.mp3', 'rb')
    #send_audio sends audio files
    bot.send_audio(speak.chat.id, audio)


#Selects a sentence at random and then sends that sentence to the user
def timeIsEpic():
     wordList = ["Woef", "Ek's honger. Voer My.", "AANDAG! EK SOEK AANDAG!", "Ruik ek iets lekker?", "Kos tyd! Word Wakker, plebians!", "Woef, Woef"]
     randWord = random.choice(wordList)
     bot.send_message("""Insert your own token here""", randWord)

#Stores the time 
timeList = ["9:00", "10:00", "11:00", "12:00", "13:00", "14:00",
            "15:00", "16:00", "17:00", "18:00", "19:00", "20:00"]

def earlyMorningBaba():
    photo = open('letMeOut.jpg', 'rb')
    bot.send_photo("""Insert your own token here""", photo)

#I use the Schedule module to send periodical messages
def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(0.3)

schedule.every().day.at(random.choice(timeList)).do(timeIsEpic)
schedule.every().day.at("06:00").do(earlyMorningBaba)

Thread(target=schedule_checker).start()

#This is how I run my bot on a server
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://keenon-bababot.herokuapp.com/' + TOKEN)
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

#bot.set_webhook()

#bot.polling()

import sys
sys.path.append('/home/SceduleBot/mysite/MyEnv/lib/python3.8/site-packages')
from flask import Flask, request

import ScheduleBot
import telebot
import CONST

bot = telebot.TeleBot(CONST.TOKEN, threaded=False)

SBot = ScheduleBot.ScheduleBot(bot)
app = Flask(__name__)

secretUpadate = 'asdfasdf'

@app.route('/{}'.format(CONST.SECRET), methods=['POST'])
def webhook():
    try:
        update = telebot.types.Update.de_json(
            request.stream.read().decode('utf-8'))
        print(update.message.text)
        bot.process_new_updates([update])
        return 'ok', 200
    except Exception as e:
        bot.send_message(CONST.ARKADY_ID, 'Eror > \n' + str(e))
        print(e)
        return 'ok', 200
    
    # if update.message.text != '/check':

    # else:
    #     SBot.revoke()
@app.route('/{}'.format(secretUpadate), methods=['POST'])
def Update():
    print('get_response')
    SBot.revoke()

@bot.message_handler(commands=['start'])
def C_start(m):
    SBot.C_start(m)


@bot.message_handler(commands=['who_next'])
def C_who_mext(m):
    SBot.C_who_next(m)


@bot.message_handler(commands=['edit'])
def C_edit(m):
    SBot.C_edit(m)


@bot.message_handler(commands=['duty_list'])
def C_duty_list(m):
    SBot.C_duty_list(m)


@bot.message_handler(commands=['newnew'])
def C_new(m):
    SBot.C_new(m)


@bot.message_handler(commands=['new_nextnew'])
def C_new_next(m):
    SBot.C_new_next(m)


@bot.message_handler(commands=['inform_me'])
def C_inform_me(m):
    SBot.C_inform_me(m)

@bot.message_handler()
def C_Menager(m):
    SBot.C_Maneger(m)

bot.remove_webhook()

if __name__ == "__main__":
    bot.polling()
else:
    bot.set_webhook(url=CONST.URL)


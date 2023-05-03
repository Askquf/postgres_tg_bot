import re
from datetime import datetime
import telebot
import db_worker
import request_worker
from config import disaster_levels, need_db
from secret import token

token = token
bot = telebot.TeleBot(token)

@bot.message_handler(content_types=['text'])
def answer_message(message):
    if need_db:
        if 'уровень' in message.text.lower():
            msg_list = message.text.split(' ')
            level = msg_list[len(msg_list) - 1]
            if level in disaster_levels:
                answer = worker.get_level_disasters(level)
                bot.send_message(message.from_user.id, bot_answer(answer))
            else:
                bot.send_message(message.from_user.id, 'Такого уровня нет!')
        elif 'решенные' in message.text.lower():
            bot.send_message(message.from_user.id, bot_answer(worker.get_is_solved_disasters('true')))
        elif 'нерешенные' in message.text.lower():
            bot.send_message(message.from_user.id, bot_answer(worker.get_is_solved_disasters('false')))
        else:
            bot.send_message(message.from_user.id, 'Пожалуйста, напишите правильную команду')
    else:
        text = re.split('(?<!,)\s', message.text.lower())
        text = dict([(text[i], [value.strip() for value in text[i + 1].split(',')]) for i in range(0, len(text), 2)]) if len(text) > 1 and len(text) % 2 == 0 else '400'
        if (text == '400'):
            bot.send_message(message.from_user.id, 'Вы клоун')
        else:
            problems = worker.get_problems(text)
            answer = [f'Id события: {problem["eventid"]}\n' \
                  f'Дата: {datetime.fromtimestamp(int(problem["clock"]))}\n' \
                  f'Наименование: {problem["name"]}\n'
                  f'Значимость: {problem["severity"]}\n' \
                      f'Id объекта: {problem["objectid"]}' for problem in problems]
            for problem in answer:
                bot.send_message(message.from_user.id, problem)

def bot_answer(answer):
    return '\n'.join([f'Проблема решена: {string[1]}\nПроблема: {string[2]}\nУровень проблемы: {string[3]}' for string in answer])

if __name__ == '__main__':
    if need_db:
        worker = db_worker.DataBaseWorker()
    else:
        worker = request_worker.RequestWorker()
    bot.polling(interval=0, none_stop=True)



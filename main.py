import telebot;
import db_worker
from config import disaster_levels

token = ''
bot = telebot.TeleBot(token)

@bot.message_handler(content_types=['text'])
def answer_message(message):
    if 'уровень' in message.text().lower():
        msg_list = message.text().split(' ')
        level = msg_list[len(msg_list) - 1]
        if level in disaster_levels:
            answer = db_worker.get_level_disasters(level)
            bot.send_message(message.from_user_id, bot_answer(answer))
        else:
            bot.send_message(message.from_user_id, 'Такого уровня нет!')
    elif 'решенные' in message.text().lower():
        bot.send_message(message.from_user_id, bot_answer(db_worker.get_is_solved_disasters('true')))
    elif 'нерешенные' in message.text().lower():
        bot.send_message(message.from_user_id, bot_answer(db_worker.get_is_solved_disasters('false')))
    else:
        bot.send_message(message.from_user_id, 'Пожалуйста, напишите правильную команду')

def bot_answer(answer):
    return '\n'.join([f'Проблема решена: {string[1]}\nПроблема: {string[2]}\nУровень проблемы: {string[3]}' for string in answer])

if __name__ == '__main__':
    bot.polling(interval=0, none_stop=True)

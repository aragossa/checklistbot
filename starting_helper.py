# /usr/bin/python3
import datetime

import telebot

from buttons_helper import KeyboardHelper
from dbconnector import Dbconnetor


def stating_handler(user, message):
    last_name = message.from_user.last_name
    first_name = message.from_user.first_name
    username = message.from_user.username
    user.join_aggrbot(last_name=last_name, first_name=first_name, username=username, ref_key='Notset', lang='rus')
    keyboard1 = KeyboardHelper.reply_call_back_button(user=user)
    user.send_message(message_index='WELCOME', keyboard=keyboard1)
    keyboard = KeyboardHelper.first_post_keyboard(user=user)
    user.send_message(message_index='HELLO_MESSAGE', keyboard=keyboard)


def text_message_handler(user, message, bot, input_value):
    user_state = user.getstate()
    if message.text == user.select_message ('CONTACT'):
        user.change_user_state ('REQUEST')
        user.send_message(message_index='ENTER_TEXT')

    elif user_state:
        if user_state == 'REQUEST':
            user.change_user_state('')
            user.save_request (message_text=message.text)

        elif 'RESPONSE' in user_state:
            sender_id = user_state.split('_')[1]
            request_id = user_state.split('_')[2]
            send_text = ('Ответ от {}\n\n{}'.format(user.get_username(user.uid), message.text))
            user.send_message(chat_id=sender_id, text=send_text)
            user.request_update_staus(request_id=request_id, new_staus='FIN', resposne_text=send_text)
            result_query = user.get_message_ids(request_id)
            user.change_user_state('')
            for row in result_query:
                bot.edit_message_text(chat_id=row[1], message_id=row[0], text='Обработано')



def reply_to_request_handler(call, user, bot):
    sender_user = call.data.split('_')[1]
    request_id = call.data.split('_')[2]
    user.change_user_state('RESPONSE_{}_{}'.format(sender_user, request_id))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.message.text)
    send_text = ('{}\n\nВведите ответ:'.format(call.message.text))
    try:
        bot.send_message(chat_id=call.message.chat.id, text=send_text)
    except telebot.apihelper.ApiException:
        Dbconnetor.execute_insert_query("""UPDATE core.users SET aggregator_bot_block_date = '{}' WHERE user_id = '{}'
                                            """.format(datetime.datetime.now(), call.message.chat.id))


def first_post_handler(call, user, bot):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.message.text)
    keyboard = KeyboardHelper.inline_call_back_button(user)
    user.send_message(message_index='POST_1', keyboard=keyboard)


def call_back_handler(call, user, bot):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.message.text)
    user.change_user_state ('REQUEST')
    user.send_message(message_index='ENTER_TEXT')


def user_answer_handler(call, user, bot):
    data = call.data.split('_')
    answer = data[1]
    question_type = data[2]
    user.save_answer(answer=answer, test_type=question_type)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=user.select_message('POST$2'), parse_mode='markdown')
    user.send_message(message_index='THANKS')



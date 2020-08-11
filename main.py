import logging

import telebot
from telebot import apihelper

import likeshelper
from bot_user import BotUser
from dbconnector import DbConnetor
import starting_helper

logging.basicConfig(
    filename='errors.log',
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
logger = telebot.logger

telebot.logger.setLevel(logging.INFO)
TOKEN = DbConnetor.get_config_parameter('api_token')
bot = telebot.TeleBot(TOKEN, threaded=True)

@bot.message_handler(commands=['clear'])
def handle_start(m):
    user = BotUser(uid=m.chat.id, bot=bot)
    DbConnetor.execute_insert_query(f"""DELETE FROM checklist_bot.active_child""")
    DbConnetor.execute_insert_query(f"""DELETE FROM checklist_bot.users_state""")
    DbConnetor.execute_insert_query(f"""DELETE FROM checklist_bot.configuration WHERE group_id = {user.uid}""")
    DbConnetor.execute_insert_query(f"""DELETE FROM checklist_bot.reg_keys""")
    DbConnetor.execute_insert_query(f"""DELETE FROM checklist_bot.users""")


@bot.message_handler(commands=['start'])
def handle_start(m):
    user = BotUser(uid=m.chat.id, bot=bot)
    try:
        starting_helper.stating_handler(user=user, message=m)
    except:
        logging.exception(str(m))
        logging.exception('Got exception on main handler')
        user.send_message(message_index="ERROR_MESSAGE")


@bot.message_handler(content_types='text')
def simple_text_message(m):
    user = BotUser(uid=m.chat.id, bot=bot)
    try:
        starting_helper.text_message_handler(user=user, message=m, bot=bot)
    except:
        logging.exception(str(m))
        logging.exception('Got exception on main handler')
        user.send_message(message_index="ERROR_MESSAGE")


@bot.callback_query_handler(func=lambda call: call.data[:5] == 'like_')
def likeshandler(call):
    user = BotUser(uid=call.message.chat.id, bot=bot)
    try:
        likeshelper.send_likes(user=user, call=call)

    except:
        logging.exception(str(call))
        logging.exception('Got exception on main handler')
        bot.send_message(call.message.chat.id, 'Что-то пошло не так')


@bot.callback_query_handler(func=lambda call: call.data[:6] == 'extra_')
def extra_menu_handler(call):
    user = BotUser(uid=call.message.chat.id, bot=bot)
    try:
        starting_helper.extra_checklist(user=user, call=call)
    except:
        logging.exception(str(call))
        logging.exception('Got exception on main handler')
        bot.send_message(call.message.chat.id, 'Что-то пошло не так')


@bot.callback_query_handler(func=lambda call: call.data[:9] == 'settings_')
def extra_menu_handler(call):
    user = BotUser(uid=call.message.chat.id, bot=bot)
    try:
        starting_helper.app_settings(user=user, call=call)
    except:
        logging.exception(str(call))
        logging.exception('Got exception on main handler')
        bot.send_message(call.message.chat.id, 'Что-то пошло не так')
#edit_

@bot.callback_query_handler(func=lambda call: call.data[:5] == 'edit_')
def extra_menu_handler(call):
    user = BotUser(uid=call.message.chat.id, bot=bot)
    try:
        starting_helper.app_new_value(user=user, call=call)
    except:
        logging.exception(str(call))
        logging.exception('Got exception on main handler')
        bot.send_message(call.message.chat.id, 'Что-то пошло не так')

#checklist_select_
#checklist_edit_
@bot.callback_query_handler(func=lambda call: call.data[:10] == 'checklist_')
def extra_menu_handler(call):
    user = BotUser(uid=call.message.chat.id, bot=bot)
    try:
        starting_helper.choose_checklists(user=user, call=call)
    except:
        logging.exception(str(call))
        logging.exception('Got exception on main handler')
        bot.send_message(call.message.chat.id, 'Что-то пошло не так')


@bot.callback_query_handler(func=lambda call: call.data[:5] == 'item_')
def extra_menu_handler(call):
    user = BotUser(uid=call.message.chat.id, bot=bot)
    try:
        starting_helper.checklist_item_actions(user=user, call=call)
    except:
        logging.exception(str(call))
        logging.exception('Got exception on main handler')
        bot.send_message(call.message.chat.id, 'Что-то пошло не так')

if __name__ == '__main__':
    bot.polling(none_stop=True)

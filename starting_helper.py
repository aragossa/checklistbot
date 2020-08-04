# /usr/bin/python3
import datetime

import telebot

import likeshelper
from buttons_helper import KeyboardHelper
from dbconnector import DbConnetor


def stating_handler(user, message):
    parent_id = message.text.replace('/start ', '')
    send_text = "Добро пожаловать!"
    print ('send_text1', send_text)
    if parent_id == ('/start'):
        parent_id = None
        send_text = f"""Добро пожаловать! Добавьте профиль ребенка и настройте чек-листы

Сслылка для ребенка:
https://t.me/cheklistbot_bot?start={user.uid}"""

    user_role = 'child'
    user.join_bot(last_name=message.from_user.last_name,
                  first_name=message.from_user.first_name,
                  user_name=message.from_user.username,
                  parent_id=parent_id,
                  user_role=user_role)
    keyboard = KeyboardHelper.main_menu_buttons(user)
    print ('send_text2', send_text)
    user.send_message(text=send_text, keyboard=keyboard)


def text_message_handler(user, message, bot):
    user_state = user.get_user_state()
    if 'Текущий профиль: ' in message.text:
        user.set_user_state('')
        user.change_active_user()
        keyboard = KeyboardHelper.main_menu_buttons(user)
        user.send_message(text=user.select_message('CHANGE_PROFILE'),
                          keyboard=keyboard)


    elif message.text == 'Ежедневно':
        user.set_user_state('')
        keyboard = KeyboardHelper.generate_checklist_buttons(user=user, checklist_type='day')
        send_text = user.select_message('SEND_CHECKLIST')
        if not keyboard:
            send_text = 'Чеклист не задан'
        user.send_message(text=send_text, keyboard=keyboard)

    elif message.text == 'Еженедельно':
        user.set_user_state('')
        keyboard = KeyboardHelper.generate_checklist_buttons(user=user, checklist_type='week')
        send_text = user.select_message('SEND_CHECKLIST')
        if not keyboard:
            send_text = 'Чеклист не задан'
        user.send_message(text=send_text, keyboard=keyboard)

    elif message.text == 'Другое':
        user.set_user_state('')
        keyboard = KeyboardHelper.extra_checklist_keyboard(user)
        send_text = user.select_message('CHOOSE_EXTRA')
        user.send_message(text=send_text, keyboard=keyboard)

    elif message.text == '👍':
        user.set_user_state('')
        likeshelper.likes_handler(message=message, action='like_p', user=user)

    elif message.text == '👎':
        user.set_user_state('')
        likeshelper.likes_handler(message=message, action='like_m', user=user)

    elif message.text == 'Настройка':
        user.set_user_state('')
        send_text = user.select_message('CHOOSE_EXTRA')
        keyboard = KeyboardHelper.app_settings_menu(user=user)
        user.send_message(text=send_text, keyboard=keyboard)

    elif user_state in user.get_configs(return_conf_name=True):
        user_state = user.get_user_state()
        user.update_conf_value(conf_name=user_state, new_value=message.text)
        user.send_message(text="Ok")
        user.set_user_state('')

    elif 'CHECKLIST_EDIT_ITEM_' in user.get_user_state():
        item_id = user.get_user_state().split('_')[3]
        checklist_type = user.get_user_state().split('_')[4]
        user.edit_checklist_item(item_id=item_id, new_item=message.text)
        send_checklist_again(user, checklist_type, editing=True)

    elif 'CHECKLIST_ADD_ITEM_' in user.get_user_state():
        checklist_type = user.get_user_state().split('_')[3]
        user.add_checklist_item(new_item=message.text, checklist_type=checklist_type)
        send_checklist_again(user, checklist_type, editing=True)

    else:
        user.send_message(text='simple text message')

def extra_checklist(user, call):
    user.bot.delete_message (chat_id=call.message.chat.id, message_id=call.message.message_id)
    action = call.data.split('_')[1]
    if action == 'stat':
        user.send_message(message_index='USER_STATISCTICS')
    elif action == 'date':
        keyboard = KeyboardHelper.generate_checklist_buttons(user=user, checklist_type='date')
        send_text = user.select_message('SEND_CHECKLIST')
        if not keyboard:
            send_text = 'Чеклист не задан'
        user.send_message(text=send_text, keyboard=keyboard)
    elif action == 'once':
        keyboard = KeyboardHelper.generate_checklist_buttons(user=user, checklist_type='once')
        send_text = user.select_message('SEND_CHECKLIST')
        if not keyboard:
            send_text = 'Чеклист не задан'
        user.send_message(text=send_text, keyboard=keyboard)
    elif action == 'month':
        keyboard = KeyboardHelper.generate_checklist_buttons(user=user, checklist_type='month')
        send_text = user.select_message('SEND_CHECKLIST')
        if not keyboard:
            send_text = 'Чеклист не задан'
        user.send_message(text=send_text, keyboard=keyboard)


def app_settings(user, call):
    user.bot.delete_message (chat_id=call.message.chat.id, message_id=call.message.message_id)
    action = call.data.split('_')[1]
    if action == 'checklist':
        keyboard = KeyboardHelper.choose_checklist_keyboard(user=user)
    elif action == 'values':
        keyboard = KeyboardHelper.settings_keyboard(user=user)
    user.send_message(message_index='CHOOSE_EXTRA', keyboard=keyboard)


def app_new_value(user, call):
    user.bot.delete_message (chat_id=call.message.chat.id, message_id=call.message.message_id)
    action = call.data.replace('edit_', '')
    user.set_user_state(action)
    user.send_message(message_index='ENTER_NEW_VALUE')


def choose_checklists(user, call):
    user.set_user_state('EDIT_CHECKLIST')
    user.bot.delete_message (chat_id=call.message.chat.id, message_id=call.message.message_id)
    action = call.data.split('_')[1]
    checklist_type = call.data.split('_')[2]
    keyboard = KeyboardHelper.generate_checklist_buttons(user=user, checklist_type=checklist_type, editable=True)
    if keyboard:
        send_text = user.select_message('SEND_CHECKLIST')
        user.send_message(text=send_text, keyboard=keyboard)
    else:
        send_text = 'Чеклист не задан'
        user.send_message(text=send_text)



def send_checklist_again(user, checklist_type, editing=False):
    if user.get_user_state() == 'EDIT_CHECKLIST':
        editable=True
    else:
        editable=False
    if editing:
        editable=True
    keyboard = KeyboardHelper.generate_checklist_buttons(user=user, checklist_type=checklist_type, editable=editable)
    if keyboard:
        send_text = user.select_message('SEND_CHECKLIST')
        user.send_message(text=send_text, keyboard=keyboard)
    else:
        send_text = 'Чеклист не задан'
        user.send_message(text=send_text)
#check
#view
#edit
#del
#add
def checklist_item_actions(user, call):
    print(call.data)
    action = call.data.split('_')[1]
    if action == 'add':
        checklist_type = call.data.split('_')[2]
    else:
        item_id = call.data.split('_')[2]
        checklist_type = call.data.split('_')[3]
    if action == 'check':
        user.check_checklist_item(item_id=item_id)
    elif action == 'view':
        pass
    elif action == 'edit':
        user.bot.delete_message (chat_id=call.message.chat.id, message_id=call.message.message_id)
        new_user_state = 'CHECKLIST_EDIT_ITEM_' + item_id + '_' + checklist_type
        user.set_user_state(new_user_state)
        user.send_message(message_index='ENTER_NEW_VALUE')
    elif action == 'del':
        user.del_checklist_item(item_id=item_id)
        user.bot.delete_message (chat_id=call.message.chat.id, message_id=call.message.message_id)
        send_checklist_again(user=user, checklist_type=checklist_type)
    elif action == 'add':
        user.bot.delete_message (chat_id=call.message.chat.id, message_id=call.message.message_id)
        new_user_state = 'CHECKLIST_ADD_ITEM_' + checklist_type
        user.set_user_state(new_user_state)
        user.send_message(message_index='NEW_CHECKLIST_ITEM')

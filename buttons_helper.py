from telebot import types


class KeyboardHelper:

    @staticmethod
    def main_menu_buttons(user):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        user_role = user.get_user_role()
        user_childs_list = user.get_all_childs()
        if user_childs_list:
            if (user_role == 'parent' and len(user_childs_list) > 1):
                child_id = user.get_active_child()
                child_name = user.get_user_username(user_id=child_id)
                child_button = types.KeyboardButton('Текущий профиль: ' + child_name)
                keyboard.add(child_button)
        btn1 = types.KeyboardButton('Ежедневно')
        btn2 = types.KeyboardButton('Еженедельно')
        btn3 = types.KeyboardButton('Другое')
        btn4 = types.KeyboardButton('👍')
        btn5 = types.KeyboardButton('👎')
        keyboard.add(btn1, btn2, btn3, btn4, btn5)
        if user_role == 'parent':
            btn6 = types.KeyboardButton('Настройка')
            keyboard.add(btn6)
        return keyboard

    @staticmethod
    def likes_helper():
        keyboard = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='Правда', callback_data='likes_true')
        btn2 = types.InlineKeyboardButton(text='Помощь природе', callback_data='likes_help')
        keyboard.add(btn1, btn2)
        return keyboard

    @staticmethod
    def dislikes_helper():
        keyboard = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='Ложь', callback_data='dislikes_lie')
        btn2 = types.InlineKeyboardButton(text='Порча чужого имущества', callback_data='dislikes_damage')
        keyboard.add(btn1, btn2)
        return keyboard

    @staticmethod
    def settings_helper():
        keyboard = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='Cоздать/корректировать чеклист', callback_data='settings_checklist')
        btn2 = types.InlineKeyboardButton(text='Задать веса', callback_data='settings_weights')
        keyboard.add(btn1, btn2)
        return keyboard

    @staticmethod
    def get_likes_keyboard(user, action):
        keyboard = types.InlineKeyboardMarkup()
        active_child = user.get_active_child()
        if action == 'like_p':
            text_btn1 = 'Правда'
            text_btn2 = 'Помощь природе'
        elif action == 'like_m':
            text_btn1 = 'Ложь'
            text_btn2 = 'Порча чужого имущества'
        btn1 = types.InlineKeyboardButton(text=text_btn1, callback_data=action + '_1_' + str(active_child))
        btn2 = types.InlineKeyboardButton(text=text_btn2, callback_data=action + '_2_' + str(active_child))
        keyboard.add(btn1, btn2)
        return keyboard

    @staticmethod
    def add_checklist_item():
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Добавить пункт',
                                                callback_data='item_add'))

    @staticmethod
    def generate_checklist_buttons(user, checklist_type, editable=False):
        keyboard = types.InlineKeyboardMarkup()
        checklist_item_list = user.get_checklist_list(checklist_type)
        if editable:
            btn_add = types.InlineKeyboardButton(text='Добавить пункт',
                                                  callback_data='item_add_' + checklist_type)
            keyboard.add(btn_add)
        if checklist_item_list:
            for elem in checklist_item_list:
                if elem.get('item_status') == 1:
                    status_check = '☑'
                else:
                    status_check = '☐'
                if user.get_user_role() == 'parent':
                    action = 'item_check_'
                elif user.get_user_role() == 'child':
                    action = 'item_view_'
                btn_item = types.InlineKeyboardButton(text=status_check + ' ' + elem.get('item_text'),
                                                      callback_data=action + elem.get('item_id') + '_' + checklist_type)
                if editable:
                    btn_del = types.InlineKeyboardButton(text='⌫',
                                                         callback_data='item_del_' + elem.get('item_id') + '_' + checklist_type)
                    btn_edit = types.InlineKeyboardButton(text='✎',
                                                          callback_data='item_edit_' + elem.get('item_id') + '_' + checklist_type)
                    keyboard.add(btn_item, btn_edit, btn_del)
                else:
                    keyboard.add(btn_item)
        else:
            keyboard = None
        return keyboard

    @staticmethod
    def extra_checklist_keyboard(user):
        keyboard = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='Статистика', callback_data='extra_stat')
        btn2 = types.InlineKeyboardButton(text='На дату', callback_data='extra_date')
        btn3 = types.InlineKeyboardButton(text='Разово без даты', callback_data='extra_once')
        btn4 = types.InlineKeyboardButton(text='Ежемесячно', callback_data='extra_month')
        keyboard.add(btn1, btn2, btn3, btn4)
        return keyboard

    @staticmethod
    def app_settings_menu(user):
        keyboard = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='Создать/корректировать чеклист', callback_data='settings_checklist')
        btn2 = types.InlineKeyboardButton(text='Задать веса', callback_data='settings_values')
        keyboard.add(btn1, btn2)
        return keyboard

    @staticmethod
    def app_settings_values():
        keyboard = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='Создать/корректировать чеклист', callback_data='settings_checklist')
        btn2 = types.InlineKeyboardButton(text='Задать веса', callback_data='settings_values')
        keyboard.add(btn1, btn2)
        return keyboard

    @staticmethod
    def settings_keyboard(user):
        keyboard = types.InlineKeyboardMarkup()
        config_list = user.get_configs()
        for row in config_list:
            send_msg = row.get("conf_name") + ': ' + row.get("conf_value")
            btn = types.InlineKeyboardButton(text=send_msg, callback_data='edit_' + row.get("conf_name"))
            keyboard.add(btn)
        return keyboard

    @staticmethod
    def choose_checklist_keyboard(user):
        keyboard = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='Ежедневный', callback_data='checklist_select_day')
        btn2 = types.InlineKeyboardButton(text='Еженедельный', callback_data='checklist_select_week')
        btn3 = types.InlineKeyboardButton(text='На дату', callback_data='checklist_select_date')
        btn4 = types.InlineKeyboardButton(text='Разово без даты', callback_data='checklist_select_once')
        btn5 = types.InlineKeyboardButton(text='Ежемесячный', callback_data='checklist_select_month')
        keyboard.add(btn1, btn2, btn3, btn4, btn4, btn5)
        return keyboard



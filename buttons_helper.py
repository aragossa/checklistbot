from telebot import types


class KeyboardHelper:

    @staticmethod
    def reply_call_back_button(user):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text=user.select_message('CONTACT'))
        keyboard.add(btn1)
        return keyboard

    @staticmethod
    def inline_call_back_button(user):
        keyboard = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text=user.select_message('CONTACT'), callback_data='call_back')
        keyboard.add(btn1)
        return keyboard

    @staticmethod
    def reply_to_user_request_keyboard(user, sender_id, request_id):
        keyboard = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text=user.select_message('REPLY_TO'),
                                          callback_data='reply_{}_{}'.format(sender_id, request_id))
        keyboard.add(btn1)
        return keyboard

    @staticmethod
    def yes_no_answers(user, post_index):
        keyboard = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text=user.select_message ('YES_ANSWER'),
                                          callback_data='answer_yes_{}'.format(post_index))
        btn2 = types.InlineKeyboardButton(text=user.select_message ('NO_ANSWER'),
                                          callback_data='answer_no_{}'.format(post_index))
        keyboard.add(btn1, btn2)
        return keyboard

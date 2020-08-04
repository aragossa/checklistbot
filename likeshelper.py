from bot_user import BotUser
from buttons_helper import KeyboardHelper


def likes_handler(message, action, user):
    keyboard = KeyboardHelper.get_likes_keyboard(user=user, action=action)
    user.send_message(message_index='SELECT_LIKE', keyboard=keyboard)

def send_likes(user, call):
    action = call.data.split('_')
    like_var = '_'.join([action[0], action[1]])
    like_type = action[2]
    child_id = action[3]
    if like_var == 'like_p':
        user.send_like(child_id=child_id, like_var=like_var, like_type=like_type)
    elif like_var == 'like_m':
        user.send_dislike(child_id=child_id, like_var=like_var, like_type=like_type)
    user.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Отправлено')
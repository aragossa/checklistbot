import datetime
import uuid
import time

import telebot

from buttons_helper import KeyboardHelper
from dbconnector import Dbconnetor


class Botuser():

    def __init__(self, uid, bot):
        self.uid = uid
        self.bot = bot

    @staticmethod
    def get_admins():
        result = Dbconnetor.execute_select_many_query("""SELECT user_id FROM toparents_bot.bot_admin
                                                           WHERE status = 'ENABLE'""")
        admins_list = []
        if result:
            for row in result:
                admins_list.append(row[0])
            return admins_list

    @staticmethod
    def get_username(uid):
        result = Dbconnetor.execute_select_query(
            "SELECT username, first_name, last_name from core.users WHERE user_id = {}".format(
                uid))
        if result[1] != 'None':
            return (result[1] + ' ' + result[2])
        else:
            return result[0]

    def get_user_lang(self):
        lang = Dbconnetor.execute_select_query(
            "SELECT lang from core.users WHERE users.user_id = {}".format(self.uid))
        if lang:
            return lang[0]

    def send_message(self, chat_id=None, message_index=None, text=None, keyboard=None):
        if not text:
            text = self.select_message(message_index=message_index)

        if not chat_id:
            chat_id = self.uid

        try:
            if keyboard:
                return self.bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard, parse_mode='Markdown')
            else:
                return self.bot.send_message(chat_id=chat_id, text=text, parse_mode='Markdown')
        except telebot.apihelper.ApiException:
            Dbconnetor.execute_insert_query("""UPDATE core.users SET aggregator_bot_block_date = '{}' WHERE user_id = '{}'
                                            """.format(datetime.datetime.now(), chat_id))

    def select_message(self, message_index):
        lang = self.get_user_lang()
        if not lang:
            lang = 'rus'
        result = Dbconnetor.execute_select_query("""SELECT text FROM toparents_bot.messages
                                                       WHERE lang = '{0}'
                                                       AND message_index = '{1}'""".format(lang, message_index))
        if result:
            return str(result[0])

    def join_aggrbot(self, last_name, first_name, username, ref_key='Notset', lang='rus'):
        Dbconnetor.execute_insert_query("""
        INSERT INTO core.users
	        ( ref_id, lang, interface, user_id, last_name, first_name, username, aggregator_bot_join_date)
	    VALUES
	        ( '{0}', '{1}', 'TG', {2}, '{3}', '{4}', '{5}', current_timestamp )
	    ON CONFLICT ON CONSTRAINT idx_users
	    DO UPDATE SET aggregator_bot_join_date = current_timestamp;""".format(ref_key, lang, self.uid, last_name,
                                                                              first_name, username))

    def save_request_message(self, request_id, admin_id, message_id):
        Dbconnetor.execute_insert_query("""
                INSERT INTO toparents_bot.request_messages (message_id, user_id, request_id, status)
                VALUES ('{}', '{}', '{}', 'SENT')
        """.format(message_id, admin_id, request_id))

    def save_request(self, message_text):
        request_id = uuid.uuid4()
        Dbconnetor.execute_insert_query("""
                INSERT INTO toparents_bot.user_requests
	            ( request_id, sender_user_id, "message_text", request_status )
	            VALUES ( '{}', {}, '{}', 'NEW' );
                """.format(request_id, self.uid, message_text))

    def getstate(self):
        status = Dbconnetor.execute_select_query(
            "SELECT user_state from toparents_bot.user_state_toparents_bot WHERE user_id = {}".format(self.uid))
        if status:
            return status[0]

    def change_user_state(self, user_state):
        query = """
        INSERT INTO toparents_bot.user_state_toparents_bot
	        ( user_id,  user_state )
	    VALUES
	        ( '{}', '{}' )
	    ON CONFLICT ON CONSTRAINT pk_user_state_user_id
	    DO UPDATE SET user_state = '{}';""".format(self.uid, user_state, user_state)

        Dbconnetor.execute_insert_query(query)

    def request_update_staus(self, request_id, new_staus, resposne_text):
        now = datetime.datetime.now()
        query = """
                UPDATE toparents_bot.user_requests SET request_status = '{}', response_text = '{}', response_datetime = '{}' WHERE request_id = '{}'
        """.format(new_staus, resposne_text, now, request_id)
        Dbconnetor.execute_insert_query(query)

    def get_message_ids(self, request_id):
        result = Dbconnetor.execute_select_many_query("""SELECT message_id, user_id FROM toparents_bot.request_messages
                                                           WHERE request_id = '{}'""".format(request_id))
        message_list = []
        if result:
            for row in result:
                message_list.append(row)
            return message_list

    def send_post_to_users(self, post_index):
        dbconnector = Dbconnetor()
        users = dbconnector.execute_select_many_query(
            "SELECT user_id from core.users WHERE aggregator_bot_join_date IS NOT NULL AND aggregator_bot_block_date IS NULL")
        post = self.select_message(post_index)
        for user in users:
            self.send_message(chat_id=user[0], text=post)
            time.sleep(1)

    def send_custom_post(self, post_index):
        users = Dbconnetor.execute_select_many_query(
            "SELECT user_id from core.users WHERE aggregator_bot_join_date IS NOT NULL")
        keyboard = KeyboardHelper.yes_no_answers(user=self, post_index=post_index)
        send_text = self.select_message(post_index)
        for user in users:
            self.send_message(chat_id=user[0], text=send_text, keyboard=keyboard)


    def save_answer(self, answer, test_type):
        Dbconnetor.execute_insert_query("""
                INSERT INTO
                    toparents_bot.user_answers (user_id, answer, status, question_num, post_type)
	            VALUES ({}, '{}', 'ACTIVE', 1 , '{}');""".format(
            self.uid, answer, test_type))


import datetime
import uuid
import time

import telebot

from buttons_helper import KeyboardHelper
from checklist_helper import ChecklistHelper
from dbconnector import DbConnetor


class BotUser:

    def __init__(self, uid, bot):
        self.uid = uid
        self.bot = bot

    """
    Select message text by message index
    """

    @staticmethod
    def select_message(message_index):
        result = DbConnetor.execute_select_query(f"""SELECT message_text FROM checklist_bot.messages
                                                       WHERE message_index = '{message_index}'""")
        if result:
            return str(result[0])

    """
    Reacting to '/start' command
    """

    def join_bot(self, last_name, first_name, user_name, parent_id, user_role):
        print ('parent_id1', parent_id)
        if parent_id:
            print ('parent_id2', parent_id)
            DbConnetor.execute_insert_query(
                f"""INSERT INTO checklist_bot.users ( user_id, first_name, last_name, user_name, parent_user_id, user_role )
                   VALUES ( '{self.uid}', '{last_name}', '{first_name}', '{user_name}','{parent_id}', '{user_role}' )
                   ON CONFLICT DO NOTHING;""")
            print ('parent_id3', parent_id)
            DbConnetor.execute_insert_query(
                f"""INSERT INTO checklist_bot.active_child
	                    ( user_id, child_id) VALUES ( {parent_id}, {self.uid} )
                    ON CONFLICT DO NOTHING;""")
            print ('parent_id4', parent_id)
        else:
            print ('test else')
            DbConnetor.execute_insert_query(
                f"""INSERT INTO checklist_bot.users ( user_id, first_name, last_name, user_name, parent_user_id, user_role )
                   VALUES ( '{self.uid}', '{last_name}', '{first_name}', '{user_name}', '{self.uid}', 'parent' )
                   ON CONFLICT DO NOTHING;""")
            DbConnetor.execute_insert_query(f"""INSERT INTO checklist_bot.configuration (conf_name, conf_value, group_id)
                    VALUES('DISLIKE_LIE_VAL', 100, {self.uid});""")
            DbConnetor.execute_insert_query(f"""INSERT INTO checklist_bot.configuration (conf_name, conf_value, group_id)
                    VALUES('DISLIKE_BROKE_VAL', 100, {self.uid});""")
            DbConnetor.execute_insert_query(f"""INSERT INTO checklist_bot.configuration (conf_name, conf_value, group_id)
                    VALUES('WEEK_CHECKLIST_VAL', 100, {self.uid});""")
            DbConnetor.execute_insert_query(f"""INSERT INTO checklist_bot.configuration (conf_name, conf_value, group_id)
                    VALUES('ONCE_CHECKLIST_VAL', 100, {self.uid});""")
            DbConnetor.execute_insert_query(f"""INSERT INTO checklist_bot.configuration (conf_name, conf_value, group_id)
                    VALUES('MONTH_CHECKLIST_VAL', 100, {self.uid});""")
            DbConnetor.execute_insert_query(f"""INSERT INTO checklist_bot.configuration (conf_name, conf_value, group_id)
                    VALUES('DATE_CHECKLIST_VAL', 100, {self.uid});""")
            DbConnetor.execute_insert_query(f"""INSERT INTO checklist_bot.configuration (conf_name, conf_value, group_id)
                    VALUES('LIKE_TRUE_VAL', 100, {self.uid});""")
            DbConnetor.execute_insert_query(f"""INSERT INTO checklist_bot.configuration (conf_name, conf_value, group_id)
                    VALUES('LIKE_HELP_VAL', 100, {self.uid});""")
            DbConnetor.execute_insert_query(f"""INSERT INTO checklist_bot.configuration (conf_name, conf_value, group_id)
                    VALUES('DAY_CHECKLIST_VAL', 100, {self.uid});""")
            DbConnetor.execute_insert_query(f"""INSERT INTO checklist_bot.users_state (user_id, user_state)
                    VALUES({self.uid}, '');""")
        print ('test fin')

    """
    Sending message
    """

    def send_message(self, chat_id=None, message_index=None, text=None, keyboard=None):
        print ('text2', text)
        if not text:
            text = self.select_message(message_index=message_index)

        print ('text2', text)

        if not chat_id:
            chat_id = self.uid

        try:
            if keyboard:
                self.bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)
            else:
                self.bot.send_message(chat_id=chat_id, text=text)
        except telebot.apihelper.ApiException:
            DbConnetor.execute_insert_query(f"""UPDATE checklist_bot.users
                                                SET block_date = '{datetime.datetime.now()}'
                                                WHERE user_id = '{chat_id}'
                                            """)

    """
    User attributes method
    """

    def get_user_role(self, user_id=None):
        if not user_id:
            user_id = self.uid
        result_query = DbConnetor.execute_select_query(
            f"SELECT user_role from checklist_bot.users WHERE user_id = {user_id}")
        if result_query:
            return result_query[0]

    def get_user_username(self, user_id=None):
        if not user_id:
            user_id = self.uid
        result_query = DbConnetor.execute_select_query(
            f"SELECT user_name from checklist_bot.users WHERE user_id = {user_id}")
        if result_query:
            return result_query[0]

    """
    User state methods
    """

    def get_user_state(self):
        result_query = DbConnetor.execute_select_query(
            f"SELECT user_state from checklist_bot.users_state WHERE user_id = {self.uid}")
        if result_query:
            return result_query[0]

    def set_user_state(self, new_state):
        DbConnetor.execute_insert_query(f"""
                INSERT INTO checklist_bot.users_state (user_id, user_state) 
                VALUES ('{self.uid}', '{new_state}')
                ON CONFLICT (user_id) DO UPDATE 
                    SET user_state = '{new_state}';""")

    """
    User input value methods
    """

    def get_user_input_value(self):
        result_query = DbConnetor.execute_select_query(
            f"SELECT input_value from checklist_bot.user_input_value WHERE user_id = {self.uid}")
        if result_query:
            return result_query[0]

    def set_user_input_value(self, new_state):
        DbConnetor.execute_insert_query(f"""
                INSERT INTO checklist_bot.user_input_value (user_id, input_value) 
                VALUES ('{self.uid}', '{new_state}')
                ON CONFLICT (user_id) DO UPDATE 
                    SET input_value = '{new_state}';""")

    """
    Active child methods
    """

    def get_active_child(self):
        result_query = DbConnetor.execute_select_query(
            f"SELECT child_id from checklist_bot.active_child WHERE user_id = {self.uid}")
        if result_query:
            return result_query[0]

    def set_active_child(self, child_id):
        DbConnetor.execute_insert_query(f"""
                INSERT INTO checklist_bot.active_child (user_id, child_id) 
                VALUES ('{self.uid}', '{child_id}')
                ON CONFLICT (user_id) DO UPDATE 
                    SET child_id = '{child_id}';""")

    def get_parent_user_id(self):
        result_query = DbConnetor.execute_select_query(
            f"SELECT parent_user_id FROM checklist_bot.users WHERE user_id = {self.uid}")
        if result_query:
            return result_query[0]

    def get_all_childs(self):
        parent_user_id = self.get_parent_user_id()
        result_query = DbConnetor.execute_select_many_query(
            f"""SELECT user_id
                FROM checklist_bot.users
                WHERE parent_user_id = '{parent_user_id}'
                AND user_role = 'child'""")
        result = []
        if result_query:
            for elem in result_query:
                result.append(elem[0])
            return result

    def change_active_user(self):
        current_active_child = self.get_active_child()
        all_childs = self.get_all_childs()
        next_index = all_childs.index(current_active_child) + 1
        current_active_child_id = all_childs.index(current_active_child)
        if current_active_child_id == len(all_childs) - 1:
            next_index = 0
        self.set_active_child(all_childs[next_index])

    def get_group_users(self):
        result_query = DbConnetor.execute_select_many_query(
            f"""SELECT user_id
                FROM checklist_bot.users
                WHERE parent_user_id = '{self.uid}'""")
        group_user_list = []
        for group_user in result_query:
            group_user_list.append(group_user[0])
        return group_user_list

    """
    Checklist methods
    """

    def get_checklist_list(self, checklist_type, child_profile=None):
        if not child_profile:
            child_profile = self.get_active_child()
        checklist_helper = ChecklistHelper(self.uid)
        result_query = checklist_helper.get_checklist_list(checklist_type=checklist_type, child_user_id=child_profile)
        return result_query

    def edit_checklist_item(self, item_id, new_item):
        checklist_helper = ChecklistHelper(self.uid)
        checklist_helper.edit_checklist_item(item_id=item_id, new_item=new_item)

    def check_checklist_item(self, item_id):
        checklist_helper = ChecklistHelper(self.uid)
        checklist_helper.check_checklist_item(item_id=item_id)

    def add_checklist_item(self, new_item, checklist_type):
        active_child = self.get_active_child()
        checklist_helper = ChecklistHelper(self.uid)
        checklist_helper.add_checklist_item(new_item=new_item, checklist_type=checklist_type, child=active_child)

    def del_checklist_item(self, item_id):
        checklist_helper = ChecklistHelper(self.uid)
        checklist_helper.del_checklist_item(item_id=item_id)

    """
    Likes reacting
    """
    def get_configs(self, return_conf_name=False):
        parent_id = self.get_parent_user_id()
        result_query = DbConnetor.execute_select_many_query(f"""
            SELECT conf_name, conf_value
            FROM checklist_bot.configuration
            WHERE group_id = {parent_id}
        """)
        result = []
        for row in result_query:
            if return_conf_name:
                result.append(row[0])
            else:
                result.append({'conf_name':row[0],
                               'conf_value':row[1]})
        return result

    def get_conf_value(self, conf_name):
        parent_id = self.get_parent_user_id()
        result_query = DbConnetor.execute_select_query(f"""
            SELECT conf_value
            FROM checklist_bot.configuration
            WHERE conf_name = '{conf_name}'
            AND group_id = {parent_id}
        """)
        if result_query:
            return result_query[0]

    def update_conf_value(self, conf_name, new_value):
        parent_id = self.get_parent_user_id()
        DbConnetor.execute_insert_query(f"""
            UPDATE checklist_bot.configuration
            SET conf_value = {new_value} 
            WHERE conf_name = '{conf_name}'
            AND group_id = {parent_id};
        """)


    def send_like(self, child_id, like_var, like_type):
        DbConnetor.execute_insert_query(f"""
                UPDATE checklist_bot.users
                SET likes = likes + 1
                WHERE user_id = {child_id};""")
        if like_type == '1':
            trust_correction = self.get_conf_value("LIKE_TRUE_VAL")
        else:
            trust_correction = self.get_conf_value("LIKE_HELP_VAL")
        DbConnetor.execute_insert_query(f"""
                UPDATE checklist_bot.users
                SET trust_level = trust_level + {trust_correction}
                WHERE user_id = {child_id};""")
        DbConnetor.execute_insert_query(f"""
                INSERT INTO checklist_bot.users_likes
	            ( user_id, from_user_id, like_type, like_var)
                VALUES ( {child_id}, {self.uid}, '{like_type}', '{like_var}' );""")

    def send_dislike(self, child_id, like_var, like_type):
        DbConnetor.execute_insert_query(f"""
                UPDATE checklist_bot.users
                SET likes = likes - 1
                WHERE user_id = {child_id};""")
        if like_type == '1':
            trust_correction = self.get_conf_value("DISLIKE_LIE_VAL")
        else:
            trust_correction = self.get_conf_value("DISLIKE_BROKE_VAL")
        DbConnetor.execute_insert_query(f"""
                UPDATE checklist_bot.users
                SET trust_level = trust_level - {trust_correction}
                WHERE user_id = {child_id};""")
        DbConnetor.execute_insert_query(f"""
                INSERT INTO checklist_bot.users_likes
	            ( user_id, from_user_id, like_type, like_var)
                VALUES ( {child_id}, {self.uid}, '{like_type}', '{like_var}' );""")


if __name__ == '__main__':
    user = BotUser(uid=556047985, bot='bot')
    print(user.get_configs())
    print(user.get_configs(return_conf_name=True))

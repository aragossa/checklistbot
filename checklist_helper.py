import uuid

from dbconnector import DbConnetor


class ChecklistHelper:

    def __init__(self, uid):
        self.uid = uid

    def get_checklist_list(self, checklist_type, child_user_id):
        result = DbConnetor.execute_select_many_query(f"""SELECT checklist_item, uuid, item_status
                                                          FROM checklist_bot.users_checklist_catalog
                                                          WHERE parent_user_id = '{self.uid}'
                                                          AND child_user_id = '{child_user_id}'
                                                          AND checklist_type = '{checklist_type}'""")
        if result:
            item_list = []
            for row in result:
                item_list.append({'item_text': row[0],
                                  'item_id': row[1],
                                  'item_status': row[2]})
            return item_list

    def edit_checklist_item(self, item_id, new_item):
        DbConnetor.execute_insert_query(f"""UPDATE checklist_bot.users_checklist_catalog
                                           SET checklist_item = '{new_item}'       
                                           WHERE uuid = '{item_id}'""")

    def check_checklist_item(self, item_id):
        DbConnetor.execute_insert_query(f"""UPDATE checklist_bot.users_checklist_catalog
                                           SET item_status = 1
                                           WHERE uuid = '{item_id}'""")


    def update_checklist_item_status(self, item_id, new_status):
        DbConnetor.execute_insert_query(f"""UPDATE checklist_bot.users_checklist_catalog
                                           SET item_status = '{new_status}'
                                           WHERE uuid = '{item_id}'""")

    def add_checklist_item(self, new_item, checklist_type, child):
        item_uuid = str(uuid.uuid4())
        DbConnetor.execute_insert_query(f"""INSERT INTO checklist_bot.users_checklist_catalog
                                           ( uuid, parent_user_id, checklist_item, checklist_type, child_user_id, item_status)
                                           VALUES
                                           ( '{item_uuid}', '{self.uid}', '{new_item}', '{checklist_type}', '{child}', 0 );""")

    def del_checklist_item(self, item_id):
        DbConnetor.execute_insert_query(f"""DELETE FROM checklist_bot.users_checklist_catalog
                                           WHERE uuid = '{item_id}';""")


if __name__ == '__main__':
    checklist_helper = ChecklistHelper(556047985)
    result = checklist_helper.get_checklist_list(checklist_type='day')
    checklist_helper.edit_checklist_item(new_item='qwerqwerqwer', item_id='db56b02a-13aa-402c-bbdf-57b8369dcdcd')
    result = checklist_helper.get_checklist_list(checklist_type='day')
    checklist_helper.add_checklist_item('werdvxczxdfasd', 'day')
    result = checklist_helper.get_checklist_list(checklist_type='day')
    checklist_helper.del_checklist_item('db56b02a-13aa-402c-bbdf-57b8369dcdcd')
    result = checklist_helper.get_checklist_list(checklist_type='day')

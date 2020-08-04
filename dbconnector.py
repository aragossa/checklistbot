import psycopg2
from config import config

class DbConnetor ():

    @staticmethod
    def connect():
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            return conn, cur
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    @staticmethod
    def execute_select_query(query):
        conn, cur = DbConnetor.connect()
        with conn:
            cur.execute(query)
            result = cur.fetchone()
            return result

    @staticmethod
    def execute_select_many_query(query):
        conn, cur = DbConnetor.connect()
        with conn:
            cur.execute(query)
            result = cur.fetchall()
            return result

    @staticmethod
    def execute_insert_query(query):
        conn, cur = DbConnetor.connect()
        with conn:
            cur.execute(query)
            conn.commit()

    @staticmethod
    def get_config_parameter(conf_name):
        result = DbConnetor.execute_select_query(
            "SELECT conf_value FROM checklist_bot.configuration WHERE conf_name = '{}'".format(conf_name))
        if result:
            return result[0]


if __name__ == '__main__':
    token = DbConnetor.get_config_parameter('api_token', 'aggr_bot')
    print(token)
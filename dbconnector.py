import psycopg2
from config import config

class Dbconnetor ():

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
    def execute_select_query (query):
        conn, cur = Dbconnetor.connect()
        with conn:
            cur.execute(query)
            result = cur.fetchone()
            return result

    @staticmethod
    def execute_select_many_query (query):
        conn, cur = Dbconnetor.connect()
        with conn:
            cur.execute(query)
            result = cur.fetchall()
            return result

    @staticmethod
    def execute_insert_query (query):
        conn, cur = Dbconnetor.connect()
        with conn:
            cur.execute(query)
            conn.commit()

    @staticmethod
    def get_config_parameter (conf_name, conf_group):
        result = Dbconnetor.execute_select_query(
            "SELECT conf_value FROM core.configuration WHERE conf_name = '{}' AND conf_group = '{}'".format (conf_name, conf_group))
        if result:
            return result[0]
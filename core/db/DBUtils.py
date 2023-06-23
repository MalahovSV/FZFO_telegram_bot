import psycopg2

global conn
global cursor

def executeCommandSQL(command):
    conn = psycopg2.connect(dbname='FZFO_TGB', host='localhost', user='postgres', password='1', port='5432')
    cursor = conn.cursor()
    cursor.execute(command)

    return cursor.fetchone()
    cursor.close()
    conn.close()

def checkIdUser (id):
    return executeCommandSQL(f"select * from check_id_telegram_user('{id}')")

def check_login_password(login, password):
    return executeCommandSQL(f"select * from check_data_user('{login}','{password}')")


def executeUpdateCommandSQL(command):
    conn = psycopg2.connect(dbname='FZFO_TGB', host='localhost', user='postgres', password='1', port='5432')
    cursor = conn.cursor()
    cursor.execute(command)
    conn.commit()
    print(command)
    return cursor.fetchone()[0]
    cursor.close()
    conn.close()

def add_telegram_id_user(login, password, id_telegram):
    return executeUpdateCommandSQL(f"select * from Add_ID_UserTG('{login}','{password}', '{id_telegram}')")
import sqlite3


conn = sqlite3.connect("requests.db")
cursor = conn.cursor()

CREATE_TABLE_QUERY = '''
    CREATE TABLE IF NOT EXISTS users_requests (
        chat_id INTEGER PRIMARY KEY,
        date TEXT NOT NULL
    );
'''

# cursor.execute(CREATE_TABLE_QUERY)

# INSERT_DATE_QUERY = '''
#     INSERT INTO users_requests (chat_id, date) VALUES(?, ?)
# '''
# INSERT_PARAMS = (224787, "2020-01-01")

# cursor.execute(INSERT_DATE_QUERY, INSERT_PARAMS)
# conn.commit()
# conn.rollback()

SELECT_USERS_DATES_QUERY = '''
    SELECT * FROM users_requests
'''
res = cursor.execute(SELECT_USERS_DATES_QUERY, ).fetchmany()
if res:
    print(res)




































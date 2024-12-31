import sqlite3

def create_connection():
    return sqlite3.connect("../dbs/university.db")

def get_user_details(user_id):

    # use the condition to check all the table with user_id
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT secret_code, role, name FROM user_detail WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result if result else (None, None, None)

def read_sql_query(sql):
    try:
        # st.write(sql)
        conn = create_connection()
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.commit()
        conn.close()
        # st.write(rows)
        return rows
    except Exception as e:
        #print(sql)
        print(e)
        return f"SQLite error: {e}"

def update_multifactor_status(user_id, status, secret):
    conn = create_connection()
    cursor = conn.cursor()

    # Update the multifactor status
    cursor.execute("UPDATE user_detail SET multifactor = ? WHERE id = ?", (status, user_id))
    multifactor_updated = cursor.rowcount  # Rows affected by the first query

    # Update the secret code
    cursor.execute("UPDATE user_detail SET secret_code = ? WHERE id = ?", (secret, user_id))
    secret_updated = cursor.rowcount  # Rows affected by the second query

    # Commit the changes
    conn.commit()
    conn.close()

    # Verify updates
    if multifactor_updated > 0 and secret_updated > 0:
        return 1
    elif multifactor_updated > 0:
        return 0
    elif secret_updated > 0:
        return 0
    else:
        return -1

def change_pass(password,user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE user_detail SET password = ? WHERE id = ?", (password, user_id))
    conn.commit()
    conn.close()

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


#  # SQLite connection function
# def create_connection_new():
#     return sqlite3.connect("dynamic_department.db")

# Create tables for departments, staff, timetable, and subjects
def create_main_tables():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            admin_id VARCHAR(50) PRIMARY KEY,
            password VARCHAR(50) DEFAULT 'admin_pass',
            mfa BOOLEAN DEFAULT 0,
            code VARCHAR(50) DEFAULT 'none'
        );
        """)
        # Create Department table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS department (
            department_id VARCHAR(50) PRIMARY KEY,
            name TEXT,
            graduate_level TEXT,
            phone TEXT
            
        );
        """)
        
        # Create Staff table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS staff (
            staff_id TEXT PRIMARY KEY,
            name TEXT,
            designation TEXT,
            phone TEXT,
            department_id INTEGER,
            password VARCHAR(50) DEFAULT 'pass_staff',
            mfa BOOLEAN DEFAULT 0,
            code VARCHAR(50) DEFAULT 'none',
            FOREIGN KEY(department_id) REFERENCES department(department_id)
        );
        """)
        
        # Create Timetable table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS timetable (
            timetable_id INTEGER PRIMARY KEY AUTOINCREMENT,
            day TEXT,
            time TEXT,
            subject TEXT,
            department_id INTEGER,
            class varchar(50),
            FOREIGN KEY(department_id) REFERENCES department(department_id)
        );
        """)
        
        # Create Subject table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS subject (
            subject_id TEXT PRIMARY KEY AUTOINCREMENT ,
            name TEXT,
            code TEXT,
            department_id INTEGER,
            FOREIGN KEY(department_id) REFERENCES department(department_id)
        );
        """)
        
        conn.commit()
    except :
        pass
    finally:
        conn.close()

# Insert data into the department table
def add_department(department_id, name, graduate_level, phone):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO department (department_id, name, graduate_level, phone)
    VALUES (?, ?, ?, ?);
    """, (department_id, name, graduate_level, phone))
    conn.commit()
    conn.close()

# Fetch all departments
def fetch_departments():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM department;")
    departments = cursor.fetchall()
    conn.close()
    return departments

# Insert data into the staff table
def add_staff(staff_id, name, designation, phone, department_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO staff (staff_id, name, designation, phone, department_id)
    VALUES (?, ?, ?, ?, ?);
    """, (staff_id, name, designation, phone, department_id))
    conn.commit()
    conn.close()
    
# Insert data into the staff table
def add_admin(admin_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO staff (admin_id)
    VALUES (?);
    """, (admin_id))
    conn.commit()
    conn.close()

# Insert data into the timetable table
def add_timetable(day, time, subject,class_name, department_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
    INSERT INTO timetable (day, time, subject, department_id,class)
    VALUES (?, ?, ?, ?,?);
    """, ( day, time, subject, department_id,class_name))
        conn.commit()
    except:
        pass
    finally:
        conn.close()

# Insert data into the subject table
def add_subject( name, code, department_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO subject ( name, code, department_id)
    VALUES ( ?, ?, ?);
    """, ( name, code, department_id))
    conn.commit()
    conn.close()

# def create_connection():
#     return sqlite3.connect("dynamic_department.db")
        
# Fetch department details
def fetch_department_details():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM department")
    data = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    conn.close()
    return data, columns

# Fetch staff details
def fetch_staff_details(department_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM staff WHERE department_id = ?", (department_id,))
    data = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    conn.close()
    return data, columns

# Fetch timetable
def fetch_timetable(department_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT day, time, subject FROM timetable WHERE department_id = ?", (department_id,))
    data = cursor.fetchall()
    conn.close()
    return data

# Update a record
def update_record(table, updates, condition):
    conn = create_connection()
    cursor = conn.cursor()
    set_clause = ", ".join([f"{column} = ?" for column in updates.keys()])
    condition_clause = " AND ".join([f"{column} = ?" for column in condition.keys()])
    values = list(updates.values()) + list(condition.values())
    cursor.execute(f"UPDATE {table} SET {set_clause} WHERE {condition_clause}", values)
    conn.commit()
    conn.close()

# Delete a record
def delete_record(table, condition):
    conn = create_connection()
    cursor = conn.cursor()
    condition_clause = " AND ".join([f"{column} = ?" for column in condition.keys()])
    values = list(condition.values())
    cursor.execute(f"DELETE FROM {table} WHERE {condition_clause}", values)
    conn.commit()
    conn.close()

# Fetch subject details
def fetch_subject_details(department_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM subject WHERE department_id = ?", (department_id,))
    data = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    conn.close()
    return data, columns
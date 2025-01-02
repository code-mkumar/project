import sqlite3

def create_connection():
    return sqlite3.connect("../dbs/university.db")
    
def create_tables():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = create_connection()
    cursor = conn.cursor()

    # SQL statements to create tables
    table_creation_queries = [
        """
        CREATE TABLE IF NOT EXISTS student_details (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            dob DATE NOT NULL,
            department_id TEXT NOT NULL,
            class TEXT NOT NULL,
            quiz1 FLOAT ,
            quiz2 FLOAT,
            quiz3 FLOAT,
            assignment1 FLOAT,
            assignment2 FLOAT,
            internal1 FLOAT,
            internal2 FLOAT,
            internal3 FLOAT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS staff_details (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            designation TEXT NOT NULL,
            department_id TEXT NOT NULL,
            password TEXT NOT NULL DEFAULT pass_staff ,
            mfa BOOLEAN DEFAULT 0,
            secd TEXT DEFAULT NONE,
            phone_no INTEGER NOT NULL,
            email TEXT NOT NULL UNIQUE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS department_details (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            grad_level TEXT NOT NULL,
            phone TEXT NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS admin_details (
            id TEXT PRIMARY KEY,
            password TEXT NOT NULL DEFAULT pass_admin,
            mfa BOOLEAN DEFAULT 0,
            secd TEXT DEFAULT NONE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            message TEXT NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS subject (
            id TEXT PRIMARY KEY,
            department_id INTEGER NOT NULL,
            name TEXT NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS timetable (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day TEXT NOT NULL,
            time TEXT NOT NULL,
            subject TEXT NOT NULL,
            class TEXT NOT NULL,
            department_id INTEGER NOT NULL
        );
        """
    ]

    # Execute all queries
    for query in table_creation_queries:
        cursor.execute(query)

    # Commit and close the connection
    conn.commit()
    conn.close()


# function to get the user role
def get_role(user_id):
    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()
        role = ''
        tables = ['student_details', 'staff_details', 'admin_details']
        
        for table in tables:
            cursor.execute(f'SELECT 1 FROM {table} WHERE id = ?', (user_id,))
            if cursor.fetchone():  # Checks if any row is returned
                role = table
                break
        
        return role
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if conn:
            conn.close()

# funtcion to verify the user password
def check_user(user_id, password, role):
    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()
        query = ""
        
        # Validate role to prevent SQL injection
        if role not in ['student_details', 'staff_details', 'admin_details']:
            raise ValueError("Invalid role specified.")

        # Construct query based on role
        if role == 'student_details':
            query = f'SELECT * FROM {role} WHERE id = ? AND dob = ?'
        else:
            query = f'SELECT * FROM {role} WHERE id = ? AND password = ?'
        
        # Execute the query
        cursor.execute(query, (user_id, password))
        data = cursor.fetchone()
        
        return data
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    except ValueError as ve:
        print(f"Value error: {ve}")
        return None
    finally:
        if conn:
            conn.close()

# enabling or disabling the mfa
def mfa_update(user_id, role, status):
    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        # Validate role to prevent SQL injection
        if role not in ['staff_details', 'admin_details']:
            raise ValueError("Invalid role specified.")

        # Validate status as integer or boolean (convert to 1/0 for boolean)
        if not isinstance(status, (int, bool)):
            raise ValueError("Invalid status type. Must be an integer or boolean.")
        status = int(status)

        # Construct and execute the query
        query = f"UPDATE {role} SET mfa = ? WHERE id = ?"
        cursor.execute(query, (status, user_id))
        conn.commit()
        
        return "success"
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return "failed"
    except ValueError as ve:
        print(f"Value error: {ve}")
        return "failed"
    finally:
        if conn:
            conn.close()

#function to update the serect code
def serectcode_update(user_id, secret, role):
    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        # Validate role to prevent SQL injection
        if role not in ['staff_details', 'admin_details']:
            raise ValueError("Invalid role specified.")

        # Validate secret as a string (assuming it's a secret code, not a boolean or integer)
        if not isinstance(secret, str) or len(secret) == 0:
            raise ValueError("Invalid secret type. Must be a non-empty string.")

        # Construct and execute the query with conditional MFA check
        query = f"UPDATE {role} SET secd = ? WHERE id = ? AND mfa = 1"
        cursor.execute(query, (secret, user_id))
        conn.commit()
        
        return "success"
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return "failed"
    except ValueError as ve:
        print(f"Value error: {ve}")
        return "failed"
    finally:
        if conn:
            conn.close()

#remove and disable the mfa
def clear_mfa(user_id, role):
    conn = None
    try:
        # Validate role to prevent SQL injection
        if role not in ['staff_details', 'admin_details']:
            raise ValueError("Invalid role specified.")
        
        # Establish the database connection
        conn = create_connection()
        cursor = conn.cursor()

        # Construct and execute the query to clear MFA
        query = f"UPDATE {role} SET secd = 'None', mfa = 0 WHERE id = ? AND mfa = 1"
        cursor.execute(query, (user_id,))
        conn.commit()

        return "success"
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return "failed"
    except ValueError as ve:
        print(f"Value error: {ve}")
        return "failed"
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "failed"
    finally:
        if conn:
            conn.close()


#user details by user id 
def get_user_details(user_id):
    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()
        tables = ['student_details', 'staff_details', 'admin_details']
        data=''
        for table in tables:
            cursor.execute(f'SELECT * FROM {table} WHERE id = ?', (user_id,))
            data = cursor.fetchone()
        return data
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if conn:
            conn.close()


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


def change_pass(password,user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE user_detail SET password = ? WHERE id = ?", (password, user_id))
    conn.commit()
    conn.close()

# incrementing the class and delete the final 
def incrementing_class():
    conn = None
    try:
        # Establish the database connection
        conn = create_connection()
        cursor = conn.cursor()

        # Delete students who are in their final year (class III)
        query_delete_final_year = "DELETE FROM student_details WHERE class = 'III'"
        cursor.execute(query_delete_final_year)

        # Increment class from I to II
        query_update_I_to_II = "UPDATE student_details SET class = 'II' WHERE class = 'I'"
        cursor.execute(query_update_I_to_II)

        # Increment class from II to III
        query_update_II_to_III = "UPDATE student_details SET class = 'III' WHERE class = 'II'"
        cursor.execute(query_update_II_to_III)

        # Commit the changes to the database
        conn.commit()
        return "success"
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return "failed"
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "failed"
    finally:
        if conn:
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

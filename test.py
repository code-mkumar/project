import sqlite3
import os
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "./dbs/university.db"))
conn=sqlite3.connect(db_path)
mycursor=conn.cursor()

#altering the table 

def altering_table():
    mycursor.execute("alter table staff_details drop email T NOT N;")
    #mycursor.execute("ALTER TABLE staff_details DROP CONSTRAINT UNIQUE CONSTRAINT;")
    conn.commit()
    conn.close()
altering_table()
def read_student_files():
    with open("student_role.txt", "r") as role_file:
        role_content = role_file.read()
    with open("student_sql.txt", "r") as sql_file:
        sql_content = sql_file.read()
    return role_content, sql_content

def read_default_files():
    with open("default.txt", "r") as role_file:
        role_content = role_file.read()
    with open("default_sql.txt", "r") as sql_file:
        sql_content = sql_file.read()
    return role_content, sql_content

def read_staff_files():
    with open("staff_role.txt", "r") as role_file:
        role_content = role_file.read()
    with open("staff_sql.txt", "r") as sql_file:
        sql_content = sql_file.read()
    return role_content, sql_content

def read_admin_files():
    with open("admin_role.txt", "r") as role_file:
        role_content = role_file.read()
    with open("admin_sql.txt", "r") as sql_file:
        sql_content = sql_file.read()
    return role_content, sql_content

def write_to_file(filename, data):
    """
    Writes data to a file, overwriting the existing content.
    :param filename: The file to write to (student.txt or staff.txt).
    :param data: The data to write (a list of strings).
    """
    with open(filename, "w") as file:
        for line in data:
            file.write(line + "\n")
    print(f"Data successfully written to {filename}.")

def append_to_file(filename, data):
    """
    Appends data to a file.
    :param filename: The file to append to (student.txt or staff.txt).
    :param data: The data to append (a list of strings).
    """
    with open(filename, "a") as file:
        for line in data:
            file.write(line + "\n")
    print(f"Data successfully appended to {filename}.")


def read_from_file(filename):
    """
    Reads data from a file and returns it as a list of strings.
    :param filename: The file to read from (student.txt or staff.txt).
    :return: A list of strings (one per line in the file).
    """
    with open(filename, "r") as file:
        data = file.readlines()
    return [line.strip() for line in data]  # Remove newlines from each line


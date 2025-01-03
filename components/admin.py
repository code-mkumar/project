import streamlit as st
import os
import sqlite3
import operation
import operation.dboperation
import operation.fileoperations
#import operation.dboperation
#import operation.fileoperations
from datetime import date
def admin_page():
    # st.set_page_config(page_title="Admin Dashboard", layout="wide")
    # secret, role, name = None#operation.dboperation.get_user_details(st.session_state.user_id)
    # operation.dboperation.update_multifactor_status(st.session_state.user_id, st.session_state.multifactor ,secret)  # Update MFA status in the database
    # Sidebar content
    with st.sidebar:
        st.header("Admin Modules")
        module = st.radio(
            "Select Module",
            options=["File Upload and Edit", "Database Setup", "Query Area","admin data", "Logout"]
        )
       

    # Main page content
    st.title("Admin Dashboard")
    st.write(f"Welcome, admin! 👋")

    
# Ensure required files exist

    # # Ensure required files exist
    # for file_name in ["collegehistory.txt", "departmenthistory.txt", "syllabus.txt"]:
    #     if not os.path.exists(file_name):
    #         with open(file_name, "w") as f:
    #             f.write("")  # Create an empty file

    # Proceed with other operations
    
# List of text files
                           
    if module=="File Upload and Edit":
        st.subheader("File Creation")
        f1=st.text_input("Enter the file name")
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f"../files/{f1}.txt"))
        if f1:
            operation.fileoperations.write_to_file(file_path)
        st.subheader("File Upload and Edit Module")
        folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f"../files/"))
        
# Get all files in the folder
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

        print("Files in folder:", files)
         # Selection of category to save the file
        category = st.selectbox(
        "Select the category to save the uploaded file:",
        # ["collegehistory.txt", "departmenthistory.txt", "syllabus.txt"]
        files
    )

    # File uploader
        uploaded_file = st.file_uploader(
        "Upload a PDF, Word, or Text file", type=["pdf", "docx", "txt"]
    )

        if uploaded_file:
        # Read and display the content of the uploaded file
            # if uploaded_file.type == "application/pdf":
            #     import PyPDF2
            #     pdf_reader = PyPDF2.PdfReader(uploaded_file)
            #     file_content = "".join([page.extract_text() for page in pdf_reader.pages])
            # elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            #     from docx import Document
            #     doc = Document(uploaded_file)
            #     file_content = "\n".join([p.text for p in doc.paragraphs])
            # else:
            #     file_content = uploaded_file.read().decode('utf-8')
            file_content = operation.fileoperations.file_to_text(uploaded_file)

            st.text_area("Uploaded File Content", value=file_content, height=300, disabled=True)

        # Section for editing file content
            edited_content = st.text_area("Edit File Content", value=file_content, height=300)

            if st.button("Save File"):
                with open(category, "a") as f:
                    f.write(edited_content)
                st.success(f"File content saved to {category} successfully!")

    # Section for managing existing files
        st.subheader("Manage Existing Files")
        existing_file = st.selectbox(
        "Select a file to view or edit:",
        # ["collegehistory.txt", "departmenthistory.txt", "syllabus.txt"]
        files
    )

        if st.button("Open File"):
            with open(existing_file, "r") as f:
                existing_content = f.read()
            edited_existing_content = st.text_area("Edit Existing File Content", value=existing_content, height=300)

            if st.button("Update File"):
                with open(existing_file, "w") as f:
                    f.write(edited_existing_content)
                st.success(f"Content of {existing_file} updated successfully!")

    # Deletion section
        st.subheader("Delete File Content")
        file_to_delete = st.selectbox(
        "Select a file to delete content:",
        # ["collegehistory.txt", "departmenthistory.txt", "syllabus.txt"]
        files
    )

        if st.button("Delete Content"):
            with open(file_to_delete, "w") as f:
                f.write("")
            st.success(f"Content of {file_to_delete} deleted successfully!")


   
    


    elif module == "Database Setup":
        

       
        
        # Streamlit app
        st.title("Department and Related Tables Management")
        
        # Create tables if they don't exist
        # operation.dboperation.create_main_tables()
        if st.button('create table'):
            operation.dboperation.create_tables()
        
        
        # Add a Department
        with st.expander("Add a New Department"):
            department_id = st.text_input("Department Id:")
            name = st.text_input("Department Name:")
            graduate_level = st.selectbox("Graduate Level:", ["UG", "PG"])
            phone = st.text_input("Phone Number:")
        
            if st.button("Add Department"):
                if department_id and name and graduate_level and phone:
                    operation.dboperation.add_department(department_id,name,graduate_level,phone)
                    st.success(f"Department '{name}' added successfully!")
                else:
                    st.error("Please fill all the fields.")
        
        # Display existing departments
        departments = operation.dboperation.view_departments()
        if departments:
            with st.expander("Existing Departments"):
                for dept in departments:
                    st.write(f"ID: {dept[0]}, Name: {dept[1]}, Graduate Level: {dept[2]}, Phone: {dept[3]}")
        
            # Select a department ID for further actions
            selected_department_id = st.selectbox(
                "Select Department ID for Adding Staff, Timetable, or Subjects:", 
                [dept[0] for dept in departments]
            )
            selected_dept = next((dept for dept in departments if dept[0] == selected_department_id), None)
            graduate_level = selected_dept[2]
            # Add Staff to the selected department
            with st.expander("Add Staff to Selected Department"):
                staff_id = st.text_input("Staff Id:")
                staff_name = st.text_input("Staff Name:")
                designation = st.text_input("Designation:")
                staff_phone = st.text_input("Phone:")
                
                if st.button("Add Staff"):
                    
                    if staff_id and staff_name and designation and staff_phone:
                        operation.dboperation.add_staff(staff_id,staff_name,designation,department_id,"pass_staff")
                        st.success(f"Staff '{staff_name}' added to Department ID {selected_department_id}!")
                    else:
                        st.error("Please fill all the fields.")
        
            # Add Timetable to the selected department
            with st.expander("Add Timetable to Selected Department"):
                # timetable_id = st.text_input("Time Table Id:")
                day = st.selectbox("day:",["monday","tuesday","wednesday","thursday","friday","saturday"])
                if day =="saturday":
                    time = st.selectbox("Time:",["9.00-9.45","9.45-10.30","10.30-11.15","11.20-12.10","12.10-1.00"])
                else:
                    time = st.selectbox("Time:",["10-11","11-12","12-1","2-3","3-4","4-5"])
                subject = st.text_input("Subject:")
        
                if graduate_level == "PG": 
                    class_name = st.selectbox("Class:", ["I", "II"]) 
                else: 
                    class_name = st.selectbox("Class:", ["I", "II", "III"])
                
                if st.button("Add Timetable"):
                    if  day and time and subject:
                        operation.dboperation.add_timetable(day, time, subject,class_name, selected_department_id)
                        st.success(f"Timetable for '{day} at {time}' added to Department ID {selected_department_id}!")
                    else:
                        st.error("Please fill all the fields.")
        
            # Add Subject to the selected department
            with st.expander("Add Subject to Selected Department"):
               
                subject_name = st.text_input("Subject Name:")
                subject_code = st.text_input("Subject Code:")
                
                if st.button("Add Subject"):
                    if subject_name and subject_code:
                        operation.dboperation.add_subject( subject_code, selected_department_id,subject_name)
                        st.success(f"Subject '{subject_name}' added to Department ID {selected_department_id}!")
                    else:
                        st.error("Please fill all the fields.")

            # Add Student to the selected department
            with st.expander("Add Student to Selected Department"):
                # Define the range of dates
                min_date = date(2000, 1, 1)  # Minimum date
                max_date = date(2050, 12, 31)  # Maximum date
                rollno = st.text_input("Student Rollno:")
                name = st.text_input("Student Name:")
                dob=st.date_input("Date of Birth",min_value=min_date,max_value=max_date)
                class_name=st.selectbox("Select the class",["I","II","III"])
                
                if st.button("Add Student"):
                    if rollno and name and dob and class_name:
                        operation.dboperation.add_student( rollno, name,dob,selected_department_id,class_name)
                        st.success(f"Student '{name}' added to Department ID {selected_department_id}!")
                    else:
                        st.error("Please fill all the fields.")

            # Add marks to the selected department
            with st.expander("Add Marks to Selected Student"):
                st.subheader("Mark Entry")
                class_name = st.selectbox("Class", ["I", "II", "III"])
                
                if class_name:
                    cycle = st.selectbox("Cycle", ["1", "2", "3"])
                    
                    if cycle:
                        # Fetch students for the selected department and class
                        students = operation.dboperation.view_students(selected_department_id, class_name)
                        students_id = [i[0] for i in students]  # List of student IDs
                        students_names = [i[1] for i in students]  # List of student names

                        # Select student by name
                        selected_student_name = st.selectbox("Select Student", students_names)
                        
                        if selected_student_name:
                            # Get the corresponding student ID for the selected student
                            student_index = students_names.index(selected_student_name)
                            student_id = students_id[student_index]
                            
                            # Display the roll number for the selected student
                            id = st.text_input("Roll No:", value=students[student_index][0], disabled=True)

                            # Inputs for marks
                            quiz = st.number_input("Quiz Marks", min_value=0.0, max_value=5.0, step=1.0)
                            assignment = st.number_input("Assignment Marks", min_value=0.0, max_value=10.0, step=1.0)
                            internal_marks = st.number_input("Internal Marks", min_value=0.0, max_value=25.0, step=1.0)

                            # Check if all inputs are filled before submitting
                            if st.button("submit"):
                                if id and quiz and assignment and internal_marks and cycle:
                                    # Add marks to the database
                                    operation.dboperation.add_marks(id, cycle, quiz, assignment, internal_marks)
                                    st.success("Marks added successfully!")

    elif module == "Query Area":
        import pandas as pd

        st.title("View Section")

        
        
        st.title("Dynamic Department Viewer")
        
        # Fetch department details
        departments= operation.dboperation.view_departments()
        department_dict = {row[1]: row[0] for row in departments}
        
        department_name = st.selectbox("Select Department", list(department_dict.keys()))
        department_id = department_dict[department_name]
        
        # Display and edit department details
        st.subheader("Department Details")
        if st.button("View Department Details"):
            st.write(f"Details for Department: {department_name} (ID: {department_id})")
            st.write(f"Department ID: {department_id}, Name: {department_name}")
        
        if st.checkbox("Edit Department Details"):
            new_name = st.text_input("New Department Name", value=department_name)
            if st.button("Update Department"):
                #operation.fileoperations.update_record("department", {"name": new_name}, {"department_id": department_id})
                st.success("Department updated successfully.")
        
        if st.checkbox("Delete Department"):
            if st.button("Delete Department"):
                #operation.dboperation.delete_record("department", {"department_id": department_id})
                st.success("Department deleted successfully.")
        
        # Fetch and edit staff details
        st.subheader("Staff Details")
        staff_data = operation.dboperation.view_staffs(department_id)
        st.table(staff_data)
        
        staff_ids = [record[0] for record in staff_data]  # Assuming `record[0]` is the `staff_id`
        selected_staff_id = st.selectbox("Select Staff ID to Update:", options=staff_ids)

        # Pre-fill fields based on selected staff
        selected_staff = next((record for record in staff_data if record[0] == selected_staff_id), None)
        if selected_staff:
            with st.form("update_staff_form"):
                st.write("Update Staff Details")
                
                staff_id = st.text_input("Staff ID (required):", value=selected_staff[0], disabled=True)
                name = st.text_input("Name:", value=selected_staff[1])  # Assuming `record[1]` is `name`
                designation = st.text_input("Designation:", value=selected_staff[2])  # Adjust indices as needed
                department_id = st.text_input("Department ID:", value=selected_staff[3])
                password = st.text_input("Password:", type="password")
                mfa = st.text_input("MFA:", value=selected_staff[5])  # Adjust index if `mfa` exists
                secd = st.text_input("Secondary Details:", value=selected_staff[6])
                phone_no = st.text_input("Phone Number:", value=selected_staff[7])
                email = st.text_input("Email:", value=selected_staff[8])

                submitted = st.form_submit_button("Update Staff")
                if submitted:
                    if staff_id:
                        operation.dboperation.update_staff(
                            staff_id,
                            name or None,
                            designation or None,
                            department_id or None,
                            password or None,
                            mfa or None,
                            secd or None,
                            phone_no or None,
                            email or None
                        )
                        st.success(f"Staff {staff_id} details updated.")
                    else:
                        st.error("Staff ID is required for updating details.")
            st.subheader("Delete Staff")
            if st.button("Delete Staff"):
                if selected_staff_id:
                    operation.dboperation.delete_staff(selected_staff_id)
                    st.success(f"Staff {selected_staff_id} deleted.")
                else:
                    st.error("Staff ID is required to delete a staff member.")
        else:
            st.warning("No staff data found.")
        # Tab for deleting staff
            

        # time table view
        st.subheader("Timetable Details")
        class_name = st.selectbox("select the class",['I','II','III'])
        if class_name:
            timetable_data = operation.dboperation.view_timetable(department_id,class_name)
            if timetable_data:
                timetable_df = pd.DataFrame(timetable_data, columns=["Day", "Time", "Subject"])
                
                # Group by Time and Day, then unstack to reshape
                timetable_df_grouped = timetable_df.groupby(['Day', 'Time'])['Subject'].first().unstack(fill_value="No Subject")
                
                # Display the reshaped timetable
                st.table(timetable_df_grouped)
            else:
                st.warning("No timetable found for this department.")

        
        # Subject details
        st.subheader("Subject Details")
        if st.button("View Subject Details"):
            data = operation.dboperation.view_subjects(department_id)
            if data:
                st.write(f"Subject Details for Department: {department_name}")
                # st.dataframe(pd.DataFrame(data, columns=columns))
            else:
                st.warning(f"No subjects found for Department: {department_name}")
        
        # Update/Delete subject
        if st.checkbox("Update Subject"):
            new_value = st.text_input("Enter new value")
            column_name = st.selectbox("Select column to update", columns)
            subject_id = st.number_input("Enter Subject ID", min_value=1, step=1)
            if st.button("Update Subject"):
                #operation.dboperation.update_record("subject", {column_name: new_value}, {"subject_id": subject_id})
                st.success("Subject details updated successfully.")
        
        if st.checkbox("Delete Subject"):
            subject_id = st.number_input("Enter Subject ID for deletion", min_value=1, step=1)
            if st.button("Delete Subject"):
                #operation.dboperation.delete_record("subject", {"subject_id": subject_id})
                st.success("Subject deleted successfully.")
                
    elif module == "admin data":
        st.subheader("admin")
        admin_id = st.text_input("enter the admin ID")
        if admin_id:
            operation.dboperation.add_admin(admin_id,'pass_admin')
            st.success(f"Admin {admin_id} added successfully")
    elif module == "Logout":
        st.session_state.authenticated = False
        st.session_state.page = "login"
        st.success("Logged out successfully!")
        st.rerun()

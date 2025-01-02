import streamlit as st
import os
import sqlite3
import operation
import operation.dboperation
import operation.fileoperations
def admin_page():
    # st.set_page_config(page_title="Admin Dashboard", layout="wide")
    secret, role, name = None#operation.dboperation.get_user_details(st.session_state.user_id)
    operation.dboperation.update_multifactor_status(st.session_state.user_id, st.session_state.multifactor ,secret)  # Update MFA status in the database
    # Sidebar content
    with st.sidebar:
        st.header("Admin Modules")
        module = st.radio(
            "Select Module",
            options=["File Upload and Edit", "Database Setup", "Query Area","admin data", "Logout"]
        )
       

    # Main page content
    st.title("Admin Dashboard")
    st.write(f"Welcome, {name}! 👋")

    
# Ensure required files exist

    # Ensure required files exist
    for file_name in ["collegehistory.txt", "departmenthistory.txt", "syllabus.txt"]:
        if not os.path.exists(file_name):
            with open(file_name, "w") as f:
                f.write("")  # Create an empty file

    # Proceed with other operations
    
# List of text files
                           
    if module=="File Upload and Edit":
        st.subheader("File Upload and Edit Module")
         # Selection of category to save the file
        category = st.selectbox(
        "Select the category to save the uploaded file:",
        ["collegehistory.txt", "departmenthistory.txt", "syllabus.txt"]
    )

    # File uploader
        uploaded_file = st.file_uploader(
        "Upload a PDF, Word, or Text file", type=["pdf", "docx", "txt"]
    )

        if uploaded_file:
        # Read and display the content of the uploaded file
            if uploaded_file.type == "application/pdf":
                import PyPDF2
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                file_content = "".join([page.extract_text() for page in pdf_reader.pages])
            elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
                from docx import Document
                doc = Document(uploaded_file)
                file_content = "\n".join([p.text for p in doc.paragraphs])
            else:
                file_content = uploaded_file.read().decode('utf-8')

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
        ["collegehistory.txt", "departmenthistory.txt", "syllabus.txt"]
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
        ["collegehistory.txt", "departmenthistory.txt", "syllabus.txt"]
    )

        if st.button("Delete Content"):
            with open(file_to_delete, "w") as f:
                f.write("")
            st.success(f"Content of {file_to_delete} deleted successfully!")


   
    


    elif module == "Database Setup":
        

       
        
        # Streamlit app
        st.title("Department and Related Tables Management")
        
        # Create tables if they don't exist
        operation.dboperation.create_main_tables()
        
        
        # Add a Department
        with st.expander("Add a New Department"):
            department_id = st.text_input("Department Id:")
            name = st.text_input("Department Name:")
            graduate_level = st.selectbox("Graduate Level:", ["UG", "PG"])
            phone = st.text_input("Phone Number:")
        
            if st.button("Add Department"):
                if department_id and name and graduate_level and phone:
                    operation.dboperation.add_department(department_id, name, graduate_level, phone)
                    st.success(f"Department '{name}' added successfully!")
                else:
                    st.error("Please fill all the fields.")
        
        # Display existing departments
        departments = operation.dboperation.fetch_departments()
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
                        operation.dboperation.add_staff(staff_id, staff_name, designation, staff_phone, selected_department_id)
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
            #         conn = create_connection()
            #         cursor = conn.cursor()
            #         data = cursor.execute("""
            # select * from timetable;
            # """)
            #         conn.commit()
            #         conn.close()
            #         st.table(data)
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
                        operation.dboperation.add_subject(subject_name, subject_code, selected_department_id)
                        st.success(f"Subject '{subject_name}' added to Department ID {selected_department_id}!")
                    else:
                        st.error("Please fill all the fields.")


    elif module == "Query Area":
        import pandas as pd

        st.title("View Section")

        
        
        st.title("Dynamic Department Viewer")
        
        # Fetch department details
        departments, department_columns = operation.dboperation.fetch_department_details()
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
                operation.fileoperations.update_record("department", {"name": new_name}, {"department_id": department_id})
                st.success("Department updated successfully.")
        
        if st.checkbox("Delete Department"):
            if st.button("Delete Department"):
                operation.dboperation.delete_record("department", {"department_id": department_id})
                st.success("Department deleted successfully.")
        
        # Fetch and edit staff details
        st.subheader("Staff Details")
        staff_data, staff_columns = operation.dboperation.fetch_staff_details(department_id)
        if staff_data:
            staff_df = pd.DataFrame(staff_data, columns=staff_columns)
            st.dataframe(staff_df)
        
            staff_id = st.selectbox("Select Staff ID to Edit", staff_df["staff_id"])
            selected_staff = staff_df[staff_df["staff_id"] == staff_id]
        
           # Inside the form for updating staff details
            with st.form("Edit Staff"):
                # Iterate over the columns except "staff_id" for editable fields
                for column in staff_columns:
                    if column != "staff_id":
                        # For columns that should use a select box
                        options = selected_staff[column].unique().tolist()  # Assuming the column contains categorical data
                        new_value = st.selectbox(f"Update {column}", options=options, index=options.index(selected_staff[column].values[0]) if selected_staff[column].values[0] in options else 0)
            
                # Submit button for the form
                submit_button = st.form_submit_button(label="Update Staff")
            
            # Check if the submit button is pressed
            if submit_button:
                # For each field in the form, update the record
                updates = {column: new_value}  # You may need to handle more columns if updating multiple fields
                operation.dboperation.update_record("staff", updates, {"staff_id": staff_id})
                st.success("Staff updated successfully.")

        
            if st.button("Delete Staff"):
                operation.dboperation.delete_record("staff", {"staff_id": staff_id})
                st.success("Staff deleted successfully.")
        else:
            st.warning("No staff found for this department.")
        
        # Fetch and display timetable
       # Fetch and display timetable
        st.subheader("Timetable Details")
        timetable_data = operation.dboperation.fetch_timetable(department_id)
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
            data, columns = operation.dboperation.fetch_subject_details(department_id)
            if data:
                st.write(f"Subject Details for Department: {department_name}")
                st.dataframe(pd.DataFrame(data, columns=columns))
            else:
                st.warning(f"No subjects found for Department: {department_name}")
        
        # Update/Delete subject
        if st.checkbox("Update Subject"):
            new_value = st.text_input("Enter new value")
            column_name = st.selectbox("Select column to update", columns)
            subject_id = st.number_input("Enter Subject ID", min_value=1, step=1)
            if st.button("Update Subject"):
                operation.dboperation.update_record("subject", {column_name: new_value}, {"subject_id": subject_id})
                st.success("Subject details updated successfully.")
        
        if st.checkbox("Delete Subject"):
            subject_id = st.number_input("Enter Subject ID for deletion", min_value=1, step=1)
            if st.button("Delete Subject"):
                operation.dboperation.delete_record("subject", {"subject_id": subject_id})
                st.success("Subject deleted successfully.")
                
    elif module == "admin data":
        st.subheader("admin")
        admin_id = st.text_input("enter the admin ID")
        if admin_id:
            operation.dboperation.add_admin(admin_id)
    elif module == "Logout":
        st.session_state.authenticated = False
        st.session_state.page = "login"
        st.success("Logged out successfully!")
        st.rerun()

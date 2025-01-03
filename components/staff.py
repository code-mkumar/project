import streamlit as st
import genai.gemini
import operation
# import operation.dboperation
import operation.dboperation
import operation.fileoperations
import operation.preprocessing
import operation.qrsetter
import genai
from datetime import date
import pandas as pd
def staff_page():
    # st.set_page_config(page_title="Anjac_AI_staff", layout="wide")
    data = operation.dboperation.view_staff(st.session_state.user_id)
    print("data:",data)
    # Sidebar content
    with st.sidebar:
        st.header("staff Modules")
        module = st.radio(
            "Select Module",
            options=["staff assistant ","File Upload and Edit"]
        )
        if module =="staff assistant ":
            st.header("Chat History")
            # if st.button("Logout"):
            #     st.session_state.authenticated = False
            #     st.session_state.page = "login"
    
            # Display questions and answers in reverse order
            for qa in reversed(st.session_state.qa_list):
                st.write(f"**Question:** {qa['question']}")
                st.write(f"**Answer:** {qa['answer']}")
                st.write("---")

    # Inject custom CSS for the expander
    st.markdown("""
    <style>
    .stExpander {
        position: fixed; /* Keep the expander fixed */
        top: 70px; /* Distance from the top */
        right: 10px; /* Distance from the right */
        width: 200px !important; /* Shrink the width */
        z-index: 9999; /* Bring it to the front */
    }
    .stExpander > div > div {
        background-color: #f5f5f5; /* Light grey background */
        border: 1px solid #ccc; /* Border styling */
        border-radius: 10px; /* Rounded corners */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow */
    }
    .stButton button {
        width: 90%; /* Make buttons fit nicely */
        margin: 5px auto; /* Center-align buttons */
        display: block;
        background-color: #007bff; /* Blue button */
        color: white;
        border-radius: 5px;
        border: none;
        font-size: 14px;
        cursor: pointer;
    }
    .stpopover button {
        width: 90%; /* Make buttons fit nicely */
        margin: 5px auto; /* Center-align buttons */
        display: block;
        background-color: #007bff; /* Blue button */
        color: white;
        border-radius: 5px;
        border: none;
        font-size: 14px;
        cursor: pointer;
    }
    .stButton button:hover {
        background-color: #0056b3; /* Darker blue on hover */
    }
    </style>
""", unsafe_allow_html=True)
    secret =''
# Main page user menu using expander
    with st.expander(f"Welcome, {data[0][1]}! 🧑‍💻"):
        st.write("Choose an action:")
        with st.popover("profile"):
            st.write(f"name:{data[0][1]}")
            st.write(f"rollno:{st.session_state.user_id}")
        with st.popover("settings"):
            st.write("update the password")
            if data[0][5] == True:
                otp = st.text_input("enter the otp" ,type='password')
                if operation.qrsetter.verify_otp(secret,otp):
                    password = st.text_input("enter the new password",type="password")
                    operation.dboperation.change_pass(password,st.session_state.user_id)
                    st.success("changed successfully!!!")
                else:
                    st.error("enter the correct otp...")
            password = st.text_input("enter the password" ,type='password')
            if password == data[0][4]:
                password = st.text_input("enter the new password",type="password")
                operation.dboperation.change_pass(password,st.session_state.user_id)
                st.success("changed successfully!!!")
            else:
                st.error("enter the correct otp...")
            
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.page = "login"
            st.rerun()

    # Main page content
    st.title("Welcome to the ANJAC AI")
    st.write(f"Hello, {data[0][1]}!")

   
    # Initialize session state
    if 'qa_list' not in st.session_state:
        st.session_state.qa_list = []
    # st.header(f"{st.session_state.role} Role Content:")
    # st.text(st.session_state.role_content)
    # st.header(f"{st.session_state.role} SQL Content:")
    # st.text(st.session_state.sql_content)
    # role = st.session_state.role
    role_prompt=''
    sql_content = ''
    

    
    # Allow the user to ask a question
    if module == "staff assistant ":
        
        # submit = st.button('Ask the question')
        question=st.chat_input("Ask the question")
        if question:
            st.chat_message("human").text(question)
            combined_prompt = operation.preprocessing.create_combined_prompt(question, sql_content)
            response = genai.gemini.get_gemini_response(combined_prompt)

            # Display the SQL query
            # st.write("Generated SQL Query:", response)
            raw_query = response
            formatted_query = raw_query.replace("sql", "").strip("'''").strip()
            # print("formatted :",formatted_query)
            single_line_query = " ".join(formatted_query.split()).replace("```", "")
            # print(single_line_query)
            # Query the database
            data = operation.dboperation.read_sql_query(single_line_query)

            if isinstance(data, list):
                #st.write("according to,")
                #st.table(data)
                pass
                
            else:
                #st.write(data)
                # Display any errors
                pass
            # Generate response for the question and answer
            answer = genai.gemini.model.generate_content(f"staff name :{data}  prompt:{role_prompt} Answer this question: {question} with results {str(data)}")
            result_text = answer.candidates[0].content.parts[0].text
            st.chat_message('assistant').markdown(result_text)
            # Store the question and answer in session state
            st.session_state.qa_list.append({'question': question, 'answer': result_text})

            
    elif module == "File Upload and Edit":
        st.write("file upload")
        category=''
        graduate_level=''
        department_name=''
        departments = operation.dboperation.view_departments()  # Fetch all departments
        for dept in departments:
            if dept[0] == data[0][3]:  # Compare department_id
                category = dept[1] +"_department.txt"
                graduate_level=dept[2]
                department_name=dept[1]
        
        # category = data[0][3]

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
        existing_file =category

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
        file_to_delete = category

        if st.button("Delete Content"):
            with open(file_to_delete, "w") as f:
                f.write("")
            st.success(f"Content of {file_to_delete} deleted successfully!")

        
        selected_department_id = data[0][3]
        with st.expander("Add Staff to Selected Department"):
                staff_id = st.text_input("Staff Id:")
                staff_name = st.text_input("Staff Name:")
                designation = st.text_input("Designation:")
                staff_phone = st.text_input("Phone:")
                
                if st.button("Add Staff"):
                    
                    if staff_id and staff_name and designation and staff_phone:
                        operation.dboperation.add_staff(staff_id,staff_name,designation,selected_department_id,"pass_staff")
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
            if graduate_level == "PG": 
                class_name = st.selectbox("Class:", ["I", "II"]) 
            else: 
                class_name = st.selectbox("Class:", ["I", "II", "III"])
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
            if graduate_level == "PG": 
                class_name = st.selectbox("Class:", ["I", "II"]) 
            else: 
                class_name = st.selectbox("Class:", ["I", "II", "III"])
            
            if st.button("Add Student"):
                if rollno and name and dob and class_name:
                    operation.dboperation.add_student( rollno, name,dob,selected_department_id,class_name)
                    st.success(f"Student '{name}' added to Department ID {selected_department_id}!")
                else:
                    st.error("Please fill all the fields.")

        # Add marks to the selected department
        with st.expander("Add Marks to Selected Student"):
            st.subheader("Mark Entry")
            if graduate_level == "PG": 
                class_name = st.selectbox("Class:", ["I", "II"]) 
            else: 
                class_name = st.selectbox("Class:", ["I", "II", "III"])
            
            if class_name:
                cycle = st.selectbox("Cycle", ["1", "2", "3"])
                
                if cycle:
                    # Fetch students for the selected department and class
                    students = operation.dboperation.view_students(selected_department_id, class_name)
                    students_id = [i[0] for i in students]  # List of student IDs
                    students_names = [i[1] for i in students]  # List of student names
                    subjects = operation.dboperation.view_subjects(selected_department_id, class_name)
                    subjects_id = [i[0] for i in subjects]  # List of student IDs
                    # Select student by name
                    selected_student_id = st.selectbox("Select Student", students_id)
                    subject_id = st.selectbox("select subject",subjects_id)
                    if selected_student_id and subject_id:
                        # Display the roll number for the selected student
                        id = st.text_input("Roll No:", value=selected_student_id, disabled=True)

                        # Inputs for marks

                        quiz = st.number_input("Quiz Marks", min_value=0.0, max_value=5.0, step=1.0)
                        assignment = st.number_input("Assignment Marks", min_value=0.0, max_value=10.0, step=1.0)
                        internal_marks = st.number_input("Internal Marks", min_value=0.0, max_value=25.0, step=1.0)

                        # Check if all inputs are filled before submitting
                        if st.button("submit"):
                            if id and quiz and assignment and internal_marks and cycle:
                                # Add marks to the database
                                operation.dboperation.add_marks(id,subject_id, cycle, quiz, assignment, internal_marks)
                                st.success("Marks added successfully!")
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
                            name ,
                            designation ,
                            department_id ,
                            password ,
                            mfa ,
                            secd ,
                            phone_no ,
                            email 
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
            

            # Timetable View
        st.subheader("Timetable Details")

        # Select class based on graduate level
        class_name = ''
        if graduate_level == "PG":
            class_name = st.selectbox("Class:", ["I", "II"])
        else:
            class_name = st.selectbox("Class:", ["I", "II", "III"])

        if class_name:
            timetable_data = operation.dboperation.view_timetable(department_id, class_name)
            if timetable_data:
                timetable_df = pd.DataFrame(timetable_data, columns=["Day", "Time", "Subject"])

                # Split data into weekdays (Monday to Friday) and Saturday
                weekdays_df = timetable_df[timetable_df['Day'].isin(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])]
                saturday_df = timetable_df[timetable_df['Day'] == "Saturday"]

                # Display weekdays
                if not weekdays_df.empty:
                    weekdays_grouped = weekdays_df.groupby(['Day', 'Time'])['Subject'].first().unstack(fill_value="No Subject")
                    st.write("**Weekday Timetable (Monday to Friday)**")
                    st.table(weekdays_grouped)
                else:
                    st.warning("No weekday timetable found.")

                # Display Saturday
                if not saturday_df.empty:
                    saturday_grouped = saturday_df.groupby(['Day', 'Time'])['Subject'].first().unstack(fill_value="No Subject")
                    st.write("**Saturday Timetable**")
                    st.table(saturday_grouped)
                else:
                    st.warning("No Saturday timetable found.")

                # Update timetable
                st.subheader("Manage Timetable")
                if st.checkbox("Update Timetable"):
                    st.write("Update Timetable Entry")
                    entry_to_update = st.selectbox(
                        "Select Entry to Update",
                        timetable_df.to_dict('records'),
                        format_func=lambda x: f"{x['Day']} {x['Time']} - {x['Subject']}"
                    )
                    if entry_to_update:
                        with st.form("update_timetable_form"):
                            new_day = st.selectbox("Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], index=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"].index(entry_to_update['Day']))
                            new_time = st.text_input("Time", value=entry_to_update["Time"])
                            new_subject = st.text_input("Subject", value=entry_to_update["Subject"])
                            submitted = st.form_submit_button("Update")
                            if submitted:
                                operation.dboperation.update_timetable(department_id, class_name, entry_to_update['Day'], entry_to_update['Time'], new_day, new_time, new_subject)
                                st.success("Timetable entry updated successfully.")

                # Delete timetable
                if st.checkbox("Delete Timetable"):
                    st.write("Delete Timetable Entry")
                    entry_to_delete = st.selectbox(
                        "Select Entry to Delete",
                        timetable_df.to_dict('records'),
                        format_func=lambda x: f"{x['Day']} {x['Time']} - {x['Subject']}"
                    )
                    if entry_to_delete:
                        if st.button("Delete"):
                            operation.dboperation.delete_timetable(department_id, class_name, entry_to_delete['Day'], entry_to_delete['Time'])
                            st.success("Timetable entry deleted successfully.")
            else:
                st.warning("No timetable found for this department.")


        
        # Subject Details
        st.subheader("Subject Details")

        # View Subjects
        if st.button("View Subject Details"):
            subjects = operation.dboperation.view_subjects(department_id)
            if subjects:
                st.write(f"Subject Details for Department: {department_name}")
                subject_df = pd.DataFrame(subjects, columns=["Subject ID", "Name", "Class"])
                st.dataframe(subject_df)
            else:
                st.warning(f"No subjects found for Department: {department_name}")

        # Update Subject
        if st.checkbox("Update Subject"):
            subjects = operation.dboperation.view_subjects(department_id)
            if subjects:
                subject_ids = [subject[0] for subject in subjects]  # Assuming Subject ID is the first field
                selected_subject_id = st.selectbox("Select Subject ID", subject_ids)
                
                # Pre-fill current details
                selected_subject = next((subject for subject in subjects if subject[0] == selected_subject_id), None)
                if selected_subject:
                    current_name = selected_subject[1]  # Assuming Subject Name is the second field
                    current_class = selected_subject[2]  # Assuming Class is the third field
                    
                    new_name = st.text_input("Enter New Subject Name", value=current_name)
                    if graduate_level == "PG":
                        class_name = st.selectbox("Class:", ["I", "II"], index=["I", "II"].index(current_class))
                    else:
                        class_name = st.selectbox("Class:", ["I", "II", "III"], index=["I", "II", "III"].index(current_class))
                    
                    if st.button("Update Subject"):
                        operation.dboperation.update_subject(selected_subject_id, department_id, new_name, class_name)
                        st.success("Subject details updated successfully.")
            else:
                st.warning("No subjects available for update.")

        #
        # Delete Subject
        if st.checkbox("Delete Subject"):
            subjects = operation.dboperation.view_subjects(department_id)
            if subjects:
                subject_ids = [subject[0] for subject in subjects]  # Assuming Subject ID is the first field
                selected_subject_id = st.selectbox("Select Subject ID to Delete", subject_ids)
                
                if st.button("Delete Subject"):
                    operation.dboperation.delete_subject(selected_subject_id)
                    st.success("Subject deleted successfully.")
            else:
                st.warning("No subjects available for deletion.")
        # Student Details
        st.subheader("Student Details")

        # Fetch Students Based on Department and Class
        if graduate_level == "PG":
            class_name = st.selectbox("Select Class:", ["I", "II"])
        else:
            class_name = st.selectbox("Select Class:", ["I", "II", "III"])

        if class_name:
            students = operation.dboperation.view_students(department_id, class_name)
            if students:
                st.write(f"Students in {department_name}, Class {class_name}:")
                student_df = pd.DataFrame(students, columns=["Student ID", "Name", "Date of Birth", "Department ID", "Class"])
                st.dataframe(student_df)
            else:
                st.warning(f"No students found for {department_name}, Class {class_name}.")

        # Update Student
        if st.checkbox("Update Student"):
            if students:
                student_ids = [student[0] for student in students]  # Assuming Student ID is the first field
                selected_student_id = st.selectbox("Select Student ID to Update:", student_ids)

                # Pre-fill fields for the selected student
                selected_student = next((student for student in students if student[0] == selected_student_id), None)
                if selected_student:
                    current_name = selected_student[1]  # Assuming Name is the second field
                    current_dob = selected_student[2]  # Assuming Date of Birth is the third field
                    current_class = selected_student[4]  # Assuming Class is the fifth field

                    with st.form("update_student_form"):
                        st.write("Update Student Details")
                        student_id = st.text_input("Student ID (required):", value=selected_student_id, disabled=True)
                        name = st.text_input("Name:", value=current_name)
                        dob = st.date_input("Date of Birth:", value=pd.to_datetime(current_dob))
                        class_name = st.selectbox("Class:", ["I", "II", "III"], index=["I", "II", "III"].index(current_class))

                        submitted = st.form_submit_button("Update Student")
                        if submitted:
                            if student_id:
                                operation.dboperation.update_student(student_id, name, dob, department_id, class_name)
                                st.success(f"Student {student_id} details updated successfully.")
                            else:
                                st.error("Student ID is required to update details.")
            else:
                st.warning("No students available for update.")

        # Delete Student
        if st.checkbox("Delete Student"):
            if students:
                student_ids = [student[0] for student in students]  # Assuming Student ID is the first field
                selected_student_id = st.selectbox("Select Student ID to Delete:", student_ids)

                if st.button("Delete Student"):
                    operation.dboperation.delete_student(selected_student_id)
                    st.success(f"Student {selected_student_id} deleted successfully.")
            else:
                st.warning("No students available for deletion.")

# Subject-Wise Marks Management
        st.subheader("Subject-Wise Marks Management")

        # Select Department and Class
        if graduate_level == "PG":
            class_name = st.selectbox("Select Class:", ["I", "II"])
        else:
            class_name = st.selectbox("Select Class:", ["I", "II", "III"])

        # Fetch Subjects for Department and Class using view_subject()
        subjects = operation.dboperation.view_subjects(department_id, class_name)
        subject_dict = {subject[1]: subject[0] for subject in subjects}  # Subject Name: Subject ID

        subject_name = st.selectbox("Select Subject", list(subject_dict.keys()))
        subject_id = subject_dict[subject_name]

        # View Marks Subject-Wise
        if st.button("View Marks Subject-Wise"):
            students_marks_data = operation.dboperation.view_marks_class_department(department_id, class_name, subject_id)
            if students_marks_data:
                st.write(f"Subject-Wise Marks for Department: {department_name}, Class: {class_name}, Subject: {subject_name}")
                marks_df = pd.DataFrame(
                    students_marks_data,
                    columns=["Student ID", "Name", "Quiz 1", "Quiz 2", "Quiz 3",
                            "Assignment 1", "Assignment 2", "Internal 1", "Internal 2", "Internal 3"]
                )
                st.dataframe(marks_df)
            else:
                st.warning(f"No marks found for Subject: {subject_name}, Department: {department_name}, Class: {class_name}.")

        # Update Marks by Student ID and Subject ID
        if st.checkbox("Update Marks by Student ID"):
            students = operation.dboperation.view_students(department_id, class_name)
            student_ids = [student[0] for student in students]
            if student_ids:
                student_id = st.selectbox("Select Student ID to Update Marks:", student_ids)
                # Fetch existing marks for selected student
                marks_data = operation.dboperation.view_marks(student_id, subject_id)
                if marks_data:
                    quiz1, quiz2, quiz3, assignment1, assignment2, internal1, internal2, internal3 = marks_data[0][1:]

                    # Input fields to update marks
                    quiz1_new = st.number_input("Quiz 1", value=quiz1)
                    quiz2_new = st.number_input("Quiz 2", value=quiz2)
                    quiz3_new = st.number_input("Quiz 3", value=quiz3)
                    assignment1_new = st.number_input("Assignment 1", value=assignment1)
                    assignment2_new = st.number_input("Assignment 2", value=assignment2)
                    internal1_new = st.number_input("Internal 1", value=internal1)
                    internal2_new = st.number_input("Internal 2", value=internal2)
                    internal3_new = st.number_input("Internal 3", value=internal3)

                    # Update button
                    if st.button("Update Marks"):
                        operation.dboperation.update_marks(
                            student_id,
                            subject_id,
                            quiz1=quiz1_new,
                            quiz2=quiz2_new,
                            quiz3=quiz3_new,
                            assignment1=assignment1_new,
                            assignment2=assignment2_new,
                            internal1=internal1_new,
                           internal2= internal2_new,
                            internal3=internal3_new
                        )
                        st.success(f"Marks for Student ID {student_id} in Subject {subject_name} updated successfully.")
                else:
                    st.warning(f"No existing marks found for Student ID {student_id} in Subject {subject_name}.")
            else:
                st.warning(f"No students found for Department: {department_name}, Class: {class_name}.")

        # Delete Marks by Student ID
        if st.checkbox("Delete Marks by Student ID"):
            students = operation.dboperation.view_students(department_id, class_name)
            student_ids = [student[0] for student in students]
            if student_ids:
                student_id = st.selectbox("Select Student ID to Delete Marks:", student_ids)

                if st.button("Delete Marks"):
                    operation.dboperation.delete_marks(student_id)
                    st.success(f"Marks for Student ID {student_id} deleted successfully.")
            else:
                st.warning(f"No students found for Department: {department_name}, Class: {class_name}.")

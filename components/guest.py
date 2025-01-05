import streamlit as st
import genai.gemini
import operation
# import operation.dboperation
# import operation.fileoperations
import operation.dboperation
import operation.fileoperations
import operation.preprocessing
import json
import genai
import operation
import os
def guest_page():
    # Initialize session state variables
    if 'qa_list' not in st.session_state:
        st.session_state.qa_list = []
    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'input' not in st.session_state:
        st.session_state.input = ""
    if 'stored_value' not in st.session_state:
        st.session_state.stored_value = ""

    # Sidebar for navigation and displaying past Q&A
    with st.sidebar:
        if st.button("Go to Login"):
            st.session_state.page = "login"
            st.rerun()

        for qa in reversed(st.session_state.qa_list):
            st.write(f"**Question:** {qa['question']}")
            st.write(f"**Answer:** {qa['answer']}")
            st.write("---")
    if "qa_list" in st.session_state and len(st.session_state.qa_list) % 3 == 0 and len(st.session_state.qa_list):
        # qa_list exists and its length is a multiple of 3
        st.write("qa_list exists and its length is a multiple of 3.")
        with st.popover("feedback"):
            user_id = st.text_input("User ID")
            name = st.text_input("Your Name")
            message = st.text_area("Your Feedback")
            
            if st.button("Submit Feedback"):
                if user_id and name and message:
                    operation.dboperation.add_feedback(user_id, name, message)
                else:
                    st.warning("Please fill all the fields to submit your feedback.")
            
    
    # Load text files for college and department history
    # with open("collegehistory.txt", "r") as f:
    #     collegehistory = f.read()
    # with open("departmenthistory.txt", "r") as f:
    #     departmenthistory = f.read()
    # default,default_sql=operation.fileoperations.read_default_files()
    # Display guest welcome message
    st.title("Welcome, Guest!")
    st.write("You can explore the site as a guest, but you'll need to log in for full role-based access.")

    # Ask for the user's name
    if not st.session_state.username:
        st.session_state.username =''
    name = ''
    if not name and not st.session_state.username:
        name=st.text_input('Enter your name:', placeholder='John', key='name')
        st.session_state.username = name
    
        # st.write(f"Hello, {name}!")

    # Process questions if the username is set
    if st.session_state.username:
        role_prompt = operation.fileoperations.read_from_file('default.txt')
        folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../files/"))

        # Define the list of files to exclude
        excluded_files = {'staff_role.txt', 'staff_sql.txt', 'student_role.txt', 'student_sql.txt', 'default.txt'}

        # Get all files in the folder except the excluded ones
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f not in excluded_files]
        info=''
        # Print the filtered files
        for file in files:
            info += str(operation.fileoperations.read_from_file(file))
        
        chunks=operation.preprocessing.chunk_text(info)
        st.write(f"Hello, {st.session_state.username}!")
        # chunks = operation.preprocessing.chunk_text(f"{collegehistory}\n{departmenthistory}")
        question = st.chat_input("Ask your question")

        if question:
            # Retrieve relevant chunks
            relevant_chunks = operation.preprocessing.get_relevant_chunks(question, chunks)
            context = "\n\n".join(relevant_chunks)

            # Display relevant context
            # st.write("Relevant context:")
            # st.write(context)

            # Query LM Studio for the answer
            with st.spinner("Generating answer..."):
                answer = genai.gemini.model.generate_content(
                    f"use the data {context} and frame the answer for this question {question} use this template  in formal english"
                )
                result_text = answer.candidates[0].content.parts[0].text

                # Store the question and answer in session state
                st.session_state.qa_list.append({'question': question, 'answer': result_text})

                # Display the current question and answer
                st.chat_message('user').markdown(f"**Question:** {question}")
                st.chat_message('ai').markdown(f"**Answer:** {result_text}")
                
#                 txt = genai.gemini.model.generate_content(f"{question} give 1 if the question needs an SQL query or 0")
#                 data = ''
#                 if txt.text.strip() != '0':
#                     response = genai.gemini.model.generate_content(f"{default_sql}\n\n{question}")
#                     raw_query = response.text
#                     formatted_query = raw_query.replace("sql", "").strip("'''").strip()
#                     single_line_query = " ".join(formatted_query.split()).replace("```", "")
#                     data = operation.dboperation.read_sql_query(single_line_query)

#                 # Format data for readability
#                 formatted_data = json.dumps(data, indent=2) if isinstance(data, (dict, list)) else str(data)

#                 # Generate answer using the context and formatted data
#                 answer = genai.gemini.model.generate_content(
#                     f"use the data {context} and frame the answer for this question {question} use this template  in formal english"
#                 )
#                 result_text = answer.candidates[0].content.parts[0].text

#                 # Store the question and answer in session state
#                 st.session_state.qa_list.append({'question': question, 'answer': result_text})

#                 # Display the current question and answer
#                 st.markdown(f"**Question:** {question}")
#                 st.markdown(f"**Answer:** {result_text}")
# #login page

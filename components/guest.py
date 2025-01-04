import streamlit as st
import genai.gemini
import operation
# import operation.dboperation
# import operation.fileoperations
import operation.preprocessing
import json
import genai
import operation
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
            st.session_state.page = "admin"
            st.rerun()

        for qa in reversed(st.session_state.qa_list):
            st.write(f"**Question:** {qa['question']}")
            st.write(f"**Answer:** {qa['answer']}")
            st.write("---")

    # Load text files for college and department history
    with open("collegehistory.txt", "r") as f:
        collegehistory = f.read()
    with open("departmenthistory.txt", "r") as f:
        departmenthistory = f.read()
    default,default_sql=operation.fileoperations.read_default_files()
    # Display guest welcome message
    st.title("Welcome, Guest!")
    st.write("You can explore the site as a guest, but you'll need to log in for full role-based access.")

    # Ask for the user's name
    name = ''
    if not name and not st.session_state.username:
        name=st.text_input('Enter your name:', placeholder='John', key='name')
        st.session_state.username = name
    
        # st.write(f"Hello, {name}!")

    # Process questions if the username is set
    if st.session_state.username:
        st.write(f"Hello, {st.session_state.username}!")
        chunks = operation.preprocessing.chunk_text(f"{collegehistory}\n{departmenthistory}")

        def process_and_clear():
            st.session_state.stored_value = st.session_state.input
            st.session_state.input = ""

        # Input field for the user's question
        st.text_area('Input your question:', key='input', on_change=process_and_clear)
        question = st.session_state.stored_value

        if question:
            # Retrieve relevant chunks
            relevant_chunks = operation.preprocessing.get_relevant_chunks(question, chunks)
            context = "\n\n".join(relevant_chunks)

            # Display relevant context
            # st.write("Relevant context:")
            # st.write(context)

            # Query LM Studio for the answer
            with st.spinner("Generating answer..."):
                txt = genai.gemini.model.generate_content(f"{question} give 1 if the question needs an SQL query or 0")
                data = ''
                if txt.text.strip() != '0':
                    response = genai.gemini.model.generate_content(f"{default_sql}\n\n{question}")
                    raw_query = response.text
                    formatted_query = raw_query.replace("sql", "").strip("'''").strip()
                    single_line_query = " ".join(formatted_query.split()).replace("```", "")
                    data = operation.dboperation.read_sql_query(single_line_query)

                # Format data for readability
                formatted_data = json.dumps(data, indent=2) if isinstance(data, (dict, list)) else str(data)

                # Generate answer using the context and formatted data
                answer = genai.gemini.model.generate_content(
                    f"use the data {context} and frame the answer for this question {question} use this template {default} in formal english"
                )
                result_text = answer.candidates[0].content.parts[0].text

                # Store the question and answer in session state
                st.session_state.qa_list.append({'question': question, 'answer': result_text})

                # Display the current question and answer
                st.markdown(f"**Question:** {question}")
                st.markdown(f"**Answer:** {result_text}")
#login page

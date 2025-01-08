import streamlit as st
import genai.gemini
import operation
import operation.dboperation
import operation.otheroperation
import operation.fileoperations
import operation.preprocessing
import operation.qrsetter
import genai
import os
def welcome_page():
    # st.set_page_config(page_title="Anjac_AI", layout="wide")
    data = operation.dboperation.view_student(st.session_state.user_id)
    
    #operation.dboperation.update_multifactor_status(st.session_state.user_id, st.session_state.multifactor ,secret)  # Update MFA status in the database
    # Sidebar content
    with st.sidebar:
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

# Main page user menu using expander
    with st.expander(f"Welcome, {data[1]}! 🧑‍💻"):
        st.write("Choose an action:")
        with st.popover("profile"):
            st.write(f"name:{data[1]}")
            st.write(f"rollno:{st.session_state.user_id}")
        with st.popover("settings"):
            st.write()
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.page = "login"
            st.rerun()

    # Main page content
    st.title("Welcome to the ANJAC AI")
    st.write(f"Hello, {data[1]}!")
    st.subheader(operation.otheroperation.get_dynamic_greeting())
    st.write("---")
    st.write(f"🎓 **Fun Fact:** {operation.otheroperation.get_fun_fact()}")
    
    # Initialize session state
    if 'qa_list' not in st.session_state:
        st.session_state.qa_list = []
    # st.header(f"{st.session_state.role} Role Content:")
    # st.text(st.session_state.role_content)
    # st.header(f"{st.session_state.role} SQL Content:")
    # st.text(st.session_state.sql_content)
    # role = st.session_state.role
    role_prompt=operation.fileoperations.read_from_file("student_role.txt")
    sql_content = operation.fileoperations.read_from_file("student_sql.txt")
    # st.write(sql_content)
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
    
    #question1 = st.text_area('Input your question:', key='input',on_change=process_and_clear)
    # submit = st.button('Ask the question')
    
    question=st.chat_input("Ask the question")
    if question:
        combined_prompt = operation.preprocessing.create_combined_prompt(question, sql_content)
        response = genai.gemini.get_gemini_response(combined_prompt,data[0][0:4])
        
        # Display the SQL query
        # st.write("Generated SQL Query:", response)
        raw_query = response
        formatted_query = raw_query.replace("sql", "").strip("'''").strip()
        # print("formatted :",formatted_query)
        single_line_query = " ".join(formatted_query.split()).replace("```", "")
        print(single_line_query)
        # Query the database
        data_sql = operation.dboperation.read_sql_query(single_line_query)
        # print(data_sql)
        if isinstance(data_sql, list):
            #st.write("according to,")
            #st.table(data)
            pass
            
        else:
            #st.write(data)
            # Display any errors
            pass
        # Generate response for the question and answer
        relevent_chunk=operation.preprocessing.get_relevant_chunks(question,chunks)
        # context = "{question}"+str(data_sql)+relevent_chunk
        # question = "I want the staff detail and the student timetable"
        options = ["department", "timetable", "student", "student_mark", "subject", "staff"]

        matched_words = [option for option in options if option in question]

       
        matchword = ', '.join(matched_words)
        retrived_answer = question+str(data_sql)
        relevent_chunk.append(retrived_answer)
        context = ''.join(relevent_chunk)
        print(str(data_sql))
        st.write(relevent_chunk)
        # st.write(context)
        # print (context)
        from datetime import datetime
        current_datetime = datetime.now()
        # Address the user's question by utilizing the database information provided: {str(data_sql)} format and give this. 
        answer = genai.gemini.model.generate_content(
f"""Please interact with the user without ending the communication prematurely dont restrict the user. 
Use the following staff name: {data[0][0:4]} use the word according to or dear. 
current date and time  {current_datetime.strftime("%A, %B %d, %Y, at %I:%M %p")} ,{datetime.now()}.
Format your response based on this role prompt: {role_prompt} but don't provide the content inside it. 
relevent general context into your response: {context} for this question {question}"""
)

        # result_text = answer.candidates[0].content.parts[0].text
        result_text = answer.text
        st.chat_message('assistant').markdown(result_text)
        # Store the question and answer in session state
        st.session_state.qa_list.append({'question': question, 'answer': result_text})

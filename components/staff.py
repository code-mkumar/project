import streamlit as st
import genai.gemini
import operation
# import operation.dboperation
import operation.dboperation
import operation.preprocessing
import operation.qrsetter
import genai
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

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
import time
import random

# Function to display a dynamic welcome message
def get_dynamic_greeting():
    hour = time.localtime().tm_hour
    if hour < 12:
        return "Good Morning! Welcome to Anjac AI."
    elif 12 <= hour < 18:
        return "Good Afternoon! Glad to see you here."
    else:
        return "Good Evening! How can I assist you today?"

# Function to display a random fun fact
def get_fun_fact():
    fun_facts = [
        
        🏫 History in a Name: ANJAC is named after the generous founders Thiru P. Ayya Nadar and Thirumathi A. Janaki Ammal,
        🌏 Little Japan Connection: Located in Sivakasi, also known as Little Japan, ANJAC has a legacy of excellence since 1963,
        🌳 Vast and Vibrant Campus: Spread over 157 acres, ANJAC is a self-sufficient educational hub,
        🏆 NIRF Top 100: Ranked 69th in NIRF 2023, showcasing academic and research excellence,
        ✨ NAAC ‘A+’ Excellence: Re-accredited with a stellar CGPA of 3.48 by NAAC,
        🍄 Mushroom Centre Marvel: ANJAC features its own Mushroom Cultivation Centre,
        ♻️ Eco-Friendly Practices: The campus recycles lab water through a Water Treatment Grid,
        📶 Wi-Fi Wonderland: Entire campus enjoys blazing-fast Wi-Fi at 100 Mbps,
        🚀 Student Startup Hub: ANJAC’s All-Hub encourages innovative ideas and entrepreneurship,
        📚 Digital Library: Access over 1 lakh books and 110 journals through its advanced digital library,
        🦯 Inclusive Tech: Braille materials and assistive technologies support visually challenged students,
        🏅 Sports Powerhouse: A 50-bed UGC Sports Hostel nurtures athletic talent,
        📻 Community Radio: ANJA Community Radio connects and educates the surrounding community,
        🌈 Dynamic Diversity: With 36 academic associations, there’s something for everyone,
        🌿 Nature at Heart: Tree-growing competitions and an ornamental garden promote eco-awareness,
        📜 Certificate Extravaganza: Offers 39 certificate courses ranging from Animation to Tourism,
        🚨 Anti-Ragging Pledge: ANJAC has a 24x7 anti-ragging helpline for a safe campus,
        🌱 Green Goals: Initiatives like vermicomposting and mushroom cultivation lead sustainability efforts,
        🎭 Cultural Competitions: From Fresher’s Day to national events, ANJAC celebrates talent in style,
        💻 Tech Titans: Boasts over 600 high-configured computers and cutting-edge software for futuristic learning,
    ]
    return random.choice(fun_facts)
    
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
    st.subheader(get_dynamic_greeting())
    st.write("---")
    st.write(f"🎓 **Fun Fact:** {get_fun_fact()}")
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
            st.chat_message('user').markdown(question)
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
                # st.chat_message('user').markdown(f"**Question:** {question}")
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

import streamlit as st
import operation
# import operation.dboperation
# import operation.fileoperations
import operation.qrsetter
def otp_verification_page():
    # st.set_page_config(page_title="verify")
    st.title("Verify OTP")
    user_id = st.session_state.user_id
    secret, role, name = operation.dboperation.get_user_details(user_id)
    st.session_state.id=user_id
    st.session_state.role = role
    st.session_state.name = name
    

    otp = st.text_input("Enter OTP", type="password")
    if st.button("Verify"):
        if not operation.qrsetter.verify_otp(secret, otp):
            st.success("OTP Verified! Welcome.")
            
            if role == "student":
                role_content, sql_content = operation.fileoperations.read_student_files()
                st.session_state.role_content = role_content
                st.session_state.sql_content = sql_content
                st.session_state.page = "welcome"
                st.rerun()
            if role == "staff":
                role_content,sql_content = operation.fileoperations.read_staff_files()
                st.session_state.role_content = role_content
                st.session_state.sql_content = sql_content
                st.session_state.page = "staff"
                st.rerun()
            if role == "admin":
                role_content,sql_content = operation.fileoperations.read_admin_files()
                st.session_state.role_content = role_content
                st.session_state.sql_content = sql_content
                st.session_state.page = "admin"
                st.rerun()
            
        else:
            st.error("Invalid OTP. Try again.")

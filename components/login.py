import streamlit as st
import operation
import operation.dboperation
def login_page():
    st.set_page_config(page_title="Login")
    st.title("Login")
    user_id = st.text_input("User ID")
    role = get_role(user_id)
    dob=''
    password=''
    if role == "student_details":
        dob = st.date_input()
    else
        password = st.text_input("Password", type="password")

    if st.button("Login"):
        if user and (password or dob):
            # st.session_state.authenticated = True
            st.session_state.user_id = user_id
            user = check_user(user_id,password,role)
            if not user:    
            # st.session_state.multifactor = user[8]  # Multifactor column
            # st.session_state.secret = user[9]  # Secret code column
                st.success("Login successful!")
                # if st.session_state.multifactor == 1:
                #     st.session_state.page = "otp_verification"  # Direct to OTP verification if MFA is enabled
                #     st.rerun()
                # else:
                #     if st.session_state.secret == "None":
                #         st.session_state.page = "qr_setup"  # If MFA is not enabled, show QR setup
                #         st.rerun()
                #     else:
                #         st.session_state.page = "otp_verification"  # Otherwise show OTP verification
                #         st.rerun()
                st.session_state.page = "admin"
            else:
                st.error("Invalid credentials.")
    if st.button("←--"):
        st.session_state.page = "guest"
        st.rerun()


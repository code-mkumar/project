import streamlit as st
import operation
import operation.dboperation
def login_page():
    # st.set_page_config(page_title="Login")
    st.title("Login")
    user_id = st.text_input("User ID")
    # role = operation.dboperation.get_user_details(user_id)
    #if role == "student":
    #   st.date_input
    #else
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        conn = operation.dboperation.create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_detail WHERE id = ? AND password = ?", (user_id, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            st.session_state.authenticated = True
            st.session_state.user_id = user_id
            st.session_state.multifactor = user[8]  # Multifactor column
            st.session_state.secret = user[9]  # Secret code column
            st.success("Login successful!")
            if st.session_state.multifactor == 1:
                st.session_state.page = "otp_verification"  # Direct to OTP verification if MFA is enabled
                st.rerun()
            else:
                if st.session_state.secret == "None":
                    st.session_state.page = "qr_setup"  # If MFA is not enabled, show QR setup
                    st.rerun()
                else:
                    st.session_state.page = "otp_verification"  # Otherwise show OTP verification
                    st.rerun()
        else:
            st.error("Invalid credentials.")
    if st.button("←--"):
        st.session_state.page = "guest"
        st.rerun()
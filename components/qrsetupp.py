import streamlit as st
import operation
import operation.dboperation
import operation.fileoperations
import operation.qrsetter
import operation.secretcode

def qr_setup_page():
    # st.set_page_config(page_title="QRcode")
    st.title("Setup Multifactor Authentication")
    user_id = st.session_state.user_id
    
    if st.session_state.secret == "None":
        # Generate a new secret
        secret = operation.secretcode.generate_secret_code(user_id)
        st.session_state.secret = secret
    else:
        secret = st.session_state.secret

    # Display QR Code
    qr_code_stream = operation.qrsetter.generate_qr_code(user_id, secret)
    st.image(qr_code_stream, caption="Scan this QR code with your authenticator app.")
    st.write(f"Secret Code: `{secret}` (store this securely!)")
    operation.dboperation.update_multifactor_status(user_id, 0 ,secret)  # Update MFA status in the database
    # Immediate OTP verification
    otp = st.text_input("Enter OTP from Authenticator App", type="password")
    if st.button("Verify OTP"):
        # secret, role, name = get_user_details(st.session_state.user_id)
        if not operation.qrsetter.verify_otp(st.session_state.secret, otp):
            st.session_state.multifactor = 1
            _, role, name = operation.dboperation.get_user_details(user_id)
            st.session_state.id=user_id
            st.session_state.role = role
            st.session_state.name = name
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
            st.success("Multifactor authentication is now enabled.")
            # st.session_state.page = "welcome"
            # st.rerun()
        else:
            st.error("Invalid OTP. Try again.")

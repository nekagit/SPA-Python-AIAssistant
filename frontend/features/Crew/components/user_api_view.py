from api import user_service
import streamlit as st
def show_user_api_view():
    # Streamlit UI
    st.subheader("Fetch Users")
    if st.button("Fetch All Users", key="fetch_Users_button"):
        users = user_service.fetch_users()
        st.write(users)

    st.subheader("Fetch User by ID")
    user_id = st.number_input("user ID", min_value=1)
    if st.button("Fetch User"):
        user = user_service.fetch_user_by_id(user_id)
        st.write(user)

    st.subheader("Create New User")
    with st.form("create_user_form"):
        new_id = st.number_input("ID", min_value=1)
        new_name = st.text_input("Name")
        new_email = st.text_input("Email")
        new_password = st.number_input("Password")
        new_is_admin = st.checkbox("Admin", value=True)
        create_submit = st.form_submit_button("Create user")

        if create_submit:
            new_user = {
                "id": new_id,
                "name": new_name,
                "email": new_email,
                "password": new_password,
                "isAdmin": new_is_admin
            }
            user_service.create_user(new_user)

    st.subheader("Update User")
    with st.form("update_user_form"):
        update_id = st.number_input("Update ID", min_value=1)
        update_name = st.text_input("Update Name")
        update_email = st.text_input("Update Email")
        update_password = st.number_input("Update Password")
        update_is_admin = st.checkbox("Update Admin", value=True)
        update_submit = st.form_submit_button("Update user")

        if update_submit:
            updated_user = {
                "id": update_id,  # Ensure ID is included for PUT request
                "name": update_name,
                "email": update_email,
                "password": update_password,
                "isAdmin": update_is_admin
            }
            user_service.update_user(update_id, updated_user)

    st.subheader("Delete User")
    delete_id = st.number_input("Delete User ID", min_value=1)
    if st.button("Delete User"):
        user_service.delete_user(delete_id)

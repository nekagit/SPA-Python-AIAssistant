from api import task_service
import streamlit as st
import uuid

def show_task_api_view():
    # Streamlit UI
    st.subheader("Fetch Tasks")
    if st.button("Fetch All Tasks", key=f"fetch_tasks_button_{uuid.uuid4()}"):
        tasks = task_service.fetch_tasks()
        st.write(tasks)

    st.subheader("Fetch Task by ID")
    task_id = st.number_input("Task ID", min_value=1, key=f"ID_tasks_number_input_{uuid.uuid4()}")
    if st.button("Fetch Task", key=f"fetch_task_button_{uuid.uuid4()}"):
        task = task_service.fetch_task_by_id(task_id)
        st.write(task)

    st.subheader("Create New Task")
    with st.form(f"create_task_form_{uuid.uuid4()}"):
        new_id = st.number_input("ID", min_value=1)
        new_name = st.text_input("Name")
        create_submit = st.form_submit_button("Create Task")

        if create_submit:
            new_task = {
                "id": new_id,
                "name": new_name,
            }
            task_service.create_task(new_task)

    st.subheader("Update Task")
    with st.form(f"update_task_form{uuid.uuid4()}"):
        update_id = st.number_input("Update ID", min_value=1)
        update_name = st.text_input("Update Name")
        update_submit = st.form_submit_button("Update Task")

        if update_submit:
            updated_task = {
                "id": update_id,  # Ensure ID is included for PUT request
                "name": update_name,
            }
            task_service.update_task(update_id, updated_task)

    st.subheader("Delete Task")
    delete_id = st.number_input("Delete Task ID", min_value=1, key=f"Delete_tasks_{uuid.uuid4()}")
    if st.button("Delete Task", key=f"Delete_task_{uuid.uuid4()}"):
        task_service.delete_task(delete_id)

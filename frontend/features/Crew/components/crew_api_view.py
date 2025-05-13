from api import crew_service
import streamlit as st


def show_crew_api_view():
    # Streamlit UI
    st.subheader("Fetch Crews")
    if st.button("Fetch All Crews", key="fetch_Crews_button"):
        crews = crew_service.fetch_crews()
        st.write(crews)

    st.subheader("Fetch Crew by ID")
    crew_id = st.number_input("Crew ID", min_value=1)
    if st.button("Fetch Crew"):
        crew = crew_service.fetch_crew_by_id(crew_id)
        st.write(crew)

    st.subheader("Create New Crew")
    with st.form("create_crew_form"):
        new_id = st.number_input("ID", min_value=1)
        new_name = st.text_input("Name")
        create_submit = st.form_submit_button("Create Crew")

        if create_submit:
            new_crew = {
                "id": new_id,
                "name": new_name,
            }
            crew_service.create_crew(new_crew)

    st.subheader("Update Crew")
    with st.form("update_crew_form"):
        update_id = st.number_input("Update ID", min_value=1)
        update_name = st.text_input("Update Name")
        update_submit = st.form_submit_button("Update Crew")

        if update_submit:
            updated_crew = {
                "id": update_id,  # Ensure ID is included for PUT request
                "name": update_name,
            }
            crew_service.update_crew(update_id, updated_crew)

    st.subheader("Delete Crew")
    delete_id = st.number_input("Delete Crew ID", min_value=1)
    if st.button("Delete Crew"):
        crew_service.delete_crew(delete_id)

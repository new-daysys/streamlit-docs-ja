import streamlit as st

st.set_page_config(
    page_title='Exercise.1',
    page_icon="👋",
    )

st.write("# Sales by item 👋")
st.sidebar.success("Select a demo above.")

st.markdown(
    """
        Streamlit is an open-source app framework built specifically for
        Machine Learning and Data Science projects.

        **👈 Select a demo from the dropdown on the left** to see some examples
        of what Streamlit can do!
    """
)

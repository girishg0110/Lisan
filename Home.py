import streamlit as st

st.set_page_config(
    page_title="Welcome to Lisan",
    page_icon="👋",
)

st.write("# Welcome to Lisan! 👋")

st.sidebar.success("Head to Story mode to interact with the Lisan storytelling agent.")

st.markdown(
    """
    Lisan (pron. lee-saan) uses collaborative storytelling to fill the market gap in intermediate-level language learning services. 
    Users will develop professional competency in an international language (like English, Arabic, French, etc...) by writing a story with Claude. 
    Feedback on vocabulary and grammar will be provided, and new words will be logged for export into online flashcard services like Anki and Quizlet. 
    """
)
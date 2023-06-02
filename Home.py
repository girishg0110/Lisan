import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

import streamlit as st

st.set_page_config(
    page_title="Welcome to Lisan",
    page_icon="👋",
)

st.write("# Welcome to Lisan! 👋")

st.sidebar.success("Head to Story mode to interact with the Lisan storytelling agent.")

st.markdown(
    """
    Lisan (pron. lee-saan) uses collaborative storytelling to fill the market gap in intermediate-level language learning services. Users will develop professional competency in an international language (like English, French, Spanish, etc...) by writing a story with Lisan.

    🧠 Receive immediate feedback on your sentences.
    👩‍🏫 Tailor Lisan to match your CEFR language level.
    🎤 Hear Lisan speak in your language.
    ⛏️ Get a word-level breakdown of all sentences in the story.
    📂 Export flashcards for use on platforms like Anki and Quizlet.
    📈 View analytics on a personalized dashboard.
    """
)
import streamlit as st
import pandas as pd

st.title("Flashcards")

if 'flashcards' not in st.session_state:
    st.session_state.flashcards = pd.DataFrame(columns = ["English", "Language", "Hint"])

@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')

flashcard_csv = convert_df(st.session_state.flashcards)

st.dataframe(st.session_state.flashcards)
st.download_button(
    label="Download Flashcards",
    data=flashcard_csv,
    file_name='flashcards.csv',
    mime='text/csv',
)

storywriter = st.session_state.storywriter
st.write(storywriter.story_history)
st.download_button(
    label="Download Story",
    data=storywriter.story_history,
    file_name='story.txt',
    mime='text/text'
)
import streamlit as st
from annotated_text import annotated_text
import pandas as pd

import sys
sys.path.append('./utils')
from ml_utils import StoryAgent, FeedbackAgent, tts


st.title("Lisan")
###
language = st.sidebar.selectbox(
    "What is your target language?",
    ("French", "Spanish", "German", "Italian", "Portuguese")    
)
user_sentence = st.sidebar.text_area("Type sentence: ")
user_submit = st.sidebar.button("Add Sentence")
###
st.sidebar.divider()
###
structure_complexity = st.sidebar.select_slider(
    "Desired sentence complexity",
    ("Low", "Medium", "High"),
    value="Medium"
)
###

def add_row(row):
    n_rows = len(st.session_state.flashcards)
    st.session_state.flashcards.loc[n_rows] = row
if 'flashcards' not in st.session_state:
    st.session_state.flashcards = pd.DataFrame(columns = ["English", language, "Hint"])
if 'storywriter' not in st.session_state:
    st.session_state.storywriter = StoryAgent(language)
storywriter = st.session_state.storywriter
editor = FeedbackAgent(language)

if user_submit:
    with st.spinner(text="Lisan is critiquing..."):
        feedback = editor.get_feedback(user_sentence)

    user_advice = feedback["Analysis"]
    user_correction = feedback["Correction"]
    user_translation = feedback["Translation"]

    if user_advice == "N/A":
        st.write("Great! Your sentence is grammatically correct and well-formatted.")
        st.write(user_sentence)
    else:
        st.write(f"Instead of \"{user_sentence}\", write \"{user_correction}\".")
        st.write(user_advice)
    with st.spinner(text="You are speaking..."):
        user_audio_file = tts(user_correction, 'fr')
    user_audio = st.audio(data=user_audio_file)
    with st.expander("Show translation"):
        st.write(user_translation)

    st.divider()

    with st.spinner(text="Lisan is thinking..."):
        ai_json = storywriter.send_sentence(user_sentence, structure_complexity)

    ai_sentence = ai_json["Sentence"]
    ai_word_trans = ai_json["Word-Level Translation"]
    ai_translation = ai_json["Translation"]

    with st.spinner(text="Lisan is speaking..."):
        ai_audio_file = tts(ai_sentence, 'fr')
    ai_audio = st.audio(data=ai_audio_file)
    with st.expander("Show transcription"):
        st.write(ai_sentence)
    with st.expander("Show translation"):
        st.write(ai_translation)
        st.json(ai_word_trans)

    add_row([user_translation, user_correction, user_sentence])
    add_row([ai_translation, ai_sentence, ai_word_trans])
    

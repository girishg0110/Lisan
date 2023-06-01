from dotenv import load_dotenv
import streamlit as st
import anthropic
# from flask import Flask
import os

load_dotenv()
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
claude = anthropic.Client(anthropic_api_key)

# app = Flask(__name__)

# Stages:
#   (1) Console App
#   (2) Streamlit Deployment
#   (3) Stateful API & Frontend *
#   (4) Stateless API w/ Database


# Command Loop: {EN <-> FR}
# START.
# The LLM writes a sentence. The user translates.
# The LLM judges. The user writes a sentence. The LLM judges.
# Goto START.
# Need to call for (1) story completion and (2) judging -> extract poorly used vocab
# 1) POST /story-completion/ {story_history} => story_history[-1] = last user sentence
# : return {story_history}* , translation of story_history[-1], feedback on previous sentence
# Run two agents. One for telling the story and exchanging sentences. One acts on user sentences and gives feedback, also extracts poorly used words.
# Will eventually store conversations in a database and just send conversation_id to the user

class FeedbackAgent:
    target_language = ""

    def __init__(self, target_language):
        self.target_language = target_language

    def get_feedback(self, user_sentence):
        prompt_setup = f"""{anthropic.HUMAN_PROMPT} You are a {target_language} language tutor. 
            I will write a sentence in {target_language} and you will give feedback on the correctness 
            of that sentence:\n{user_sentence}{anthropic.AI_PROMPT}"""
        claude_response = claude.completion(
            prompt=prompt_setup,
            max_tokens_to_sample=300,
            model="claude-v1",
        )
        feedback = claude_response['completion']
        return feedback


class StoryAgent:
    system_message = ""
    story_history = ""

    def __init__(self, target_language):
        self.system_message = f"{anthropic.HUMAN_PROMPT} You are a {target_language} language tutor. Continue the following story with one sentence:\n"
        self.story_history = ""

    def send_message(self, new_message):
        self.story_history += new_message 
        prompt_input = f"""{self.system_message}{self.story_history} {anthropic.AI_PROMPT}"""

        claude_response = claude.completion(
            prompt=prompt_input, 
            max_tokens_to_sample=300,
            model="claude-v1"
        )
        #print(claude_response)
        assistant_response = claude_response['completion']
        self.story_history += ' ' + assistant_response

        return assistant_response


def display_conversation(convo):
    for exchange in convo:
        student, tutor = exchange
        st.write(student)
        st.write(tutor)


if __name__ == "__main__":
    st.title("Lisan")
    target_language = st.sidebar.text_input("Language: ")
    storywriter = StoryAgent(target_language)
    tutor = FeedbackAgent(target_language)
    i = 0
    new_message = st.sidebar.text_input("You: ", i)
    submit_message = st.sidebar.button("Add Sentence")
    if submit_message:
        response = storywriter.send_message(new_message)

    st.write(storywriter.story_history)
    # app.run(debug=True)

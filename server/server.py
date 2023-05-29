import openai
from dotenv import load_dotenv
import streamlit as st
#from flask import Flask
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

#app = Flask(__name__)

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
        prompt_setup = [
            {"role" : "system", "content" : "You are a {target_language} language tutor. I will write a sentence in {target_language} and you will give feedback on the correctness of that sentence."},
            {"role" : "user", "content" : user_sentence}
        ]
        gpt_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt_setup
        )
        feedback = gpt_response['choices'][0]['message']['content']
        return feedback

class StoryAgent:
    system_message = ""
    story_history = []

    def __init__(self, target_language):
        self.system_message = f"You are a {target_language} language tutor. We will play a collaborative story-writing game where we take turns writing one sentence each of a story. "
        self.story_history.append({
            "role" : "system",
            "content" : self.system_message
        })
    
    def send_message(self, new_message):
        self.story_history.append({
            "role" : "user", 
            "content" : new_message
        })

        gpt_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.story_history
        )
        assistant_response = gpt_response['choices'][0]['message']['content']
        self.story_history.append({
            "role": "assistant", 
            "content": assistant_response
        })

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
    conversation = []
    if submit_message:
        response = storywriter.send_message(new_message)
        conversation.append([new_message, response])
        #feedback = tutor.get_feedback(new_message)
        #st.write(f"Feedback: {feedback}")
        
    display_conversation(conversation)
    #app.run(debug=True)

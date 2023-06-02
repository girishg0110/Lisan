from dotenv import load_dotenv
import anthropic
import json
from gtts import gTTS
from io import BytesIO
import streamlit as st

load_dotenv()
anthropic_api_key = st.secrets["ANTHROPIC_API_KEY"]
claude = anthropic.Client(anthropic_api_key)

class FeedbackAgent:
    language = ""

    def __init__(self, language):
        self.language = language

    def get_feedback(self, user_sentence):
        prompt_setup = f"""{anthropic.HUMAN_PROMPT} You are a {self.language} language tutor. 
            I will write a sentence in {self.language} and you will response with a JSON with the following field(s):
            (1) Analysis: An explanation of the grammatical and syntactical mistakes made in the user's sentence. If there are none, write N/A.
            (2) Correction: A corrected version of the user's sentence.
            (3) Translation: A translation of the correction into English.
            \n{user_sentence}
            {anthropic.AI_PROMPT}"""

        claude_response = claude.completion(
            prompt=prompt_setup,
            max_tokens_to_sample=300,
            model="claude-v1",
        )

        feedback = claude_response['completion']
        feedback_json = json.loads(feedback)
        return feedback_json


class StoryAgent:
    story_history = ""
    language = ""

    def __init__(self, language):
        self.language = language
        self.story_history = ""

    def send_sentence(self, new_message, structure_complexity, attempts = 3):
        self.story_history += new_message 
        prompt_input = f"""{anthropic.HUMAN_PROMPT} You are a {self.language} language tutor. 
            Respond to the following story with a JSON with three fields: 
            (1) Sentence: A {self.language} sentence of {structure_complexity.lower()} structural complexity that continues the story,
            (2) Word-Level Translation: A JSON of translations of each individual word in your sentence to English, and
            (3) Translation: A translation of your new sentence to English:\n
            {self.story_history} 
            {anthropic.AI_PROMPT}"""
        
        for attempt_idx in range(attempts):
            claude_response = claude.completion(
                prompt=prompt_input, 
                max_tokens_to_sample=300,
                model="claude-v1"
            )
            ai_response = claude_response['completion']
            try: 
                ai_json = json.loads(ai_response)
            except:
                print("Failed! Retrying...")
                continue
            break
        self.story_history += ' ' + ai_json["Sentence"]
        return ai_json

    def summarize(self):
        prompt_input = f"""{anthropic.HUMAN_PROMPT} Summarize the following story in English:\n
            {self.story_history} 
            {anthropic.AI_PROMPT}"""

        claude_response = claude.completion(
            prompt=prompt_input, 
            max_tokens_to_sample=300,
            model="claude-v1"
        )
        ai_response = claude_response['completion']
        return ai_response

def tts(sentence, lang_code):
    fp = BytesIO()
    ttsObject = gTTS(sentence, lang=lang_code)
    ttsObject.write_to_fp(fp)
    return fp

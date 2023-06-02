# Lisan

Lisan (pron. lee-saan) uses collaborative storytelling to fill the market gap in intermediate-level language learning services. Users will develop professional competency in an international language (like English, Arabic, French, etc...) by writing a story with Claude. Feedback on vocabulary and grammar will be provided, and new words will be logged for export into online flashcard services like Anki and Quizlet. 

# Stages:
#   (1) Console App
#   (2) Streamlit Deployment
#   (3) Stateful API & Frontend *
#   (4) Stateless API w/ Database

# Add part of speech tagging AND add Anki flashcard import

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

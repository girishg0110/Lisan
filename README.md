# Lisan

Lisan (pron. lee-saan) uses collaborative storytelling to fill the market gap in intermediate-level language learning services. Users will develop professional competency in an international language (like English, French, Spanish, etc...) by writing a story with Lisan. 

* 🧠 Receive immediate feedback on your sentences. 
* 👩‍🏫 Tailor Lisan to match your CEFR language level.
* 🎤 Hear Lisan speak in your language. 
* ⛏️ Get a word-level breakdown of all sentences in the story. 
* 📂 Export flashcards for use on platforms like Anki and Quizlet.
* 📈 View analytics on a personalized dashboard. 

## Getting Started
All necessary Python packages are included in the requirements.txt file. Execute
```
python -m pip install -r requirements.txt
```
to install all Python dependences.

Lisan needs additional data downloaded through NLTK, the natural language toolkit. Open a Python client in the command line and execute
```python
>> import nltk
>> nltk.download('punkt')
>> nltk.download('averaged_perceptron_tagger')
```

On Ubuntu, install ffmpeg and espeak using the command
```
sudo apt install espeak ffmpeg
```

Create a .env file with a single line containing your Anthropic API key.
```
ANTHROPIC_API_KEY="ADD_YOUR_KEY_HERE"
```
It will be loaded as an environment variable.

Ready? Jump into a new language with Lisan!
```
streamlit run Home.py
```
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

from nltk.tokenize import word_tokenize, sent_tokenize
import re

def pos_tag_story(story):
    pos_tagged = []
    for sentence in sent_tokenize(story):
        simplified_sentence = re.sub(r'[?.;(),-]', '', sentence)
        simp_words = word_tokenize(simplified_sentence)
        pos_tagged.append(nltk.pos_tag(simp_words))
    return pos_tagged
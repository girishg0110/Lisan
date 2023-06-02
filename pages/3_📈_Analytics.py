import sys
sys.path.append('../utils')
from tokenizer_utils import pos_tag_story

import streamlit as st
from annotated_text import annotated_text
from pytrie import SortedStringTrie as Trie
from streamlit_agraph import agraph, Node, Edge, Config

storywriter = st.session_state.storywriter
# Show tagged POS for full story
st.subheader("Part of Speech Tagging")
postagged_story = pos_tag_story(storywriter.story_history)
for i, dialogue in enumerate(postagged_story):
    formatted_dialogue = [("User: " if i % 2 == 0 else "Lisan: "), *dialogue, '.']
    annotated_text(formatted_dialogue)

# Show summary of story
st.subheader("Summary")
with st.spinner(text="Lisan is summarizing..."):
    summary = storywriter.summarize()
st.write(summary)

# Show trie of words
st.subheader("Vocabulary Trie")

def make_trie(words):
    trie = Trie({word : i for i, word in enumerate(words)})
    visited = dict()
    root = Node(id="root", label="*")
    visited['root'] = True
    nodes = [root]
    edges = []
    for key in trie.iterkeys():
        prev = None
        curr = None
        for prefix in trie.iter_prefixes(key):
            prev = curr
            curr = prefix
            # check if prev, curr are in nodes; add prev->curr to edges
            if prev not in visited:
                nodes.append(Node(id=prev, label=prev, size=50, color='white'))
                visited[prev] = True
            if curr not in visited:
                nodes.append(Node(id=curr, label=curr, size=50, color='white'))
                visited[curr] = True
            edges.append(Edge(source=prev, label='prefixes', target=curr))
    return nodes, edges      
      
unique_words = set(storywriter.story_history.lower().split())
trie_nodes, trie_edges = make_trie(unique_words)
config = Config(width=750,
                height=950,
                directed=True, 
                physics=True, 
                hierarchical=True,
                # **kwargs
                )
return_value = agraph(nodes=trie_nodes, 
                      edges=trie_edges, 
                      config=config)

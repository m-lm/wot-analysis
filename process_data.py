import os
import spacy
import pandas as pd
import networkx as nx
import pyvis
import itertools
from collections import Counter

def locate_names(sentence: list, characters: pd.DataFrame) -> list:
    # Function that returns names found in sentence and converts to full name
    names = []
    for token in sentence: 
        if token.text in list(characters["First"]) or token.text in list(characters["Last"]):
            names.append(token.text) 
    for i in range(len(names)):
        for full_name in list(characters["Name"]):
            if names[i] in full_name:
                # Want to convert each First or Last token to full Name token for uniformity
                # Could probably be more efficient using a Pandas method
                # !Also some characters have same last names, be careful
                names[i] = full_name
    return names

# Some important characters are called/known by multiple aliases
# Some like kings, Amyrlins, Nae'blis change with time
# Some are necessary because of transformations, but others may be omitted because familiar usage implies closeness or importance
aliases = {
    "Rand al'Thor" : ["Lews Therin Telamon", "Dragon Reborn", "Car'a'carn"],
    "Ishamael" : ["Elan Morin Tedronai", "Moridin", "Ba'alzamon"],
    "Dark One" : ["Shai'tan", "Father of Lies", "Sightblinder", "Lord of the Grave", "Great Lord"],
    "Aginor" : ["Osan'gar"],
    "Lanfear" : ["Cyndane"],
    "Mazrim Taim" : ["M'Hael"],
    "Balthamel" : ["Aran'gar", "Halima", "Corlan Dashiva"],
    "Asmodean" : ["Jasin Natael"],
    "Zarine Bashere" : ["Faile"],
    "Galad Damodred" : ["Galad"],
    "Someshta" : ["The Green Man"]
}

# Convert scraped text file to dataframe
df = pd.read_csv("final_names.txt", header=None)
df.columns = ["Name"]

# Split names into first and last
df[["First", "Last"]] = df["Name"].str.split(" ", n=1, expand=True)

# Read actual book text
with open("data/01eyeoftheworld.txt", "r", encoding="utf-8") as f:
    content = f.read()[:100000]

# Format for parsing
nlp = spacy.load("en_core_web_sm")
doc = nlp(content)

# for ego graph use weights, sentence differences
associations = []
for sentence in doc.sents:
    ppl = locate_names(sentence, df)
    if len(ppl) > 0:
        # ppl is a list, but cast to list again due to how list addition works
        associations += [ppl]

# Each list in the list is for one sentence
# Names within the same list have some association
edges = []
for i in range(len(associations)):
    e = list(itertools.combinations(associations[i], 2))
    if len(e) > 0:
        edges += e

# Relationship graph will be undirected and have no loops
# Get rid of loops
edges = [e for e in edges if e[0] != e[1]]
degrees = Counter(edges)
print(degrees)
'''
edges = set(edges)
'''

# Construct graph from edge list, and visualize
G = nx.Graph(edges)
nt = pyvis.network.Network(
    height = "800px", 
    width = "100%",
    bgcolor="#222222",
    font_color="white",
    select_menu=True, 
    notebook=True,
    cdn_resources="remote")
nt.barnes_hut()
nt.repulsion()
nt.from_nx(G)
nt.show("viz/graph.html")



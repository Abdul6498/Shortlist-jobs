import numpy as np
from text_from_html import text_from_url
from translate_en import translate_to_eng
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from text_from_pdf import text_from_pdf
PATH = "/home/abdul/Desktop/Job Application/Running/Bosch_C++ Tool Engineer for AI_20221018/Abdul_Rehman_CV.pdf"

def vectorize(tokens):
    ''' This function takes list of words in a sentence as input 
    and returns a vector of size of filtered_vocab.It puts 0 if the 
    word is not present in tokens and count of token if present.'''
    vector=[]
    for w in filtered_vocab:
        vector.append(tokens.count(w))
    return vector
def unique(sequence):
    '''This functions returns a list in which the order remains 
    same and no item repeats.Using the set() function does not 
    preserve the original ordering,so i didnt use that instead'''
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]
#create a list of stopwords.You can import stopwords from nltk too
stopwords=["to","is","a"]
#list of special characters.You can use regular expressions too
special_char=[",",":"," ",";",".","?", "/", "for", "in", "the", "and", "of", "with", "all", "will", "be", "as", "by", "on"]

url = 'https://www.bosch.de/en/career/job/REF122833O-c-tool-engineer-for-ai-w-m-div/'
#url = 'https://www.stepstone.de/jobs--Software-Developer-C-for-Situation-Understanding-in-Automated-Driving-w-m-div-Stuttgart-Bosch-Gruppe--8297189-inline.html'
text = text_from_url(url)
string1 = str(translate_to_eng(text).text)
    #print(eng.text)
string2 = str(text_from_pdf(PATH))
string1 = string1.replace(",", "")
string2 = string2.replace(",", "")
string1 = string1.replace("/", "")
string2 = string2.replace("/", "")

#convert them to lower case
string1=string1.lower()
string2=string2.lower()
#split the sentences into tokens
tokens1=string1.split()
tokens2=string2.split()
#print(tokens1)
#print(tokens2)
#create a vocabulary list
vocab=unique(tokens1+tokens2)
#print(vocab)
#filter the vocabulary list
filtered_vocab=[]
for w in vocab: 
    if w not in stopwords and w not in special_char: 
        filtered_vocab.append(w)
#print(filtered_vocab)
#convert sentences into vectords
vector1=vectorize(tokens1)
#print(vector1)
vector2=vectorize(tokens2)
#print(vector2)
lang = ["c++", "python", "capl"]
match = np.where((np.array(vector1)>0) & (np.array(vector2)>0), "green", "red")
matching_words = []
for i in range(len(match)):
    if match[i] == "green":
        #print(filtered_vocab[i])
        matching_words.append(filtered_vocab[i])
        if filtered_vocab[i] == "stuttgart":
            print("City = Stuttgart")
        if any(x in filtered_vocab[i] for x in lang):
            contained = [x for x in lang if x in filtered_vocab[i]]
            print(contained)
#print(matching_words)
pd.DataFrame(matching_words).to_csv("data.csv")
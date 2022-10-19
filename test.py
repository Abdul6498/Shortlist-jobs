import glob
import numpy as np
from text_from_html import text_from_url
from translate_en import translate_to_eng
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from text_from_pdf import text_from_pdf
PATH = "/home/abdul/Desktop/Job Application/module/"

def vectorize(tokens, filtered_vocab):
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
stopwords=["to","is","a", "for", "in", "the", "and", "of", "with", "all", "will", "be", "as", "by", "on"]
#list of special characters.You can use regular expressions too
special_char=[",",":"," ",";",".","?", "/"]

url = 'https://www.stepstone.de/jobs--Senior-Software-Engineer-for-Middleware-C-Driver-Assistance-Systems-f-m-div-Berlin-Bosch-Gruppe--8741267-inline.html'
linkedin_url = 'https://www.linkedin.com/in/abdulrehman6498/details/'
linkedin_data = ['projects/', 'experience/', 'skills/', 'honors/']
def extract_data_from_linkedin(url, types):
    text = ""
    for ext in types:
        final_url = url + ext
        print(final_url)
        text += str(text_from_url(final_url))
    return text

def main(path, url, linkedin_url, linkedin_data):
    files = sorted(glob.glob(path+"*.pdf"))
    personal_dox = ""
    for file in files:
        personal_dox += str(text_from_pdf(file)) + " "
    #personal_dox += extract_data_from_linkedin(linkedin_url,linkedin_data)    
    #print(personal_dox)
    text = text_from_url(url)
    job_desc = str(translate_to_eng(text).text)
        #print(eng.text)
    
    job_desc = job_desc.replace(",", "")
    personal_dox = personal_dox.replace(",", "")
    job_desc = job_desc.replace("/", "")
    personal_dox = personal_dox.replace("/", "")

    #convert them to lower case
    job_desc=job_desc.lower()
    personal_dox=personal_dox.lower()

    #split the sentences into tokens
    tokens1=job_desc.split()
    tokens2=personal_dox.split()

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
    vector1=vectorize(tokens1, filtered_vocab)
    #print(vector1)
    vector2=vectorize(tokens2, filtered_vocab)
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

if __name__ == '__main__':
    main(PATH, url, linkedin_url, linkedin_data)
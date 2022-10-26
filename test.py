import glob
import string
import numpy as np
from text_from_html import text_from_url
from translate_en import translate_to_eng
import pandas as pd
from text_from_pdf import text_from_pdf
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from wordcloud import WordCloud
#nltk.download()

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


linkedin_url = 'https://www.stepstone.de/jobs--Computer-Vision-Expert-f-m-div-Stuttgart-Bosch-Gruppe--7970290-inline.html'
linkedin_data = ['projects/', 'experience/', 'skills/', 'honors/']

def extract_data_from_linkedin(url, types):
    text = ""
    for ext in types:
        final_url = url + ext

        text += str(text_from_url(final_url))
    return text

def main(path, url, linkedin_url, linkedin_data):
    '''This function takes in a path and a url and returns a list of 
    words in a sentence'''

    #create a list of stopwords.You can import stopwords from nltk too
    #stopwords=["to","is","a", "for", "in", "the", "and", "of", "with", "all", "will", "be", "as", "by", "on"]
    stop_words = stopwords.words('english')
    #list of special characters.You can use regular expressions too
    special_char=[",",":"," ",";",".","?", "/", ")", "(", "-", "{", "_", "}", "&", "!", "),"]

    files = sorted(glob.glob(path+"*.pdf"))
    personal_dox = ""
    for file in files:
        personal_dox += str(text_from_pdf(file)) + "master's" + "master" +" "

    text = text_from_url(url)
    job_desc = str(translate_to_eng(text).text)
    for sp_char in special_char:
        job_desc = job_desc.replace(sp_char, " ")
        personal_dox = personal_dox.replace(sp_char, " ")
    job_desc=job_desc.lower()
    personal_dox=personal_dox.lower()

    tokens1=job_desc.split()
    tokens2=personal_dox.split()
    vocab=unique(tokens1+tokens2)
    filtered_vocab=[]

    for w in vocab: 
        if w not in stop_words and w not in special_char: 
            filtered_vocab.append(w)

    vector1=vectorize(tokens1, filtered_vocab)
    vector2=vectorize(tokens2, filtered_vocab)

    lang = ["c++", "python", "capl", "matlab", "linux", "qt", "ros", "simulink", "deep", "git", "camera", "sensor", "ai"]

    match = np.where((np.array(vector1)>0) & (np.array(vector2)>0), "green", "red")

    matching_words = []
    high_scoring_words = []
    for i in range(len(match)):
        if match[i] == "green":
            matching_words.append(filtered_vocab[i])
            if filtered_vocab[i] == "stuttgart":
                print("City = Stuttgart")
            if any(x in filtered_vocab[i] for x in lang):
                contained = [x for x in lang if x in filtered_vocab[i]]
                high_scoring_words.append(contained[0])
                print(contained[0])
    #print(matching_words)
    pd.DataFrame(matching_words).to_csv("data.csv")
    return matching_words, high_scoring_words

if __name__ == '__main__':
    url = 'https://www.bosch.de/en/career/job/REF124429H-'

    matching_words, high_scorings = main(PATH, url, linkedin_url, linkedin_data)
    high_scorings = unique(high_scorings)
    print(high_scorings)
    print(len(matching_words))
    cv_words = 550
    num_skills = 20
    high_scorings_factor = ((cv_words - len(matching_words))/num_skills)
    print(high_scorings_factor)
    prob_high = ((len(high_scorings)*high_scorings_factor)/cv_words)*100
    prob_match = (len(matching_words)/cv_words)*100
    prob = ((len(matching_words) + len(high_scorings)*high_scorings_factor)/cv_words) *100
    print("Probability of matching_words: ", prob)

    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = 'keywords', 'skills', 'chances', 'needs improvement'
    sizes = [prob_match, prob_high, prob, 100-prob_match-prob_high-prob]
    explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots(1)
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    fig1.show()

    cloud_words = " "
    for text in matching_words:
        if text in high_scorings:
            text = text +" "+ text + " " + text
        cloud_words = cloud_words + text + " "
    normal_word = r"(?:\w[\w']+)"
    # 2+ consecutive punctuations, e.x. :)
    ascii_art = r"(?:[{punctuation}][{punctuation}]+)".format(punctuation=string.punctuation)
    # a single character that is not alpha_numeric or other ascii printable
    emoji = r"(?:[^\s])(?<![\w{ascii_printable}])".format(ascii_printable=string.printable)
    regexp = r"{normal_word}|{ascii_art}|{emoji}".format(normal_word=normal_word, ascii_art=ascii_art,
                                                     emoji=emoji)
    word_cloud = WordCloud(collocations = False, regexp=r'[a-zA-z\+]+', width=1080, height=920, relative_scaling=1.0, background_color = 'white').generate(cloud_words)
    
    #word_cloud.generate("c ++")
    # Display the generated Word Cloud
    word_fig = plt.figure(2)
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    

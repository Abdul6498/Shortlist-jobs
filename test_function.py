
from text_from_html import text_from_url
from translate_en import translate_to_eng
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from text_from_pdf import text_from_pdf
import numpy as np

PATH = "/home/abdul/Desktop/Job Application/Running/Bosch_C++ Tool Engineer for AI_20221018/Abdul_Rehman_CV.pdf"

def main():
    """
    Main function.
    """
    url = 'https://www.stepstone.de/jobs--C-Tool-Engineer-for-AI-w-m-div-Stuttgart-Bosch-Gruppe--7604185-inline.html'
    text = text_from_url(url)
    text_job = translate_to_eng(text).text
    #print(eng.text)
    text_pdf = str(text_from_pdf(PATH))
    #print(text_pdf)
    CountVec = CountVectorizer(ngram_range=(1,1), # to use bigrams ngram_range=(2,2)
                             stop_words='english')
    Count_data = CountVec.fit_transform([text_pdf,text_job])
    cv_dataframe=pd.DataFrame(Count_data.toarray(),columns=CountVec.get_feature_names())
    df = cv_dataframe.T
    #df.where(df.iloc[0])
    # df.where(df.iloc[0]>1, 99)
    # print(df.iloc[0])
    # resume = df.iloc[0]
    # job_description = df.iloc[1]
    # new_df = np.where(resume>0 & job_description>0, 99)
    # df = df[(df > 0).all(axis=1)]
    df.rename(columns = {0:'resume', 1:'job'}, inplace = True)
    df.to_csv("data.csv", sep='\t')
    df['color'] = np.where((df.resume > 0), "green", "red")
    df.sort_values(by = "color", ascending=True)
    print(df)
    


if __name__ == '__main__':
    main()
    # sentence_1="This is a good job.I will not miss it for anything"
    # sentence_2="This is not good at all"
    
    
    
    # CountVec = CountVectorizer(ngram_range=(1,1), # to use bigrams ngram_range=(2,2)
    #                         stop_words='english')
    # #transform
    # Count_data = CountVec.fit_transform([sentence_1,sentence_2])
    
    # #create dataframe
    # cv_dataframe=pd.DataFrame(Count_data.toarray(),columns=CountVec.get_feature_names())
    # print(cv_dataframe)


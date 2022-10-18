import glob
import fitz # install using: pip install PyMuPDF

# print("Hello test")
# PATH = "/home/abdul/Desktop/Job Application/Running/Bosch_C++ Tool Engineer for AI_20221018/"

# files = sorted(glob.glob(PATH+"*.pdf"))
# for file in files:
#     with fitz.open(file) as doc:
#         text = ""
#         for page in doc:
#             text += page.get_text()

#     print(text)

#     break
def text_from_pdf(path):
    with fitz.open(path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text
#print(text_from_pdf("/home/abdul/Desktop/Job Application/Running/Bosch_C++ Tool Engineer for AI_20221018/Abdul_Rehman_CV.pdf"))
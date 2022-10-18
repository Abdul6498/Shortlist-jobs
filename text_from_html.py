from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from googletrans import Translator

#url = 'https://www.stepstone.de/jobs--C-Tool-Engineer-for-AI-w-m-div-Stuttgart-Bosch-Gruppe--7604185-inline.html'

def text_from_url(url):
    req = Request(
        url=url, 
        headers={'User-Agent': 'Mozilla/71.0'}
    )

    html = urlopen(req).read()

    soup = BeautifulSoup(html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style", "header", "meta", "head", "input", "footer", "noscript"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    lines = (line.strip() for line in text.splitlines())

    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    #print(text[0:10])

    #translation = translate_to_eng(str(text))

    # print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")
    #print(translation.text)

    return text



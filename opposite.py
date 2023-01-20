import requests
from bs4 import BeautifulSoup
def get_op(word):
    if(word.find(" ")!=-1):
        word = word.replace(" ","-")
    link = f"https://abadis.ir/fatofa/" + word + "/"
    response = requests.get(link)
    soup = BeautifulSoup(response.text)
    syns = soup.find ("div", {"class": "lun boxBd boxMain"})

    syn_list = syns.find_next_siblings("br")
    synonyms = [elm.text for elm in syn_list]

    for br in syns.find_all("br"):
        br.replace_with("، ")

    for br in syns.find_all(": "):
        br.replace_with("، ")

    parsedText = syns.get_text()

    parsedText = parsedText.replace(": ","، ")
    parsedText = parsedText.replace(word,"")

    words=[]
    for elm in [parsedText.strip()]:
        words = words + elm.split("، ")


    words = words[words.index('متضاد ')+1:words.index('برابر پارسی')]
    return words
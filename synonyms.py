import requests
from bs4 import BeautifulSoup

def get_syn(word):
    if(word.find(" ")!=-1):
        word = word.replace(" ","-")
    link = f"https://abadis.ir/fatofa/" + word + "/"
    response = requests.get(link)
    soup = BeautifulSoup(response.text,features="lxml")
    syns = soup.find ("div",{"t":"مترادف ها"})
    words = []
    if(syns != None):
        syn_list = syns.find_all("div", {"class": None})
        synonyms = [elm.text for elm in syn_list]
        for elm in synonyms:
            words = words + elm.split("، ")
    return words
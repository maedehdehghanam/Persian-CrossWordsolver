import requests
from bs4 import BeautifulSoup
link = f"https://abadis.ir/fatofa/کهنه/"
response = requests.get(link)
soup = BeautifulSoup(response.text,features="lxml")
syns = soup.find("div", {"t": "مترادف ها"})
syn_list =  syns.find_all("div", {"class": None})
synonyms = [elem.text for elem in syn_list]
#synonyms = synonyms.remove("کهنه")

print(synonyms[0])
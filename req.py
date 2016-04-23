import requests
import sys
from bs4 import BeautifulSoup
def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)

#headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
payload = {'q':'laptop'}
r = requests.get('http://www.flipkart.com/search', params = payload)
#print(r.content)
data = r.content.decode(encoding='UTF-8')
f = open("flip.txt", "w+")
f.write(data)
soup = BeautifulSoup(r.content.decode(encoding='UTF-8'), "lxml")
#print(soup.prettify())
coll = soup.find_all("div", {"class": "product-unit unit-4 browse-product new-design "})
#uprint(coll)
href = []
for c in coll:
    a = c.find("a")
    print(a['href'])
    href.append(a['href'])
'''for c in coll:
    if("product-unit" in c):
        coll.indexof(c)
uprint(coll)'''
rev = []
for link in href:
    r = requests.get('http://www.flipkart.com'+link)
    content = r.content.decode(encoding='UTF-8')
    soup = BeautifulSoup(r.content.decode(encoding='UTF-8'), "lxml")
    reviews = soup.find_all('div', {"class": "review bigReview"})
    for review in reviews:
        p = review.find_all("p")
        for s in p:
            rev.append(s.text)
        sp = review.find_all("span")
        for s in sp:
            rev.append(s.text)
f = open("div.txt", "w+")
f.write(str(rev))

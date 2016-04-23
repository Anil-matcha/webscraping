import requests
import sys
from bs4 import BeautifulSoup
import time
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
data = r.content.decode(encoding='UTF-8')
f = open("flipkartdata.txt", "w+")
f.write(data)
soup = BeautifulSoup(r.content.decode(encoding='UTF-8'), "lxml")
collection = soup.find_all("div", {"class": "product-unit unit-4 browse-product new-design "})
href = []
for c in collection:
    a = c.find("a")
    href.append(a['href'])
reviewarray = []
paraarray = []
linkarray = []
titles = []
for link in href:
    r = requests.get('http://www.flipkart.com'+link)
    content = r.content.decode(encoding='UTF-8')
    soup = BeautifulSoup(r.content.decode(encoding='UTF-8'), "lxml")
    reviews = soup.find_all('div', {"class": "review bigReview"})
    title = soup.find_all('h1', {"class":"title"})
    for review in reviews:
        p = review.find_all("p")
        for s in p:
            reviewarray.append(s.text+"\n")
        sp = review.find_all("span", {"class" : "review-text-full"})
        if(len(sp)==0):
            sp = review.find_all("span", {"class" : "review-text"})
        for s1 in sp:
            if(s1.text not in paraarray):
                paraarray.append(s1.text.strip())
                linkarray.append(link)
                if(len(title)==1):
                    titles.append(title[0].text)
                else:
                    titles.append("Deafult")
    time.sleep(1)
f = open("reviews.txt", "w+")
f.write(str(reviewarray))
f = open("paraarray.txt", "w+")
prevlink = ""
for i in range(len(linkarray)):
    if(linkarray[i]!=prevlink): 
        f.write('http://www.flipkart.com'+linkarray[i]+"\n")
        f.write(titles[i]+"\n")
        f.write(paraarray[i]+"\n")
        prevlink = linkarray[i]
    else:
        f.write(paraarray[i]+"\n")
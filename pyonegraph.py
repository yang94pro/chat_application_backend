from bs4 import BeautifulSoup
from requests import get, Session

import lxml
s = Session()
headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '\
                         'AppleWebKit/537.36 (KHTML, like Gecko) '\
                         'Chrome/75.0.3770.80 Safari/537.36'}
s.headers.update(headers)


def linkpreview(weblink):
    try: html = s.get(weblink)
    except: html = s.get("http://"+weblink)

    soup = BeautifulSoup(html.content, 'lxml')


    for m in soup.find_all("meta"):
        if (m.get("property", None) == "og:title"):
            otitle = (m.get("content", None)) or "None"
        elif m.get("property", None) == "og:url":
            ourl = (m.get("content", None))
        elif m.get("property", None) == "og:description":
            odescription = (m.get("content", None))
        elif m.get("property", None) == "og:image":
            oimage = (m.get("content", None))
        elif m.get("property", None) == "og:type":
            oogtype = (m.get("content", None))


    try: g={
        "title": otitle,
        "url": ourl,
        "description": odescription,
        "image": oimage,
        "ogtype": oogtype}
    except:
        g = None

    return g
        

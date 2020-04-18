import requests
import sqlite3
from bs4 import BeautifulSoup

conn = sqlite3.connect('residents.db')
c = conn.cursor()

links = []
page = 0
while 1:
    url = 'https://www.la-spa.fr/adopter-animaux?field_refuge_animal_target_id=129&page='+str(page)

    res = requests.get(url)

    if res.ok:
        soup = BeautifulSoup(res.text,'html.parser')
        divs = soup.find_all("div", {"class": "block-result-search-top"})

        if not divs:
            break

        for div in divs:
            links.append(div.a['href'])


        page += 1

for link in links:
    url = link
    res = requests.get(url)

    #CHECK IF LINK ALREADY EXISTS
    c.execute("SELECT link from residents where link =?;", (link,))
    conn.commit()
    foundlink = c.fetchone()
    
    if res.ok and not foundlink:
        soup = BeautifulSoup(res.text,'html.parser')
        
        #PHOTOS
        divs = soup.find_all("div", {"class": "field-collection-container clearfix"})

        for div in divs:
            imgs = div.find_all("img", {"typeof": "foaf:Image"})
            for img in imgs:
                c.execute("INSERT INTO photos VALUES(?, ?);", (url, img['src']))
                conn.commit()

        #DESCRIPTION
        description = soup.find("div", {"class": "field-type-text-with-summary"})

        if description.has_attr('p'):
            description = description.p.contents[0]
        else:
            description = ""

        #LINK
        print(url)
        c.execute("INSERT INTO residents VALUES(?, ?);", (url, description))
        conn.commit()
conn.close()
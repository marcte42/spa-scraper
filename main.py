import requests
import sqlite3
from bs4 import BeautifulSoup

conn = sqlite3.connect('residents.db')
c = conn.cursor()

links = []
page = 0
while 1:
    url = 'https://www.la-spa.fr/adopter-animaux?field_refuge_animal_target_id=118&page='+str(page)

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

    c.execute("SELECT link from residents where link = ?;", (link)))
    conn.commit()
    c.fetchone
    # ADD AND IF URL NOT EXISTS IN DB
    if res.ok and foundlink:
        soup = BeautifulSoup(res.text,'html.parser')
        
        #PHOTOS
        divs = soup.find_all("div", {"class": "field-collection-container clearfix"})

        for div in divs:
            imgs = div.find_all("img", {"typeof": "foaf:Image"})
            for img in imgs:
                print(img['src'])
                c.execute("INSERT INTO photos VALUES(?, ?);", (url, img['src']))
                conn.commit()

        #DESCRIPTION
        description = soup.find("div", {"class": "field-type-text-with-summary"})
        print(description.p.contents[0])

        #LINK
        print(url)
        c.execute("INSERT INTO residents VALUES(?, ?);", (url, description.p.contents[0]))
        conn.commit()
conn.close()
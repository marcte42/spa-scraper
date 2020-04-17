import requests
from bs4 import BeautifulSoup

links = []
page = 0

while 1:
    url = 'https://www.la-spa.fr/adopter-animaux?field_esp_ce_value=All&_field_localisation=refuge&field_refuge_animal_target_id=118&field_departement_refuge_tid=All&field_sexe_value=All&field_taille_value=All&title_1=&field_sauvetage_value=All&_field_age_value=&_field_adresse=&page='+str(page)

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

    if res.ok:
        soup = BeautifulSoup(res.text,'html.parser')
        
        #PHOTOS
        divs = soup.find_all("div", {"class": "field-collection-container clearfix"})

        for div in divs:
            imgs = div.find_all("img", {"typeof": "foaf:Image"})
            for img in imgs:
                print(img['src'])

        #DESCRIPTION
        description = soup.find("div", {"class": "field-type-text-with-summary"})
        print(description.p.contents[0])

        #LINK
        print(url)
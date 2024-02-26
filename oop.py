from requests_html import HTMLSession
from bs4 import BeautifulSoup

import json,pandas


class Scraper:
    def __init__(self):
        self.session = HTMLSession()

    def details(self,url):
        item = {
            "title":"",
            "price":"",
            "rating":"",
            "availability":"",
            "style":"",
            "volume":"",
            "abv":"",
            "malt":"",
            "origin":"",
            "brewer":"",
            "allergens":""
        }

        send_requests = self.session.get(url)
        html = send_requests.html.html

        soup = BeautifulSoup(html,"html.parser")
        item["title"] = soup.find("span","bw-text-h2 bw-mb-3").text.strip()

        table = soup.find_all("td")
        item["style"] = table[1].text.strip()
        item["volume"] = table[3].text.strip()
        item["abv"] = table[5].text.strip()
        item["malt"] = table[7].text.strip()
        item["origin"] = table[9].text.strip()
        item["brewer"] = table[11].text.strip()
        item["allergens"] = table[13].text.strip()
        
        script = soup.find("script",{"type":"application/ld+json"}).text.strip()
        script = json.loads(script)
        item["price"] = script["offers"]["price"]
        item["availability"] = script["offers"]["availability"]
        item["rating"] = script["aggregateRating"]["ratingValue"]
        
        return item

    def extract_links():
        pass


if __name__=="__main__":
    url = "https://www.beerwulf.com/en-gb/p/beers/affligem-blond-8l-keg-bladekeg-8"
    beer = Scraper()
    item = beer.details(url)
    print(item)
    print(type(item))


    
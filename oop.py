from requests_html import HTMLSession
from bs4 import BeautifulSoup

import json,pandas,re


class Scraper:
    def __init__(self):
        self.session = HTMLSession()

    def get_html(self,url):
        send_requests = self.session.get(url)
        print(f"Get {url}")
        html = send_requests.html.html
        return html

    def details(self,html):
        item = {
            "ProductUrl":url,
            "Title":"",
            "Price":"",
            "PriceCurrency":"",
            "Rating":"",
            "ReviewCount":"",
            "Availability":"",
            "Style":"",
            "Volume":"",
            "ABV":"",
            "Malt":"",
            "Origin":"",
            "Brewer":"",
            
        }

        soup = BeautifulSoup(html,"html.parser")
        item["Title"] = soup.find("span","bw-text-h2 bw-mb-3").text.strip()

        table = soup.find_all("td")
        for i in range(0,len(table),2):
            key = table[i].text.strip()
            if key == "Brewer" or key == "Allergens" or key == "Hops":
                val = table[i+1].text.split()
            else:
                val = table[i+1].text.replace("\n","").replace("\r","").strip()
            item[key] = val
            i = i+2
        
        script = soup.find("script",{"type":"application/ld+json"}).text.strip()
        script = json.loads(script)
        item["Price"] = script["offers"]["price"]
        item["Rating"] = script["aggregateRating"]["ratingValue"]
        availability = script["offers"]["availability"]
        if availability == "http://schema.org/InStock":
            item["Availability"] = "In Stock"
        else:
            item["Availability"] = "Out of Stock"
        
        return item

    def extract_links(self,url):
        send_requests = self.session.get(url)
        send_requests.html.render(sleep=1,scrolldown=15)
        html = send_requests.html.html
        soup = BeautifulSoup(html,"html.parser")

        links = soup.find_all("a",class_=re.compile("product search-product product-info-container bw-plp-product-card"))
        all_links = [f'https://www.beerwulf.com{link["href"]}' for link in links if "beercases" not in link["href"]]
        print(f"Get {len(all_links)} of items")

        return all_links
    
    def save(self,data,filename):
        df = pandas.DataFrame(data)
        df.to_excel(filename,index=False)
        print("Saved!")


if __name__=="__main__":
    # url = "https://www.beerwulf.com/en-gb/c/beer-kegs"
    # beer = Scraper()
    # links = beer.extract_links(url)
    # items = [beer.details(item) for item in links]    
    
    # beer.save(items,"oop_output.xlsx")

    url = "https://www.beerwulf.com/en-gb/p/beers/affligem-blond-2l-keg"
    beer = Scraper()
    html = beer.get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    taste_tables = soup.find("div","taste-tables")
    div = taste_tables.find_all("div")
    print(len(div))
    i = 0
    while i in range(len(div)):
        print(i)       
        name = div[i].section.span.text.strip()
        value = div[i].section.div["title"]
        print(name)
        print(value)
        i = i+3
        if i > 15:
            break

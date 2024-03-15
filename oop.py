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
    
    def parse_script(self,html):
        soup = BeautifulSoup(html,"html.parser")
        script = soup.find("script",{"type":"application/ld+json"}).text.strip()
        script = json.loads(script)
        name = script["name"]
        image = script["image"]
        rating = script["aggregateRating"]["ratingValue"]
        review = script["aggregateRating"]["reviewCount"]
        price = script["offers"]["price"]
        currency = script["offers"]["priceCurrency"]
        availability = script["offers"]["availability"]
        if availability == "http://schema.org/InStock":
            availability = "In Stock"
        else:
            availability = "Out of Stock"
        product_details = {
            "ProductName":name,
            "Image":image,
            "Rating":rating,
            "ReviewCount":review,
            "Price":price,
            "PriceCurrency":currency,
            "Availability":availability
        }
        return product_details
    
    def parse_table_details(self,html):
        table_details = dict()
        soup = BeautifulSoup(html,"html.parser")
        table = soup.find_all("td")
        for i in range(0,len(table),2):
            key = table[i].text.strip()
            if key == "Allergens" or key == "Hops" or key == "NutritionalValues":
                pass
            else:
                val = table[i+1].text.replace("\n","").replace("\r","").strip()
                table_details[key] = val
            i = i+2
        return table_details
    
    def parse_taste_tables(self,html):
        taste_tables = dict()
        soup = BeautifulSoup(html,"html.parser")
        taste_tables_html = soup.find("div","taste-tables")
        div = taste_tables_html.find_all("div")
        i = 0
        while i in range(len(div)):   
            name = div[i].section.span.text.strip()
            value = div[i].section.div["title"]
            taste_tables[name]=value
            i = i+3
            if i > 15:
                break
        return taste_tables

    def details(self,html):
        pass

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
    data1 = beer.parse_script(html)
    data2 = beer.parse_table_details(html)
    data3 = beer.parse_taste_tables(html)
    print(data1)
    print(data2)
    print(data3)

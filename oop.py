from requests_html import HTMLSession
from bs4 import BeautifulSoup

import json,pandas,re, concurrent.futures


class Scraper:
    def __init__(self):
        self.session = HTMLSession()

    def get_html(self,url):
        send_requests = self.session.get(url)
        print(f"Get {url}")
        html = send_requests.html.html
        return html
    
    def extract_links(self,url):
        send_requests = self.session.get(url)
        send_requests.html.render(sleep=1,scrolldown=15)
        html = send_requests.html.html
        soup = BeautifulSoup(html,"html.parser")

        links = soup.find_all("a",class_=re.compile("product search-product product-info-container bw-plp-product-card"))
        all_links = [f'https://www.beerwulf.com{link["href"]}' for link in links if "beercases" not in link["href"]]
        print(f"Get {len(all_links)} of links")

        return all_links

class Parser:
    def __init__(self,html):
        soup = BeautifulSoup(html,"html.parser")
        self.soup = soup
    
    def parse_script(self):
        script = self.soup.find("script",{"type":"application/ld+json"}).text.strip()
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
    
    def parse_table_details(self):
        table_details = dict()
        table = self.soup.find_all("td")
        for i in range(0,len(table),2):
            key = table[i].text.strip()
            if key == "Allergens" or key == "Hops" or key == "NutritionalValues":
                pass
            else:
                val = table[i+1].text.replace("\n","").replace("\r","").strip()
                table_details[key] = val
            i = i+2
        return table_details
    
    def parse_taste_tables(self):
        taste_tables = dict()
        try:
            taste_tables_html = self.soup.find("div","taste-tables")
            div = taste_tables_html.find_all("div")
            i = 0
            while i in range(len(div)):   
                name = div[i].section.span.text.strip()
                value = div[i].section.div["title"]
                taste_tables[name]=value
                i = i+3
                if i > 15:
                    break
        except AttributeError:
            pass

        return taste_tables

    def details(self):
        product_details = self.parse_script()
        table_details = self.parse_table_details()
        taste_tables = self.parse_taste_tables()
        details = {**product_details,**table_details,**taste_tables}
        return details
    
def save_to_excel(data,filename="beer_product.xlsx"):
    df = pandas.DataFrame(data)
    df.to_excel(filename,index=False)
    print(f"{filename} Saved!")

def main(url):
    result = []
    beer = Scraper()
    links = beer.extract_links(url)
    for link in links:
        html = beer.get_html(link)
        data = Parser(html).details()
        data["ProductURL"] = link
        result.append(data)
    save_to_excel(result)
    

if __name__=="__main__":
    url = "https://www.beerwulf.com/en-gb/c/beer-kegs"
    main(url)

from requests_html import HTMLSession
from bs4 import BeautifulSoup #auto installed after install requests-html
import json #its default
import pandas as pd

def scrape_single_product(url):
    r = session.get(url)
    text = r.html.render(sleep=1)
    text = r.html.html
    soup = BeautifulSoup(text,"html.parser")
    #this script contain json data
    script = soup.find("script",{"type":"application/ld+json"}).text.strip()
    json_script = json.loads(script)
    name = json_script["name"]
    image = json_script["image"]
    desc = json_script["description"]
    rating = json_script["aggregateRating"]["ratingValue"]
    price = json_script["offers"]["price"]
    
    product_details = {"product name":name,
                   "rating":rating,
                   "price":price,
                   "description":desc,
                   "image":image,
                   "url":url}
    return product_details

if __name__ == "__main__":
    url = "https://www.beerwulf.com/en-gb/c/all-beers?segment=Beers&catalogCode=Beer_1"
    session = HTMLSession()
    #getting all url in a page
    r = session.get(url)
    r.html.render(sleep=1,scrolldown=15)
    #get all links, 83 links
    links = r.html.xpath('//*[@id="product-items-container"]', first = True).absolute_links
    #links = "https://www.beerwulf.com/en-gb/p/beers/newcastle-brown-ale-2l-keg"

    result_dict = []
    x= 1

    for link in links:
        product_data = scrape_single_product(link)
        print("Scrap link #",x,":",link)
        result_dict.append(product_data)
        x = x+1
    df = pd.DataFrame(result_dict)
    #return 82 data
    df.to_excel("beerwulf_result.xlsx", index=False)
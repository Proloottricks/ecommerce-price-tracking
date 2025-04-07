import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from database import store_price

def add_affiliate_tag(url, platform):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    if platform == "amazon":
        query["tag"] = ["yourtag-21"]
    elif platform == "flipkart":
        query["affid"] = ["yourtag"]
    elif platform == "ajio":
        query["affid"] = ["yourtag"]
    elif platform == "shopsy":
        query["affid"] = ["yourtag"]

    new_query = urlencode(query, doseq=True)
    updated_url = urlunparse(parsed._replace(query=new_query))
    return updated_url

def scrape_and_store_price(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    domain = urlparse(url).netloc

    platform = None
    if "amazon" in domain:
        platform = "amazon"
    elif "flipkart" in domain:
        platform = "flipkart"
    elif "ajio" in domain:
        platform = "ajio"
    elif "shopsy" in domain:
        platform = "shopsy"
    else:
        return "Unsupported platform"

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        if platform == "amazon":
            title = soup.find(id="productTitle")
            price = soup.find("span", {"class": "a-offscreen"})
        elif platform == "flipkart":
            title = soup.find("span", {"class": "B_NuCI"})
            price = soup.find("div", {"class": "_30jeq3 _16Jk6d"})
        elif platform == "ajio":
            title = soup.find("h1", {"class": "prod-name"})
            price = soup.find("div", {"class": "price  components-base-style__salePrice"})
        elif platform == "shopsy":
            title = soup.find("span", {"class": "B_NuCI"})
            price = soup.find("div", {"class": "_30jeq3 _16Jk6d"})
        else:
            return "Platform not supported"

        product_title = title.text.strip() if title else "Product Title not found"
        product_price = price.text.strip() if price else "Price not found"

        updated_url = add_affiliate_tag(url, platform)
        store_price(updated_url, product_price)

        return f"**{product_title}**\nPrice: {product_price}\n[Buy Now]({updated_url})"

    except Exception as e:
        return f"Error: {str(e)}"
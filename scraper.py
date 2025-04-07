import re
import requests
from bs4 import BeautifulSoup
from database import store_price
from utils import extract_price, add_affiliate_tag

def scrape_and_store_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
    except Exception as e:
        return f"Failed to fetch page: {e}"

    site = identify_site(url)

    if site == "amazon":
        title_tag = soup.find(id="productTitle")
        price_tag = soup.find("span", {"class": "a-price-whole"})
    elif site == "flipkart":
        title_tag = soup.find("span", {"class": "B_NuCI"})
        price_tag = soup.find("div", {"class": "_30jeq3 _16Jk6d"})
    elif site == "ajio":
        title_tag = soup.find("h1", {"class": "prod-name"})
        price_tag = soup.find("div", {"class": "prod-sp"})
    elif site == "shopsy":
        title_tag = soup.find("span", {"class": "B_NuCI"})
        price_tag = soup.find("div", {"class": "_30jeq3 _16Jk6d"})
    else:
        return "Site not supported"

    if not title_tag or not price_tag:
        return "Failed to extract product info"

    title = title_tag.get_text(strip=True)
    price = extract_price(price_tag.get_text())

    if not price:
        return "Price not found"

    affiliate_url = add_affiliate_tag(url, site)
    store_price(affiliate_url, title, price, site)

    return f"**{site.upper()}**\nTitle: {title}\nPrice: ₹{price}\n[View Product]({affiliate_url})"

def identify_site(url):
    if "amazon." in url:
        return "amazon"
    elif "flipkart.com" in url:
        return "flipkart"
    elif "ajio.com" in url:
        return "ajio"
    elif "shopsy.in" in url:
        return "shopsy"
    else:
        return "unknown"
import requests
from bs4 import BeautifulSoup
import re

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_price_data(url):
    try:
        domain = get_domain(url)
        if "amazon" in domain:
            return scrape_amazon(url)
        elif "flipkart" in domain or "shopsy" in domain:
            return scrape_flipkart(url)
        elif "ajio" in domain:
            return scrape_ajio(url)
        else:
            return None
    except Exception as e:
        return None

def get_domain(url):
    return re.findall(r'https?://(?:www\.)?([^/]+)', url)[0]

def clean_price(p):
    return int(re.sub(r"[^\d]", "", p.split()[0]))

def scrape_amazon(url):
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    title = soup.find(id="productTitle").get_text(strip=True)
    price_tag = soup.find("span", {"class": "a-price-whole"}) or soup.find("span", {"class": "a-offscreen"})
    img = soup.find("img", {"id": "landingImage"})["src"]

    return {
        "title": title,
        "price": clean_price(price_tag.text),
        "image": img
    }

def scrape_flipkart(url):
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    title = soup.find("span", {"class": "B_NuCI"}).get_text(strip=True)
    price = soup.find("div", {"class": "_30jeq3 _16Jk6d"}).text
    img = soup.find("img", {"class": "_396cs4 _2amPTt _3qGmMb"})["src"]

    return {
        "title": title,
        "price": clean_price(price),
        "image": img
    }

def scrape_ajio(url):
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    title = soup.find("h1", {"class": "prod-title"}).get_text(strip=True)
    price = soup.find("div", {"class": "price"}).find("span").get_text(strip=True)
    img = soup.find("img", {"class": "image-container"})["src"]

    return {
        "title": title,
        "price": clean_price(price),
        "image": img
    }
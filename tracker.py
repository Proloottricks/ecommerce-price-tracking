import requests
from bs4 import BeautifulSoup
import re

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
}


def get_price_details(url):
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        if "amazon" in url:
            title = soup.find(id="productTitle").get_text(strip=True)
            price = soup.find("span", {"class": "a-price-whole"}).get_text(strip=True).replace(",", "")
            image = soup.find("img", {"id": "landingImage"})["src"]

        elif "flipkart" in url:
            title = soup.find("span", {"class": "B_NuCI"}).get_text(strip=True)
            price = re.findall(r"₹[\d,]+", res.text)[0].replace("₹", "").replace(",", "")
            image = soup.find("img", {"class": "_396cs4 _2amPTt _3qGmMb"})["src"]

        elif "ajio" in url:
            title = soup.find("h1", {"class": "prod-title"}).get_text(strip=True)
            price = soup.find("div", {"class": "prod-sp"}).get_text(strip=True).replace("₹", "").replace(",", "")
            image = soup.find("img", {"class": "rilrtl-lazy-img"})["src"]

        elif "shopsy" in url:
            title = soup.find("span", {"class": "B_NuCI"}).get_text(strip=True)
            price = re.findall(r"₹[\d,]+", res.text)[0].replace("₹", "").replace(",", "")
            image = soup.find("img", {"class": "_396cs4 _2amPTt _3qGmMb"})["src"]

        else:
            return None

        return {"title": title, "price": price, "image": image}
    except:
        return None
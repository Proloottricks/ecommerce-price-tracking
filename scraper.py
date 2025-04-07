import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

def scrape_amazon(url):
    try:
        page = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(page.content, "html.parser")
        title = soup.select_one("#productTitle")
        price = soup.select_one(".a-price .a-offscreen")

        return {
            "title": title.get_text(strip=True) if title else "N/A",
            "price": price.get_text(strip=True) if price else "N/A"
        }
    except Exception as e:
        return {"error": str(e)}

def scrape_flipkart(url):
    try:
        page = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(page.content, "html.parser")
        title = soup.select_one("span.B_NuCI")
        price = soup.select_one("div._30jeq3")

        return {
            "title": title.get_text(strip=True) if title else "N/A",
            "price": price.get_text(strip=True) if price else "N/A"
        }
    except Exception as e:
        return {"error": str(e)}

def scrape_ajio(url):
    try:
        page = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(page.content, "html.parser")
        title = soup.select_one("h1.pdp-title")
        price = soup.select_one("div.product-price span.price")

        return {
            "title": title.get_text(strip=True) if title else "N/A",
            "price": price.get_text(strip=True) if price else "N/A"
        }
    except Exception as e:
        return {"error": str(e)}

def scrape_shopsy(url):
    try:
        page = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(page.content, "html.parser")
        title = soup.select_one("span.B_NuCI")
        price = soup.select_one("div._30jeq3")

        return {
            "title": title.get_text(strip=True) if title else "N/A",
            "price": price.get_text(strip=True) if price else "N/A"
        }
    except Exception as e:
        return {"error": str(e)}
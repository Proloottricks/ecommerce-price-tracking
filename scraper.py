import re
import requests
from bs4 import BeautifulSoup
from database import save_product
from utils import extract_domain

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

async def scrape_and_store_price(url, chat_id):
    try:
        domain = extract_domain(url)
        title, price = None, None

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        if "amazon" in domain:
            title = soup.select_one("#productTitle")
            price = soup.select_one(".a-price .a-offscreen")
        elif "flipkart" in domain:
            title = soup.select_one("span.B_NuCI")
            price = soup.select_one("div._30jeq3")
        elif "ajio" in domain:
            title = soup.select_one("h1.title")
            price = soup.select_one("div.price .amount")
        elif "shopsy" in domain:
            title = soup.select_one("span.B_NuCI")
            price = soup.select_one("div._30jeq3")

        if not title or not price:
            return "Could not scrape the product details. Try another link."

        data = {
            "chat_id": chat_id,
            "url": url,
            "title": title.get_text(strip=True),
            "price": price.get_text(strip=True)
        }
        save_product(data)
        return f"Tracking started: {data['title']} at {data['price']}"
    except Exception as e:
        return f"Error: {str(e)}"
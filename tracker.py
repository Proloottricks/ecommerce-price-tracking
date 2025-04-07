import requests from bs4 import BeautifulSoup import re

def get_price_details(url): headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36" }

try:
    res = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(res.text, 'html.parser')

    if 'amazon' in url:
        title = soup.find(id='productTitle').get_text(strip=True)
        price_tag = soup.find('span', {'class': 'a-price-whole'})
        price = price_tag.get_text(strip=True).replace(',', '') if price_tag else '0'
        return title, int(float(price)), 'Amazon'

    elif 'flipkart' in url:
        title = soup.find('span', {'class': 'B_NuCI'}).get_text(strip=True)
        price_tag = soup.find('div', {'class': '_30jeq3 _16Jk6d'})
        price = price_tag.get_text(strip=True).replace('₹', '').replace(',', '') if price_tag else '0'
        return title, int(float(price)), 'Flipkart'

    elif 'ajio' in url:
        title_tag = soup.find('h1', {'class': 'prod-title'})
        price_tag = soup.find('div', {'class': 'prod-sp'})
        title = title_tag.get_text(strip=True) if title_tag else 'Ajio Product'
        price = re.findall(r'\d+', price_tag.get_text()) if price_tag else ['0']
        return title, int(''.join(price)), 'Ajio'

    elif 'shopsy' in url:
        title = soup.find('span', {'class': 'B_NuCI'}).get_text(strip=True)
        price_tag = soup.find('div', {'class': '_30jeq3 _16Jk6d'})
        price = price_tag.get_text(strip=True).replace('₹', '').replace(',', '') if price_tag else '0'
        return title, int(float(price)), 'Shopsy'

except Exception as e:
    print("Error fetching details:", e)

return None


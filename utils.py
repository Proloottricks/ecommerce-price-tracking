from urllib.parse import urlparse

def extract_domain(url):
    return urlparse(url).netloc

def format_price_message(product):
    return f"Product: {product['title']}\nPrice: {product['price']}\nURL: {product['url']}"
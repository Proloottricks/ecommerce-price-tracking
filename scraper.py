import re

def get_platform_and_clean_url(url):
    if 'amazon.' in url:
        return 'amazon', url.split('?')[0]
    elif 'flipkart.' in url:
        return 'flipkart', url.split('?')[0]
    elif 'ajio.' in url:
        return 'ajio', url.split('?')[0]
    elif 'shopsy.' in url:
        return 'shopsy', url.split('?')[0]
    else:
        return 'unknown', url

def add_affiliate_tag(url, platform, tags):
    if platform == "amazon":
        if "tag=" not in url:
            return f"{url}?tag={tags.get('AMAZON_TAG', '')}"
    elif platform == "flipkart":
        if "affid=" not in url:
            return f"{url}&affid={tags.get('FLIPKART_TAG', '')}"
    elif platform == "ajio":
        if "affid=" not in url:
            return f"{url}?affid={tags.get('AJIO_TAG', '')}"
    elif platform == "shopsy":
        if "affid=" not in url:
            return f"{url}?affid={tags.get('SHOPSY_TAG', '')}"
    return url

def fetch_price_and_title(url, platform):
    # Placeholder dummy logic — replace with actual scraping logic
    return "Product Title
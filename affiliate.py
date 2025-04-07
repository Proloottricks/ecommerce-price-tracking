import os from urllib.parse import urlencode, urlparse, parse_qs, urlunparse from dotenv import load_dotenv

load_dotenv()

def convert_to_affiliate(url, platform): if platform == 'Amazon': tag = os.getenv('AFFILIATE_ID_AMAZON') parsed = urlparse(url) query = parse_qs(parsed.query) query['tag'] = [tag] new_query = urlencode(query, doseq=True) return urlunparse(parsed._replace(query=new_query))

elif platform == 'Flipkart':
    tag = os.getenv('AFFILIATE_ID_FLIPKART')
    return f"{url}?affid={tag}"

elif platform == 'Ajio':
    tag = os.getenv('AFFILIATE_ID_AJIO')
    return f"https://www.ajio.com/?_r=aff:{tag}&redirectUrl={url}"

elif platform == 'Shopsy':
    tag = os.getenv('AFFILIATE_ID_SHOPSY')
    return f"{url}?affid={tag}"

return url


from urllib.parse import urlparse

def get_domain_name(url):
    return urlparse(url).netloc.split(".")[0]
def convert_to_affiliate(url):
    if "amazon" in url:
        return url.split("?")[0] + "?tag=yourtag-21"
    elif "flipkart" in url:
        return url.split("?")[0] + "?affid=youraffid"
    elif "ajio" in url:
        return url.split("?")[0] + "?aff=youraffid"
    elif "shopsy" in url:
        return url.split("?")[0] + "?affid=youraffid"
    return url
from dotenv import load_dotenv
import os

load_dotenv()

TAGS = {
    "AMAZON_TAG": os.getenv("AMAZON_TAG"),
    "FLIPKART_TAG": os.getenv("FLIPKART_TAG"),
    "AJIO_TAG": os.getenv("AJIO_TAG"),
    "SHOPSY_TAG": os.getenv("SHOPSY_TAG")
}
import logging
import requests
from bs4 import BeautifulSoup

# Setup Logging
LOG_FILE = "backend/logs/scrape.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def scrape_url(url: str):
    """Scrapes visible content from a webpage using requests & BeautifulSoup."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        with requests.Session() as session:  # Ensure session closure
            response = session.get(url, headers=headers, timeout=10)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        text_elements = soup.find_all(["p", "h1", "h2", "h3", "li"])
        text = " ".join([elem.get_text().strip() for elem in text_elements])
        clean_text = " ".join(text.split())

        if not clean_text:
            logging.error(f"No valid text found for {url}")
            return None

        logging.debug(f"Scraping successful for URL: {url}")
        return clean_text

    except requests.exceptions.RequestException as e:
        logging.error(f"Error scraping {url}: {str(e)}")
        return None

from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from validators import url as valid_url


def is_valid_url_format(url):
    try:
        return valid_url(url)
    except Exception as e:
        print(f"Error validating URL: {e}")
        return False


def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def scrape_website_links(url) -> list:
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.find_all("a", href=True)
    except requests.exceptions.RequestException as e:
        print(f"Error scraping '{url}': {e}")
        raise


def find_broken_links(url) -> list:
    invalid_links = []
    try:
        if is_valid_url_format(url=url):
            links = scrape_website_links(url=url)

            for link in links:
                link_url = link["href"]
                # join the URL as per host name of original URL
                full_url = urljoin(url, link_url)

                if not is_valid_url_format(url=full_url):
                    invalid_links.append(full_url)
                    continue

                if not is_valid_url(full_url):
                    invalid_links.append(full_url)
                    continue

    except Exception as e:
        print(f"Error identifying invalid links for '{url}': {e}")
        raise
    return invalid_links

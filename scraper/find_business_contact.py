import requests
from bs4 import BeautifulSoup
import time
import random
import string
from urllib.parse import urlparse, urljoin
import json
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from stem import Signal
from stem.control import Controller

# Constants
TOR_PASSWORD = "your_password"  # Replace with your hashed Tor control password
GOOGLE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Initialize Selenium with Tor
def init_selenium_with_tor():
    options = webdriver.FirefoxOptions()
    options.add_argument("--proxy-server=socks5://127.0.0.1:9050")
    driver = webdriver.Firefox(options=options)
    return driver

# Change Tor IP
def renew_tor_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password=TOR_PASSWORD)
        controller.signal(Signal.NEWNYM)

# Scrape multiple URLs with Tor
def scrape_with_tor(urls):
    driver = init_selenium_with_tor()
    html_pages = []
    try:
        for i, url in enumerate(urls):
            if i % 5 == 0:  # Change IP every 5 requests
                renew_tor_ip()
                time.sleep(10)
            driver.get(url)
            try:
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                html_pages.append(driver.page_source)
                print(f"Scraped: {url}")
            except Exception as e:
                print(f"Failed to load {url}: {e}")
    finally:
        driver.quit()
    return html_pages

# Fetch webpage HTML with requests
def get_html(url):
    response = requests.get(url, headers=GOOGLE_HEADERS)
    if response.status_code == 200:
        time.sleep(random.uniform(1, 3))
        return response.text
    print(f"Failed to fetch {url}: {response.status_code}")
    return ""

# Convert HTML to plain text
def html_to_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text(separator=" ")

# Google search and extract top links
def get_google_links(query, num_results=3, retries=3):
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    for _ in range(retries):
        response = requests.get(search_url, headers=GOOGLE_HEADERS)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = [
                a['href'] for a in soup.select('div.yuRUbf a') if a['href'].startswith('http')
            ]
            return links[:num_results]
        time.sleep(random.uniform(1, 3))
    raise Exception("Failed to fetch Google search results.")

# Get the domain with the fewest subdirectories
def find_main_domain(links):
    return min(links, key=lambda url: len(urlparse(url).path.split('/')))

# Extract emails from HTML content
def extract_emails(html):
    return list(set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", html)))

# Extract phone numbers from HTML content
def extract_phone_numbers(html):
    return list(set(re.findall(r"\(?\b[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b", html)))

# Extract addresses using regex
def extract_addresses(html):
    pattern = re.compile(
        r"\d{1,5}\s\w+(\s\w+)*\s(?:Street|St|Avenue|Ave|Boulevard|Blvd|Road|Rd|Lane|Ln|Drive|Dr|Court|Ct|Square|Sq|Parkway|Pkwy|Circle|Cir)\b[^\d]*\d{5}(?:-\d{4})?",
        re.IGNORECASE,
    )
    return list(set(pattern.findall(html)))

# Extract structured address from schema.org
def extract_address_from_schema(html):
    soup = BeautifulSoup(html, 'html.parser')
    for script in soup.find_all('script', type='application/ld+json'):
        try:
            data = json.loads(script.string)
            if isinstance(data, dict) and 'address' in data:
                addr = data['address']
                return f"{addr.get('streetAddress', '')}, {addr.get('addressLocality', '')}, {addr.get('addressRegion', '')} {addr.get('postalCode', '')}"
        except json.JSONDecodeError:
            continue
    return None

# Extract social media links
def extract_social_links(html, base_url=""):
    platforms = {
        "facebook": "facebook.com",
        "twitter": "twitter.com",
        "linkedin": "linkedin.com",
        "instagram": "instagram.com",
        "youtube": "youtube.com",
        "tiktok": "tiktok.com",
    }
    soup = BeautifulSoup(html, 'html.parser')
    links = {
        platform: urljoin(base_url, a['href'])
        for a in soup.find_all('a', href=True)
        for platform, domain in platforms.items()
        if domain in a['href']
    }
    return links

# Main enrichment function
def enrich_company_data(company_name, domain=None):
    if not domain:
        links = get_google_links(company_name, num_results=3)
        domain = find_main_domain(links)
    print(f"Company domain: {domain}")

    emails, addresses, phones, social_links = set(), set(), set(), {}
    html_pages = [get_html(domain)] + [get_html(link) for link in get_google_links(f"{company_name} contact", 3)]

    for html in html_pages:
        emails.update(extract_emails(html))
        addresses.update(extract_addresses(html))
        phones.update(extract_phone_numbers(html))
        social_links.update(extract_social_links(html, domain))

    schema_address = extract_address_from_schema(html_pages[0])
    if schema_address:
        addresses.add(schema_address)

    print("Emails:", emails)
    print("Addresses:", addresses)
    print("Phones:", phones)
    print("Social Media:", social_links)

# Example Usage
if __name__ == "__main__":
    enrich_company_data("Abbott Laboratories")

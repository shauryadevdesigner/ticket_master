import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from playwright.sync_api import sync_playwright

def scrape_ticket_status(url):
    """
    Scrape the ticket status from a Ticketmaster event page using Selenium if it's a Ticketmaster URL, otherwise use requests and BeautifulSoup.
    Returns the status text (e.g., 'Buy Tickets', 'Tickets Not Available', etc.) or None if failed.
    """
    if 'ticketmaster' in url:
        return scrape_with_selenium(url)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        # Try to find common ticket status elements
        for text in ["Buy Tickets", "Tickets Not Available", "Find Tickets", "Sold Out"]:
            if soup.body and text.lower() in soup.body.get_text().lower():
                return text
        # Fallback: return a snippet of the page title or main button
        title = soup.title.string if soup.title else "Unknown"
        return title
    except Exception as e:
        logging.error(f"[scraper] Error scraping {url}: {e}")
        return None

def scrape_with_selenium(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        for text in ["Buy Tickets", "Tickets Not Available", "Find Tickets", "Sold Out"]:
            if soup.body and text.lower() in soup.body.get_text().lower():
                return text
        title = soup.title.string if soup.title else "Unknown"
        return title
    except Exception as e:
        logging.error(f"[scraper] Error scraping {url} with Selenium: {e}")
        return None
    finally:
        driver.quit()

# Optional: Selenium/Playwright fallback if needed
# def scrape_with_playwright(url):
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         page = browser.new_page()
#         page.goto(url)
#         time.sleep(5)
#         html = page.content()
#         browser.close()
#         soup = BeautifulSoup(html, 'html.parser')
#         # ... same logic as above ...
#         return ... 
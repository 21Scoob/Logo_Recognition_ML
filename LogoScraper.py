import sys
import os
import time
import asyncio
import aiohttp
import requests
import pandas as pd
import tldextract
import ssl
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from io import BytesIO
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from selenium_stealth import stealth
from time import sleep
from urllib.parse import urlparse
import nest_asyncio

# On Windows, force the Selector Event Loop Policy to avoid socket errors
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Apply nest_asyncio for compatibility if needed
nest_asyncio.apply()

# Load the Parquet file
df = pd.read_parquet("logos.snappy.parquet", engine="fastparquet")
domains = df['domain'].tolist()

# Ensure logos directory exists
os.makedirs("logos", exist_ok=True)

# ----------- ASYNC LOGO SCRAPING WITH BEAUTIFULSOUP -----------
async def extract_logo_html(session, domain):
    """Extract logo from HTML source, with HTTP fallback and SSL handling."""
    for protocol in ["https", "http"]:
        url = f"{protocol}://{domain}"
        try:
            async with session.get(url, timeout=10, ssl=False) as response:
                if response.status != 200:
                    continue
                soup = BeautifulSoup(await response.text(), "html.parser")
                for img in soup.find_all("img"):
                    if "logo" in img.get("alt", "").lower() or "logo" in img.get("src", "").lower():
                        return urljoin(url, img.get("src"))
        except Exception as e:
            print(f"⚠️ {protocol.upper()} failed for {domain}: {e}")
    print(f"❌ HTML extraction failed for {domain}")
    return None

# ----------- FALLBACK: GET FAVICON -----------
def get_favicon(domain, max_retries=10, timeout=10):
    """Attempt to fetch the website's favicon with retries."""
    root_domain = tldextract.extract(domain).registered_domain
    favicon_url = f"https://{root_domain}/favicon.ico"
    for attempt in range(max_retries):
        try:
            response = requests.get(favicon_url, timeout=timeout)
            if response.status_code == 200:
                return favicon_url
        except requests.Timeout:
            print(f"⚠️ Timeout fetching favicon for {domain}. Retrying ({attempt+1}/{max_retries})...")
        except requests.RequestException:
            break
        sleep(1)
    print(f"❌ Failed to fetch favicon for {domain} after {max_retries} attempts.")
    return None

# ----------- FALLBACK: SELENIUM FOR JS-HEAVY SITES -----------
def get_logo_selenium(driver, domain):
    """Use Selenium to extract logos from JavaScript-heavy sites."""
    try:
        url = f"https://{domain}"
        driver.get(url)
        time.sleep(5)  # Allow time for images to load
        logo_elements = driver.find_elements(By.TAG_NAME, "img")
        for img in logo_elements:
            logo_url = img.get_attribute("src")
            alt_text = img.get_attribute("alt")
            if logo_url and ("logo" in logo_url.lower() or (alt_text and "logo" in alt_text.lower())):
                return logo_url
    except Exception as e:
        print(f"❌ Selenium failed for {domain}: {e}")
    return None

# ----------- DOWNLOAD LOGO -----------
def download_logo(url, domain):
    """Download logo if it doesn't already exist."""
    if url.startswith("data:image"):
        print(f"⚠️ Skipping data URL for {domain}.")
        return False
    logo_path = f"logos/{domain}.png"
    if os.path.exists(logo_path):
        print(f"🔄 Logo for {domain} already exists. Skipping download.")
        return True
    try:
        response = requests.get(url, timeout=10, stream=True)
        if response.status_code == 200:
            img_data = BytesIO(response.content)
            img = Image.open(img_data)
            img.save(logo_path)
            print(f"✅ Logo saved for {domain}")
            return True
    except Exception as e:
        print(f"❌ Error saving logo for {domain}: {e}")
    return False

# ----------- MAIN PIPELINE FUNCTION -----------
async def process_domain(session, driver, domain):
    """Process each domain by checking for logos using multiple methods."""
    logo_url = await extract_logo_html(session, domain)
    if not logo_url:
        logo_url = get_favicon(domain)
    if not logo_url:
        logo_url = get_logo_selenium(driver, domain)
    if logo_url:
        return download_logo(logo_url, domain)
    print(f"❌ No logo found for {domain}")
    return False

async def run_async_tasks():
    """Main function to manage asynchronous logo extraction."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")

    driver = uc.Chrome(options=options, headless=True)
    stealth(driver, languages=["en-US", "en"], vendor="Google Inc.", platform="Win32",
            webgl_vendor="Intel Inc.", renderer="Intel Iris OpenGL Engine", fix_hairline=True)
    driver.set_page_load_timeout(15)

    # Setup SSL context to bypass SSL issues (if needed)
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with aiohttp.ClientSession() as session:
        tasks = [process_domain(session, driver, domain) for domain in domains]
        await asyncio.gather(*tasks)

    driver.quit()

def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(run_async_tasks())
    except KeyboardInterrupt:
        print("\n🛑 Process interrupted by user.")
    finally:
        loop.close()

if __name__ == "__main__":
    main()

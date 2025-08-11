# scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_navi_mumbai_properties():
    """
    Scrapes property data from 99acres.
    This version uses an explicit wait to ensure the page content is loaded before parsing.
    """
    URL = "https://www.99acres.com/property-in-navi-mumbai-ffid?property_type=1%2C4%2C2%2C3&budget_min=100&budget_max=500&locality_array=197&page=1"
    
    # Optimized Chrome options for cloud deployment
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")

    print("Setting up Selenium with automatic driver manager...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    html_content = None
    print("Launching browser to visit 99acres.com...")
    try:
        driver.get(URL)
        
        # Intelligent wait: Waits up to 30 seconds for the first property card to become visible.
        print("Waiting for property cards to appear on the page (max 30 seconds)...")
        wait = WebDriverWait(driver, 30)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tupleNew__outerTupleWrap")))
        print("Property cards have appeared!")
        
        time.sleep(2) # Give a couple of extra seconds for the page to settle.
        
        html_content = driver.page_source
        print("Page content loaded successfully.")
        
    except Exception as e:
        print(f"Error with Selenium (e.g., timeout waiting for cards): {e}")
        return pd.DataFrame()
    finally:
        print("Closing the browser.")
        driver.quit()

    print("Parsing HTML content...")
    soup = BeautifulSoup(html_content, 'html.parser')
    
    properties_list = []
    
    # Find all property cards using the main container class
    property_cards = soup.find_all('div', class_='tupleNew__outerTupleWrap')

    if not property_cards:
        print("Could not find any property cards. The website structure may have changed.")
        return pd.DataFrame()

    print(f"Found {len(property_cards)} properties on the page. Extracting details...")

    for card in property_cards:
        title, price, area, bedrooms = 'N/A', 'N/A', 'N/A', 'N/A'
        try:
            title_tag = card.find('a', class_='tupleNew__propertyHeading')
            if title_tag: title = title_tag.get_text(strip=True)

            price_tag = card.find('div', class_='tupleNew__priceValWrap')
            if price_tag: price = price_tag.get_text(strip=True)

            area_wraps = card.find_all('div', class_='tupleNew__areaWrap')
            if area_wraps:
                area_tag = area_wraps[0].find('span', class_='tupleNew__area1Type')
                if area_tag: area = area_tag.get_text(strip=True)
                
                if len(area_wraps) > 1:
                    bedrooms_tag = area_wraps[1].find('span', class_='tupleNew__area1Type')
                    if bedrooms_tag: bedrooms = bedrooms_tag.get_text(strip=True)
            
            properties_list.append({
                'title': title, 'price_text': price, 'bedrooms': bedrooms, 'area_sqft': area
            })
        except Exception as e:
            print(f"Error parsing one of the cards. Skipping. Details: {e}")
            continue
    
    return pd.DataFrame(properties_list)
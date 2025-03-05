import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import re
import os
import platform

def setup_driver():
    """
    Set up Chrome WebDriver with appropriate options for both development and deployment environments.
    """
    options = webdriver.ChromeOptions()

    # Essential arguments for headless operation
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Additional security and performance options
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-setuid-sandbox')
    options.add_argument('--window-size=1920,1080')

    # Set user agent
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

    try:
        if platform.system() == 'Darwin':  # macOS (local development)
            chrome_path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
            if os.path.exists(chrome_path):
                options.binary_location = chrome_path
        elif platform.system() == 'Linux':  # Linux (deployment environment)
            # Use Chromium for headless operation on Linux
            options.binary_location = '/usr/bin/chromium-browser'  # Or '/usr/bin/chromium'
            
        # Use ChromeDriverManager for driver installation
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    
    except Exception as e:
        print(f"Error in setup_driver: {str(e)}")
        # Fallback attempt without specific binary location
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Chrome(options=options)
            return driver
        except Exception as e:
            print(f"Failed to create Chrome driver with fallback: {str(e)}")
            raise


def get_image_urls(driver):
    """Extracts and returns image URLs meeting a minimum size requirement."""
    try:
        images = driver.find_elements(By.CSS_SELECTOR, 'img.pswp__img')
        urls = set()

        for img in images:
            try:
                img_src = img.get_attribute('src')
                if not img_src:
                    continue

                # Extract image dimensions from URL
                match = re.search(r"fit-in/(\d+)x(\d+)", img_src)
                if match:
                    width, height = map(int, match.groups())
                    if height >= 300:
                        urls.add(img_src)
            except Exception as e:
                print(f"Error processing image: {str(e)}")
                continue

        return urls
    except Exception as e:
        print(f"Error in get_image_urls: {str(e)}")
        return set()

def scrape_images(url, n=10):
    """
    Scrape images from the property listing page with improved error handling.
    """
    driver = None
    try:
        driver = setup_driver()
        driver.set_page_load_timeout(30)  # Set page load timeout
        driver.get(url)
        
        # Wait for page to load
        time.sleep(5)
        
        try:
            # Click on the image gallery trigger
            gallery_trigger = driver.find_element(By.CLASS_NAME, 'css-8yo374')
            gallery_trigger.click()
            time.sleep(3)  # Allow time for images to load
        except Exception as e:
            print(f"Error accessing image gallery: {str(e)}")
            return set()

        image_urls = set()
        attempts = 0
        max_attempts = 10

        while len(image_urls) < n and attempts < max_attempts:
            try:
                # Update image URLs
                new_urls = get_image_urls(driver)
                image_urls.update(new_urls)
                
                if len(image_urls) >= n:
                    break

                # Try to click next button
                next_button = driver.find_element(By.CSS_SELECTOR, "button.pswp__button.css-a0zf3")
                next_button.click()
                time.sleep(2)
                
            except Exception as e:
                print(f"Error during image collection: {str(e)}")
                attempts += 1

        return list(image_urls)[:n]  # Return only the requested number of images

    except Exception as e:
        print(f"Error in scrape_images: {str(e)}")
        return []

    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

def get_static_images():
    """Return a list of static property images."""
    return [
        '/static/property_snap/property_images/property1.jpg',
        '/static/property_snap/property_images/property2.jpg',
        '/static/property_snap/property_images/property3.jpg',
        '/static/property_snap/property_images/property4.jpg',
        '/static/property_snap/property_images/property5.jpg'
    ]

def scrape_images(url, n=5):
    """
    Return static image URLs instead of scraping.
    """
    return get_static_images()[:n]

def main(url, n=5):
    """
    Main function to get property images.
    """
    return scrape_images(url, n)

if __name__ == "__main__":
    url = "https://www.domain.com.au/example"
    output = main(url, n=5)
    print(f"Found {len(output)} images")
    
    
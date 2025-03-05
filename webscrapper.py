import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re



def setup_driver():
    options = webdriver.ChromeOptions()
    options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

    # Browser options for better performance and compatibility
    options.add_argument("--headless")  
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument("accept-language=en-US,en;q=0.9")
    options.add_argument("accept-encoding=gzip, deflate, br")
    options.add_argument("connection=keep-alive")
    options.add_argument("upgrade-insecure-requests=1")

    service =  webdriver.ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def get_image_urls(driver):
    """Extracts and returns image URLs meeting a minimum size requirement."""
    images = driver.find_elements(By.CSS_SELECTOR, 'img.pswp__img')
    urls = set()

    for img in images:
        img_src = img.get_attribute('src')

        # Extract image dimensions from URL
        match = re.search(r"fit-in/(\d+)x(\d+)", img_src)
        if match:
            width, height = map(int, match.groups())
            img_size = width * height

            # Store images larger than 300 pixels
            if height >= 300:
                urls.add(img_src)
            else:
                #print("Skipped small image.")
                pass

    #print(f"Total valid images: {len(urls)}")
    return urls

def scrape_images(url,n = 10):
    driver = setup_driver()
    driver.get(url)
    driver.maximize_window()

    try:
        # Click on the image gallery trigger
        driver.find_element(By.CLASS_NAME, 'css-8yo374').click()
        time.sleep(3)  # Allow time for images to load

        image_urls = set()

        start, end = 0, 1
        while start < end:
            # Extract current image position
            position_text = driver.find_element(By.CLASS_NAME, 'css-1ljuah8').text
            numbers = re.findall(r'\d+', position_text)
            if len(numbers) == 2:
                start, end = map(int, numbers)

            # Collect image URLs
            image_urls.update(get_image_urls(driver))
            
            
        
            if len(image_urls) >= n:
                while len(image_urls) > n:
                    image_urls.pop()
                break
            # Click next image button
            next_button = driver.find_element(By.CSS_SELECTOR, "button.pswp__button.css-a0zf3")
            next_button.click()
            time.sleep(2)

        #print(f"Scraping complete. Total images collected: {len(image_urls)}")

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        driver.quit()

    return image_urls

def main(url, n = 5):

    images = list(scrape_images(url,n))
    return images
    
    
if __name__ == "__main__":
    url = "https://www.domain.com.au/52-tuppal-drive-wyndham-vale-vic-3024-2019686426?topspot=1"
    output = main(url, n = 2)

    
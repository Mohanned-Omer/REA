import google.generativeai as genai
from google.generativeai import types
import requests
import pathlib
from PIL import Image
import os
from webscrapper import scrape_images
from dotenv import load_dotenv
import io

load_dotenv()

SYSTEM_PROMPT = """\
You are a professional real estate listing assistant. Analyze the provided property images and create a detailed, factual description focusing on:

1. Visual features and materials
2. Room layouts and architectural elements
3. Outdoor spaces and exterior features

Guidelines:
- Describe only what you can see in the images
- Use professional, neutral language
- Avoid assumptions about luxury or quality
- Structure the description by areas (Kitchen, Living Areas, etc.)
- Include specific, observable details

Format your response as a clear, well-organized description without special formatting or markdown."""

def convert_image_to_part(image_url):
    response = requests.get(image_url)
    image = Image.open(io.BytesIO(response.content))
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='JPEG')  # Ensure it's in JPEG format
    image_bytes.seek(0)
    return types.Part.from_bytes(
        data=image_bytes.read(),
        mime_type="image/jpeg"
    )
    
def generate_property_description(property_url, n=5):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    # Scrape image URLs
    image_urls = list(scrape_images(property_url, n=n))

    # Convert each downloaded image to base64-encoded format
    downloaded_images = [convert_image_to_part(image_url) for image_url in image_urls]

    # Generate the content description
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=[SYSTEM_PROMPT,
                  *downloaded_images])

    # Ensure we get a string response
    description = ""
    if hasattr(response, 'text'):
        description = response.text
    elif hasattr(response, 'parts'):
        description = response.parts[0].text
    else:
        description = str(response)

    return description, image_urls


def main():
    property_url = "https://www.domain.com.au/52-tuppal-drive-wyndham-vale-vic-3024-2019686426?topspot=1"
    description, image_urls = generate_property_description(property_url)
    print(description)
    



if __name__ == "__main__":
    
    main()
    
    

    
    
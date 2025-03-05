# Property Snap 🏠

A smart property analysis tool that uses AI to generate detailed property descriptions from images. Whether you're a real estate agent or property enthusiast, Property Snap helps you create professional property descriptions in seconds.

Learn more by reading the about tab when launching the website locally



## Tech Stack 🛠️

- Django
- Google Gemini Vision AI
- Pillow (PIL) for image processing
- Selenium for web scraping

## Getting Started 🚀

I tried to deploy the website but there are too many scrapping issues so I resorted to allowing the users to run it locally on their device

1. **Clone the repository**
   ```bash
   git clone [your-repo-url]
   cd property-snap
   ```

2. **Set up your environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory with:
   ```
   GOOGLE_API_KEY=your_api_key_here
   DJANGO_SECRET_KEY=your_secret_key_here
   DJANGO_DEBUG=True
   ```

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```

6. **Visit the application**
   Open your browser and go to your local host

## How It Works 🔍

1. Upload property images or provide a property URL
2. The system processes the images using Gemini Vision AI
3. AI analyzes the images and generates a detailed property description
4. The description is formatted and displayed to the user

## Project Structure 📁

```
property-snap/
├── property_snap/          # Main app directory
│   ├── static/            # Static files (CSS, JS, images)
│   ├── templates/         # HTML templates
│   ├── views.py          # View logic
│   └── urls.py           # URL routing
├── main.py               # Core AI processing logic
├── webscrapper.py        # Image scraping functionality
└── manage.py            # Django management script
```

---

Made with ❤️ by [Mohanned]
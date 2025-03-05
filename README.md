# Property Snap 🏠

Property Snap is a Django web application that uses AI to analyze real estate property listings. It scrapes property images and generates detailed descriptions using Google's Generative AI.

## Features 🌟

- Image scraping from property listings
- AI-powered property description generation
- Modern, responsive UI
- Real-time property analysis

## Prerequisites 📋

Before you begin, ensure you have the following installed:
- Python 3.11 or higher
- pip (Python package manager)
- Git

## Setup Instructions 🚀

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/property-snap.git
   cd property-snap
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   Create a `.env` file in the root directory with the following variables:
   ```
   DJANGO_SECRET_KEY=your-secret-key
   DJANGO_DEBUG=True
   GOOGLE_API_KEY=your-google-api-key
   ```

6. **Apply database migrations**
   ```bash
   python manage.py migrate
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

The application will be available at `http://localhost:8000`

## Environment Variables 🔐

| Variable | Description | Required |
|----------|-------------|----------|
| DJANGO_SECRET_KEY | Django secret key for security | Yes |
| DJANGO_DEBUG | Debug mode (True/False) | No (defaults to False) |
| GOOGLE_API_KEY | Google Generative AI API key | Yes |
| DATABASE_URL | Database connection URL | No (defaults to SQLite) |

## Project Structure 📁

```
property_snap/
├── static/              # Static files (CSS, JS, images)
├── templates/           # HTML templates
├── views.py            # View functions
├── urls.py            # URL configurations
└── models.py          # Database models
```

## Usage 💡

1. Navigate to the homepage
2. Enter a property listing URL in the input field
3. Click "Analyze Property"
4. View the AI-generated description and scraped images

## Contributing 🤝

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- Google Generative AI for powering the description generation
- Django framework
- All contributors and users of the application 
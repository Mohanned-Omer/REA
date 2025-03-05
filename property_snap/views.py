from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe
import json
import markdown
from main import generate_property_description
from webscrapper import scrape_images

def main(request):
    return render(request, 'main.html')

def about(request):
    return render(request, 'about.html')

@csrf_exempt
def analyze_property(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            property_url = data.get('url')
            
            if not property_url:
                return JsonResponse({'error': 'No URL provided'}, status=400)
            
            description, image_urls = generate_property_description(property_url, n=5)
            
            # Convert markdown to HTML
            html_description = markdown.markdown(description)
            
            # Mark the HTML as safe
            safe_description = mark_safe(html_description)
            
            return JsonResponse({
                'description': safe_description,
                'images': image_urls,
                'status': 'success'
            })
            
        except Exception as e:
            print(f"Error in analyze_property: {str(e)}")  # Add debugging
            return JsonResponse({
                'error': str(e),
                'status': 'error'
            }, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)
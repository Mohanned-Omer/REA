from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe
import json
import markdown
from main import generate_property_description
from webscrapper import scrape_images
import logging
import traceback

logger = logging.getLogger('property_snap')

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
                logger.warning('No URL provided in request')
                return JsonResponse({'error': 'No URL provided', 'status': 'error'}, status=400)
            
            logger.info(f'Processing property URL: {property_url}')
            
            # First try to scrape images
            try:
                image_urls = list(scrape_images(property_url, n=5))
                if not image_urls:
                    logger.warning(f'No images found for URL: {property_url}')
                    return JsonResponse({
                        'error': 'No images found for this property',
                        'status': 'error'
                    }, status=400)
                logger.info(f'Successfully scraped {len(image_urls)} images')
            except Exception as e:
                logger.error(f'Error scraping images: {str(e)}\n{traceback.format_exc()}')
                return JsonResponse({
                    'error': 'Failed to scrape property images',
                    'status': 'error'
                }, status=500)
            
            # Then generate description
            try:
                description, _ = generate_property_description(property_url, n=5)
                logger.info('Successfully generated property description')
            except Exception as e:
                logger.error(f'Error generating description: {str(e)}\n{traceback.format_exc()}')
                return JsonResponse({
                    'error': 'Failed to generate property description',
                    'status': 'error'
                }, status=500)
            
            # Convert markdown to HTML
            try:
                html_description = markdown.markdown(description)
                safe_description = mark_safe(html_description)
                logger.info('Successfully converted description to HTML')
            except Exception as e:
                logger.error(f'Error converting markdown: {str(e)}\n{traceback.format_exc()}')
                return JsonResponse({
                    'error': 'Failed to format property description',
                    'status': 'error'
                }, status=500)
            
            return JsonResponse({
                'description': safe_description,
                'images': image_urls,
                'status': 'success'
            })
            
        except json.JSONDecodeError as e:
            logger.error(f'Invalid JSON in request: {str(e)}')
            return JsonResponse({
                'error': 'Invalid JSON in request',
                'status': 'error'
            }, status=400)
        except Exception as e:
            logger.error(f'Unexpected error: {str(e)}\n{traceback.format_exc()}')
            return JsonResponse({
                'error': 'An unexpected error occurred',
                'status': 'error'
            }, status=500)
    
    logger.warning(f'Invalid request method: {request.method}')
    return JsonResponse({'error': 'Invalid request method', 'status': 'error'}, status=405)
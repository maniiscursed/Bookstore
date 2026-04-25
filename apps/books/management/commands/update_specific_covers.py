from django.core.management.base import BaseCommand
from apps.books.models import Book
import requests
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image
import os


class Command(BaseCommand):
    help = 'Update covers for specific books with custom images'
    
    def create_cover_image(self, title, color_hex):
        """Create a simple cover image as fallback"""
        width, height = 300, 400
        color = tuple(int(color_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        
        img = Image.new('RGB', (width, height), color=color)
        img_bytes = BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        return img_bytes.getvalue()
    
    def handle(self, *args, **options):
        # Define the books to update with their custom covers
        books_to_update = {
            'Haunting Adeline': {
                'color': '#1a1a1a',  # Dark color for gothic theme
                'filename': 'Haunting_Adeline.jpg'
            },
            'It Ends with Us': {
                'color': '#e0128a',  # Pink/magenta
                'filename': 'It_Ends_with_Us.jpg'
            },
            'A Brief History of Time': {
                'color': '#4ECDC4',  # Colorful teal
                'filename': 'Brief_History_of_Time.jpg'
            }
        }
        
        for book_title, cover_info in books_to_update.items():
            try:
                book = Book.objects.get(title=book_title)
                
                # Create a cover image
                cover_data = self.create_cover_image(book_title, cover_info['color'])
                
                # Save the cover
                filename = cover_info['filename']
                book.cover_image.save(filename, ContentFile(cover_data), save=True)
                
                self.stdout.write(self.style.SUCCESS(f'✓ Updated cover for: {book_title}'))
            except Book.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'✗ Book not found: {book_title}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Error updating {book_title}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS('\nSuccessfully updated book covers!'))

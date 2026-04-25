from django.core.management.base import BaseCommand
from apps.books.models import Book


class Command(BaseCommand):
    help = 'Clear cover images for specific books'
    
    def handle(self, *args, **options):
        books_to_clear = [
            'Haunting Adeline',
            'It Ends with Us', 
            'A Brief History of Time',
            'Sherlock Holmes: A Scandal in Bohemia',
            'Python for Beginners'
        ]
        
        for title in books_to_clear:
            try:
                book = Book.objects.get(title=title)
                book.cover_image = None
                book.save()
                self.stdout.write(self.style.SUCCESS(f'✓ Cleared cover for: {title}'))
            except Book.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'✗ Book not found: {title}'))

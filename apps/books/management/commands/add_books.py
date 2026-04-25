from django.core.management.base import BaseCommand
from apps.books.models import Book, Category
from PIL import Image
import io
from django.core.files.base import ContentFile


class Command(BaseCommand):
    help = 'Add specific books to the database'
    
    def create_placeholder_image(self, title):
        """Create a simple placeholder image for books"""
        img = Image.new('RGB', (300, 400), color='steelblue')
        img_io = io.BytesIO()
        img.save(img_io, 'JPEG')
        img_io.seek(0)
        return ContentFile(img_io.getvalue(), name=f'{title.replace(" ", "_")}.jpg')
    
    def handle(self, *args, **options):
        # Get or create Romance category
        romance_cat, _ = Category.objects.get_or_create(
            name='Romance',
            defaults={'description': 'Romance novels'}
        )
        
        # Books to add
        books_to_add = [
            {
                'title': 'It Ends with Us',
                'author': 'Colleen Hoover',
                'description': 'Lily Bloom has survived an abusive childhood by staying strong. But now the tables have turned and Lily questions the man she\'s in love with.',
                'price': '599',
                'isbn': '978-1492210962',
                'publication_date': '2016-08-02',
                'publisher': 'Atria Books',
                'pages': 384,
                'language': 'English',
                'stock': 30,
                'is_bestseller': True,
                'discount_percentage': 10,
            },
            {
                'title': 'Haunting Adeline',
                'author': 'H.D. Carlton',
                'description': 'A mysterious man moves into Adeline\'s house, and obsession begins. Dark romance filled with secrets and danger.',
                'price': '699',
                'isbn': '978-1737632000',
                'publication_date': '2021-05-01',
                'publisher': 'Wattpad Books',
                'pages': 472,
                'language': 'English',
                'stock': 25,
                'is_bestseller': True,
                'discount_percentage': 5,
            }
        ]
        
        for book_data in books_to_add:
            book_data['category'] = romance_cat
            book, created = Book.objects.get_or_create(
                isbn=book_data['isbn'],
                defaults=book_data
            )
            
            # Add placeholder image if book was just created
            if created and not book.cover_image:
                book.cover_image = self.create_placeholder_image(book.title)
                book.save()
                self.stdout.write(self.style.SUCCESS(f'Created: {book.title}'))
            else:
                self.stdout.write(f'Already exists: {book.title}')
        
        self.stdout.write(self.style.SUCCESS('Successfully added books!'))

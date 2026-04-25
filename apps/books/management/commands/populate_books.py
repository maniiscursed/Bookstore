from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.books.models import Category, Book
import json


class Command(BaseCommand):
    help = 'Populate database with sample book data'
    
    def handle(self, *args, **options):
        self.stdout.write('Starting to populate books...')
        
        # Create categories
        categories_data = {
            'Fiction': 'Novels and short stories',
            'Non-Fiction': 'Educational and informational books',
            'Mystery': 'Mystery and thriller novels',
            'Science': 'Science and technology books',
            'History': 'Historical books and biographies',
            'Romance': 'Romance novels',
            'Self-Help': 'Self-improvement and personal development',
            'Children': 'Books for children',
            'Poetry': 'Poetry collections',
            'Technology': 'Books about technology and programming',
        }
        
        categories = {}
        for cat_name, desc in categories_data.items():
            cat, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={'description': desc}
            )
            categories[cat_name] = cat
            if created:
                self.stdout.write(f'Created category: {cat_name}')
        
        # Sample books data
        books_data = [
            {
                'title': 'The Great Gatsby',
                'author': 'F. Scott Fitzgerald',
                'category': 'Fiction',
                'price': 399,
                'isbn': '978-0743273565',
                'publication_date': '1925-04-10',
                'publisher': 'Charles Scribner\'s Sons',
                'pages': 180,
                'language': 'English',
                'description': 'A classic American novel set in the Jazz Age.',
                'stock': 50,
                'is_bestseller': True,
                'discount_percentage': 10,
            },
            {
                'title': 'To Kill a Mockingbird',
                'author': 'Harper Lee',
                'category': 'Fiction',
                'price': 599,
                'isbn': '978-0061120084',
                'publication_date': '1960-07-11',
                'publisher': 'J.B. Lippincott',
                'pages': 324,
                'language': 'English',
                'description': 'A gripping tale of racial injustice and childhood innocence.',
                'stock': 45,
                'is_bestseller': True,
                'discount_percentage': 0,
            },
            {
                'title': 'Python for Beginners',
                'author': 'Mark Lutz',
                'category': 'Technology',
                'price': 999,
                'isbn': '978-1449355739',
                'publication_date': '2013-11-25',
                'publisher': 'O\'Reilly Media',
                'pages': 1500,
                'language': 'English',
                'description': 'Learn Python programming from scratch with practical examples.',
                'stock': 60,
                'is_bestseller': False,
                'discount_percentage': 15,
            },
            {
                'title': 'Sapiens',
                'author': 'Yuval Noah Harari',
                'category': 'Non-Fiction',
                'price': 699,
                'isbn': '978-0062316097',
                'publication_date': '2014-09-30',
                'publisher': 'Harper',
                'pages': 528,
                'language': 'English',
                'description': 'A brief history of humankind from the Stone Age to modern times.',
                'stock': 40,
                'is_bestseller': True,
                'discount_percentage': 5,
            },
            {
                'title': 'Sherlock Holmes: A Scandal in Bohemia',
                'author': 'Arthur Conan Doyle',
                'category': 'Mystery',
                'price': 299,
                'isbn': '978-1503262935',
                'publication_date': '1892-07-01',
                'publisher': 'George Newnes',
                'pages': 120,
                'language': 'English',
                'description': 'A classic mystery featuring the world\'s greatest detective.',
                'stock': 55,
                'is_bestseller': False,
                'discount_percentage': 0,
            },
            {
                'title': 'Atomic Habits',
                'author': 'James Clear',
                'category': 'Self-Help',
                'price': 599,
                'isbn': '978-0735211292',
                'publication_date': '2018-10-16',
                'publisher': 'Avery',
                'pages': 320,
                'language': 'English',
                'description': 'Transform your life by building good habits and breaking bad ones.',
                'stock': 70,
                'is_bestseller': True,
                'discount_percentage': 8,
            },
            {
                'title': 'The Name of the Wind',
                'author': 'Patrick Rothfuss',
                'category': 'Fiction',
                'price': 699,
                'isbn': '978-0756404079',
                'publication_date': '2007-08-27',
                'publisher': 'DAW Books',
                'pages': 662,
                'language': 'English',
                'description': 'An epic fantasy novel with a mysterious protagonist.',
                'stock': 35,
                'is_bestseller': False,
                'discount_percentage': 12,
            },
            {
                'title': 'A Brief History of Time',
                'author': 'Stephen Hawking',
                'category': 'Science',
                'price': 399,
                'isbn': '978-0553382679',
                'publication_date': '1988-04-01',
                'publisher': 'Bantam',
                'pages': 256,
                'language': 'English',
                'description': 'Explore the universe from the Big Bang to black holes.',
                'stock': 42,
                'is_bestseller': True,
                'discount_percentage': 0,
            },
            {
                'title': 'The Midnight Library',
                'author': 'Matt Haig',
                'category': 'Fiction',
                'price': 499,
                'isbn': '978-0525559474',
                'publication_date': '2020-08-13',
                'publisher': 'Viking',
                'pages': 304,
                'language': 'English',
                'description': 'Explore infinite possibilities in a magical library between lives.',
                'stock': 48,
                'is_bestseller': True,
                'discount_percentage': 10,
            },
            {
                'title': 'Clean Code',
                'author': 'Robert C. Martin',
                'category': 'Technology',
                'price': 999,
                'isbn': '978-0132350884',
                'publication_date': '2008-08-01',
                'publisher': 'Prentice Hall',
                'pages': 464,
                'language': 'English',
                'description': 'A manual of software craftsmanship and best practices.',
                'stock': 38,
                'is_bestseller': False,
                'discount_percentage': 20,
            },
        ]
        
        for book_data in books_data:
            cat_name = book_data.pop('category')
            category = categories[cat_name]
            
            book, created = Book.objects.get_or_create(
                isbn=book_data['isbn'],
                defaults={
                    **book_data,
                    'category': category,
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created: {book.title}'))
            else:
                self.stdout.write(f'Already exists: {book.title}')
        
        self.stdout.write(self.style.SUCCESS('Successfully populated books!'))

from decimal import Decimal

from django.core.management.base import BaseCommand

from apps.books.models import Book


class Command(BaseCommand):
    help = 'Convert sample book prices to rupee-style amounts'

    def handle(self, *args, **options):
        price_map = {
            'The Great Gatsby': Decimal('399'),
            'To Kill a Mockingbird': Decimal('599'),
            'Python for Beginners': Decimal('999'),
            'Sapiens': Decimal('699'),
            'Sherlock Holmes: A Scandal in Bohemia': Decimal('299'),
            'Atomic Habits': Decimal('599'),
            'The Name of the Wind': Decimal('699'),
            'A Brief History of Time': Decimal('399'),
            'The Midnight Library': Decimal('499'),
            'Clean Code': Decimal('999'),
            'It Ends with Us': Decimal('599'),
            'Haunting Adeline': Decimal('699'),
        }

        updated_count = 0

        for title, new_price in price_map.items():
            updated = Book.objects.filter(title=title).update(price=new_price)
            if updated:
                updated_count += updated
                self.stdout.write(self.style.SUCCESS(f'✓ Updated {title} to ₹{new_price}'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠ Book not found: {title}'))

        self.stdout.write(self.style.SUCCESS(f'\nUpdated {updated_count} books to rupee prices.'))
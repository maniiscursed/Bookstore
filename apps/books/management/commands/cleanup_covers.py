from django.core.management.base import BaseCommand
from apps.books.models import Book
import os
from pathlib import Path


class Command(BaseCommand):
    help = 'Clean up old cover files and ensure database points to correct covers'
    
    def handle(self, *args, **options):
        media_root = Path('media/book_covers')
        
        # Get all books
        books = Book.objects.all()
        
        for book in books:
            if not book.cover_image:
                self.stdout.write(self.style.WARNING(f'⚠ {book.title} - No cover'))
                continue
            
            # Get current cover filename
            current_filename = book.cover_image.name
            
            # Find all files for this book
            base_name = Path(current_filename).stem  # Get filename without extension
            pattern = f"{base_name}*.jpg"
            
            matching_files = list(media_root.glob(pattern))
            
            if not matching_files:
                self.stdout.write(self.style.WARNING(f'⚠ {book.title} - No files found'))
                continue
            
            # Find the largest file (most likely the real cover)
            largest_file = max(matching_files, key=lambda f: f.stat().st_size)
            largest_size = largest_file.stat().st_size
            
            # Check if current file is good size (real covers are usually > 1000 bytes)
            current_path = media_root / Path(current_filename).name
            if current_path.exists():
                current_size = current_path.stat().st_size
                if current_size > 1000:
                    self.stdout.write(self.style.SUCCESS(f'✓ {book.title} - Current cover is good ({current_size} bytes)'))
                    # Delete other versions
                    for f in matching_files:
                        if f != current_path:
                            f.unlink()
                            self.stdout.write(f'  Deleted: {f.name}')
                    continue
            
            # If current is bad, update to largest
            if largest_size > 1000:
                book.cover_image.name = f"book_covers/{largest_file.name}"
                book.save()
                self.stdout.write(self.style.SUCCESS(f'✓ Updated {book.title} to {largest_file.name} ({largest_size} bytes)'))
                
                # Delete other versions except the new one
                for f in matching_files:
                    if f != largest_file:
                        f.unlink()
                        self.stdout.write(f'  Deleted: {f.name}')
            else:
                self.stdout.write(self.style.ERROR(f'✗ {book.title} - All covers are too small'))
        
        self.stdout.write(self.style.SUCCESS('\nCleanup complete!'))

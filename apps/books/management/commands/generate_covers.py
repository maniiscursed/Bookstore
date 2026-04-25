from django.core.management.base import BaseCommand
from apps.books.models import Book
from PIL import Image, ImageDraw, ImageFont
import io
from django.core.files.base import ContentFile
import os


class Command(BaseCommand):
    help = 'Generate and attach cover images to books'
    
    def create_book_cover(self, book):
        """Create a visually appealing book cover image"""
        # Create image
        width, height = 300, 400
        
        # Use a color based on category
        colors = {
            'Fiction': '#FF6B6B',
            'Non-Fiction': '#4ECDC4',
            'Mystery': '#45B7D1',
            'Science': '#FFA07A',
            'History': '#98D8C8',
            'Romance': '#F7DC6F',
            'Self-Help': '#BB8FCE',
            'Children': '#85C1E2',
            'Poetry': '#F8B88B',
            'Technology': '#52C0DE',
        }
        
        # Get category color or default
        category_name = book.category.name if book.category else 'Fiction'
        color_hex = colors.get(category_name, '#3498DB')
        # Convert hex to RGB
        color = tuple(int(color_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        
        img = Image.new('RGB', (width, height), color=color)
        draw = ImageDraw.Draw(img)
        
        # Try to use a nice font, fall back to default if not available
        try:
            title_font = ImageFont.truetype("arial.ttf", 24)
            author_font = ImageFont.truetype("arial.ttf", 16)
        except:
            title_font = ImageFont.load_default()
            author_font = ImageFont.load_default()
        
        # Add book title
        title_lines = self.wrap_text(book.title, 20)
        y_pos = 80
        for line in title_lines:
            draw.text((20, y_pos), line, fill='white', font=title_font)
            y_pos += 40
        
        # Add author name
        y_pos += 40
        draw.text((20, y_pos), "by", fill='white', font=author_font)
        draw.text((20, y_pos + 30), book.author, fill='rgba(255, 255, 255, 200)', font=author_font)
        
        # Add category at bottom
        draw.text((20, height - 50), book.category.name if book.category else 'Unknown', 
                 fill='white', font=author_font)
        
        # Save to bytes
        img_io = io.BytesIO()
        img.save(img_io, 'JPEG', quality=85)
        img_io.seek(0)
        
        return ContentFile(img_io.getvalue(), name=f'{book.title.replace(" ", "_")}.jpg')
    
    def wrap_text(self, text, max_chars):
        """Wrap text to fit on image"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            if len(' '.join(current_line)) > max_chars:
                current_line.pop()
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines[:3]  # Limit to 3 lines
    
    def handle(self, *args, **options):
        books = Book.objects.all()
        
        if not books.exists():
            self.stdout.write(self.style.WARNING('No books found in database'))
            return
        
        for book in books:
            # Skip if already has a custom image
            if book.cover_image and os.path.getsize(book.cover_image.path) > 5000:
                self.stdout.write(f'Skipping {book.title} - already has cover')
                continue
            
            # Generate and save cover
            try:
                cover = self.create_book_cover(book)
                book.cover_image = cover
                book.save()
                self.stdout.write(self.style.SUCCESS(f'✓ Generated cover for: {book.title}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Failed for {book.title}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS('Successfully generated book covers!'))

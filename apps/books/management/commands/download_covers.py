from django.core.management.base import BaseCommand
from apps.books.models import Book
import requests
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from urllib.parse import quote_plus


class Command(BaseCommand):
    help = 'Download real book covers from OpenLibrary and attach to books'
    
    def _download_image_bytes(self, url):
        """Download image bytes and reject tiny placeholder responses."""
        try:
            response = requests.get(
                url,
                timeout=20,
                headers={'User-Agent': 'Mozilla/5.0'},
            )

            if response.status_code != 200:
                return None

            content = response.content
            content_type = (response.headers.get('content-type') or '').lower()

            # OpenLibrary returns a 1x1 GIF placeholder for missing covers.
            if len(content) < 1000:
                return None

            if 'image' not in content_type and not content.startswith((b'\xff\xd8\xff', b'\x89PNG', b'GIF87a', b'GIF89a')):
                return None

            return content
        except Exception as e:
            self.stdout.write(f'Error downloading image from {url}: {str(e)}')
            return None

    def _download_with_retries(self, url, attempts=3):
        """Retry transient upstream errors when downloading image data."""
        for _ in range(attempts):
            image_bytes = self._download_image_bytes(url)
            if image_bytes:
                return image_bytes
        return None

    def download_cover_from_google_books(self, book):
        """Download cover image bytes from Google Books."""
        query_variants = [
            f'{book.title} {book.author}',
            book.title,
            book.isbn,
            f'intitle:"{book.title}"',
        ]

        for query in query_variants:
            try:
                response = requests.get(
                    'https://www.googleapis.com/books/v1/volumes',
                    params={'q': query, 'maxResults': 5},
                    timeout=20,
                    headers={'User-Agent': 'Mozilla/5.0'},
                )

                if response.status_code != 200:
                    continue

                for item in response.json().get('items', []):
                    image_links = item.get('volumeInfo', {}).get('imageLinks') or {}
                    candidate_urls = [
                        image_links.get('extraLarge'),
                        image_links.get('large'),
                        image_links.get('medium'),
                        image_links.get('thumbnail'),
                        image_links.get('smallThumbnail'),
                    ]

                    for candidate_url in candidate_urls:
                        if not candidate_url:
                            continue

                        # Prefer HTTPS and request the larger variant if the API gives us HTTP.
                        candidate_url = candidate_url.replace('http://', 'https://')
                        if 'zoom=1' in candidate_url:
                            candidate_url = candidate_url.replace('zoom=1', 'zoom=2')

                        cover_bytes = self._download_with_retries(candidate_url)
                        if cover_bytes:
                            return cover_bytes
            except Exception as e:
                self.stdout.write(f'Error querying Google Books for {book.title}: {str(e)}')

        return None

    def download_cover_from_openlibrary(self, book):
        """
        Download the best available book cover from OpenLibrary.

        This first searches by title and author so we can use real cover IDs
        (cover_i / cover_edition_key), then falls back to the ISBN endpoint.
        Returns bytes if successful, None otherwise.
        """
        try:
            search_url = 'https://openlibrary.org/search.json'
            search_response = requests.get(
                search_url,
                params={'title': book.title, 'author': book.author, 'limit': 10},
                timeout=20,
                headers={'User-Agent': 'Mozilla/5.0'},
            )

            candidate_urls = []

            if search_response.status_code == 200:
                for doc in search_response.json().get('docs', []):
                    cover_i = doc.get('cover_i')
                    cover_edition_key = doc.get('cover_edition_key')

                    if cover_i:
                        candidate_urls.append(f'https://covers.openlibrary.org/b/id/{cover_i}-L.jpg')

                    if cover_edition_key:
                        candidate_urls.append(f'https://covers.openlibrary.org/b/olid/{cover_edition_key}-L.jpg')

                    for isbn in doc.get('isbn', [])[:2]:
                        candidate_urls.append(f'https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg')

            # Fall back to the book's ISBN if search does not find anything.
            candidate_urls.append(f'https://covers.openlibrary.org/b/isbn/{book.isbn}-L.jpg')

            for url in candidate_urls:
                cover_bytes = self._download_image_bytes(url)
                if cover_bytes:
                    return cover_bytes

            # Google Books is a good secondary source when OpenLibrary has no cover.
            google_books_cover = self.download_cover_from_google_books(book)
            if google_books_cover:
                return google_books_cover

            return None
        except Exception as e:
            self.stdout.write(f'Error downloading cover for {book.title}: {str(e)}')
            return None
    
    def handle(self, *args, **options):
        books = Book.objects.all()
        
        if not books.exists():
            self.stdout.write(self.style.WARNING('No books found in database'))
            return
        
        success_count = 0
        failed_count = 0
        
        for book in books:
            self.stdout.write(f'Processing: {book.title}...')
            
            # Try to download a real cover from OpenLibrary search results first.
            cover_data = self.download_cover_from_openlibrary(book)
            
            if cover_data:
                try:
                    # Remove any existing cover so Django does not create a suffixed filename.
                    if book.cover_image:
                        default_storage.delete(book.cover_image.name)

                    filename = f"{book.title.replace(' ', '_').replace(':', '').replace('/', '_')}.jpg"
                    book.cover_image.save(filename, ContentFile(cover_data), save=True)
                    self.stdout.write(self.style.SUCCESS(f'✓ Downloaded cover for: {book.title}'))
                    success_count += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'✗ Failed to save cover for {book.title}: {str(e)}'))
                    failed_count += 1
            else:
                self.stdout.write(self.style.WARNING(f'⚠ No cover found for: {book.title} (ISBN: {book.isbn})'))
                failed_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'\nSummary: {success_count} successful, {failed_count} failed'))

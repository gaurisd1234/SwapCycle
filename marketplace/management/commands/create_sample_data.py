from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from marketplace.models import Category, Item
from django.core.files import File
from django.conf import settings
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates sample categories and items for the marketplace'

    def handle(self, *args, **kwargs):
        # Create a test user if it doesn't exist
        test_user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'testuser@example.com',
                'password': 'testpass123'
            }
        )
        if created:
            test_user.set_password('testpass123')
            test_user.save()
            self.stdout.write(self.style.SUCCESS(f'Created test user: {test_user.username}'))

        # Create categories
        categories_data = [
            {'name': 'Textbooks', 'slug': 'textbooks'},
            {'name': 'Electronics', 'slug': 'electronics'},
            {'name': 'Furniture', 'slug': 'furniture'},
            {'name': 'Clothing', 'slug': 'clothing'},
            {'name': 'School Supplies', 'slug': 'school-supplies'},
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(**cat_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))

        # Create sample items
        items_data = [
            {
                'title': 'Calculus Textbook',
                'description': 'Calculus: Early Transcendentals 8th Edition. Good condition, minimal highlighting.',
                'price': '599.00',
                'condition': 'good',
                'category': Category.objects.get(slug='textbooks'),
                'seller': test_user,
                'listing_type': 'sale',
            },
            {
                'title': 'Scientific Calculator',
                'description': 'TI-84 Plus graphing calculator. Perfect for math and science courses.',
                'price': '1499.00',
                'condition': 'like_new',
                'category': Category.objects.get(slug='electronics'),
                'seller': test_user,
                'listing_type': 'sale',
            },
            {
                'title': 'Desk Lamp',
                'description': 'LED desk lamp with adjustable brightness and color temperature.',
                'price': '799.00',
                'condition': 'new',
                'category': Category.objects.get(slug='furniture'),
                'seller': test_user,
                'listing_type': 'sale',
            },
            {
                'title': 'College Hoodie',
                'description': 'University hoodie, size L. Free to a good home!',
                'price': '0.00',
                'condition': 'good',
                'category': Category.objects.get(slug='clothing'),
                'seller': test_user,
                'listing_type': 'donation',
            },
            {
                'title': 'Notebook Set',
                'description': 'Set of 5 spiral notebooks, never used.',
                'price': '299.00',
                'condition': 'new',
                'category': Category.objects.get(slug='school-supplies'),
                'seller': test_user,
                'listing_type': 'sale',
            },
        ]

        # Create a placeholder image if it doesn't exist
        from PIL import Image
        import io

        # Create a simple colored image as placeholder
        placeholder_path = os.path.join(settings.MEDIA_ROOT, 'items', 'placeholder.jpg')
        os.makedirs(os.path.dirname(placeholder_path), exist_ok=True)
        
        if not os.path.exists(placeholder_path):
            # Create a 300x300 colored image
            img = Image.new('RGB', (300, 300), color='lightgray')
            img.save(placeholder_path, 'JPEG')

        # Create items
        for item_data in items_data:
            try:
                with open(placeholder_path, 'rb') as f:
                    item = Item.objects.create(**item_data)
                    item.image.save('placeholder.jpg', File(f), save=True)
                    self.stdout.write(self.style.SUCCESS(f'Created item: {item.title}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to create item {item_data["title"]}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Successfully created sample data'))
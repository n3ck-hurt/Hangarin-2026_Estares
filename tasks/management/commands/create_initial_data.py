from django.core.management.base import BaseCommand
from tasks.models import Category, Priority

class Command(BaseCommand):
    help = 'Create initial Priority and Category data manually'
    
    def handle(self, *args, **options):
        # Create Categories
        categories = [
            {'name': 'Work', 'description': 'Work-related tasks'},
            {'name': 'School', 'description': 'Academic tasks'},
            {'name': 'Personal', 'description': 'Personal tasks'},
            {'name': 'Finance', 'description': 'Financial tasks'},
            {'name': 'Projects', 'description': 'Project-related tasks'},
        ]
        
        for cat_data in categories:
            obj, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {cat_data["name"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'Category already exists: {cat_data["name"]}'))
        
        # Create Priorities
        priorities = [
            {'name': 'Critical', 'level': 5, 'color': '#DC2626'},
            {'name': 'High', 'level': 4, 'color': '#EA580C'},
            {'name': 'Medium', 'level': 3, 'color': '#CA8A04'},
            {'name': 'Low', 'level': 2, 'color': '#16A34A'},
            {'name': 'Optional', 'level': 1, 'color': '#6B7280'},
        ]
        
        for pri_data in priorities:
            obj, created = Priority.objects.get_or_create(
                name=pri_data['name'],
                defaults={'level': pri_data['level'], 'color': pri_data['color']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created priority: {pri_data["name"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'Priority already exists: {pri_data["name"]}'))
        
        self.stdout.write(self.style.SUCCESS('Initial data created successfully!'))
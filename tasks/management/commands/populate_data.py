from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random
from tasks.models import Priority, Category, Task, Note, SubTask

class Command(BaseCommand):
    help = 'Populates the database with fake data'

    def handle(self, *args, **options):
        fake = Faker()

        priorities_data = [
            {'name': 'critical', 'level': 5, 'color': '#FF0000'},
            {'name': 'high', 'level': 4, 'color': '#FF8000'},
            {'name': 'medium', 'level': 3, 'color': '#FFFF00'},
            {'name': 'low', 'level': 2, 'color': '#80FF00'},
            {'name': 'optional', 'level': 1, 'color': '#00FF00'},
        ]
        for p in priorities_data:
            Priority.objects.get_or_create(name=p['name'], defaults=p)

        categories_data = ['Work', 'School', 'Personal', 'Finance', 'Projects']
        for c in categories_data:
            Category.objects.get_or_create(name=c)

        priorities = list(Priority.objects.all())
        categories = list(Category.objects.all())
        statuses = ["Pending", "In Progress", "Completed"]

        for _ in range(20):
            task = Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                due_date=timezone.make_aware(fake.date_time_this_month()),
                status=fake.random_element(elements=statuses),
                category=fake.random_element(elements=categories),
                priority=fake.random_element(elements=priorities)
            )

            if fake.boolean(chance_of_getting_true=70):
                Note.objects.create(
                    task=task,
                    content=fake.paragraph(nb_sentences=5)
                )

            if fake.boolean(chance_of_getting_true=60):
                num_subtasks = fake.random_int(min=1, max=5)
                for _ in range(num_subtasks):
                    SubTask.objects.create(
                        task=task,
                        title=fake.sentence(nb_words=4),
                        status=fake.random_element(elements=statuses)
                    )

        self.stdout.write(
            self.style.SUCCESS('Successfully populated the database with fake data!')
        )
import os
import base64
from pathlib import Path

from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Create or clear sample content and lightweight placeholder files.'

    def add_arguments(self, parser):
        parser.add_argument('--create', action='store_true', help='Create sample content')
        parser.add_argument('--clear', action='store_true', help='Clear sample content')

    def handle(self, *args, **options):
        base = Path(settings.BASE_DIR)

        projects_dir = base / 'projects'
        blogs_dir = base / 'blogs'
        projects_dir.mkdir(exist_ok=True)
        blogs_dir.mkdir(exist_ok=True)

        # tiny 1x1 PNG (transparent)
        png_b64 = (
            'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAAWgmWQ0AAAAASUVORK5CYII='
        )
        png_data = base64.b64decode(png_b64)

        files = {
            projects_dir / 'placeholder1.png': png_data,
            projects_dir / 'placeholder2.png': png_data,
            blogs_dir / 'blog1.png': png_data,
        }

        if options['create']:
            for path, data in files.items():
                with open(path, 'wb') as f:
                    f.write(data)
            self.stdout.write(self.style.SUCCESS('Wrote placeholder files'))

            # create sample DB entries
            from django.contrib.auth.models import User
            from website.models import Service, Project, Blog, Testimonial

            user, _ = User.objects.get_or_create(username='sampleuser', defaults={'email': 'sample@example.com'})

            Service.objects.get_or_create(title='Sample Service 1', defaults={'description': 'Placeholder service 1'})
            Service.objects.get_or_create(title='Sample Service 2', defaults={'description': 'Placeholder service 2'})
            Service.objects.get_or_create(title='Sample Service 3', defaults={'description': 'Placeholder service 3'})

            p1, _ = Project.objects.get_or_create(title='Sample Project 1', defaults={'description': 'Demo project', 'technology': 'Django'})
            p2, _ = Project.objects.get_or_create(title='Sample Project 2', defaults={'description': 'Demo project 2', 'technology': 'Django'})

            # point image paths at created files (these are relative paths used by ImageField)
            p1.image = 'projects/placeholder1.png'
            p1.save()
            p2.image = 'projects/placeholder2.png'
            p2.save()

            b1, _ = Blog.objects.get_or_create(title='Sample Blog 1', defaults={'content': 'Demo blog post', 'author': user})
            b1.image = 'blogs/blog1.png'
            b1.save()

            Testimonial.objects.get_or_create(name='Sample Tester', defaults={'company': 'Example Co', 'message': 'Great work!'})

            self.stdout.write(self.style.SUCCESS('Sample DB entries created'))

        if options['clear']:
            # delete files
            for path in files.keys():
                try:
                    os.remove(path)
                except FileNotFoundError:
                    pass
            self.stdout.write(self.style.SUCCESS('Placeholder files removed'))

            # delete DB entries seeded by this command
            from website.models import Project, Blog, Service, Testimonial

            Project.objects.filter(title__startswith='Sample').delete()
            Blog.objects.filter(title__startswith='Sample').delete()
            Service.objects.filter(title__startswith='Sample Service').delete()
            Testimonial.objects.filter(name='Sample Tester').delete()

            self.stdout.write(self.style.SUCCESS('Sample DB entries cleared'))

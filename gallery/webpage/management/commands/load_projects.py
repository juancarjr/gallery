import json
from webpage.project_parser import get_projects, parse_projects, generate_tags
from webpage.models import Project, Tag, ProjectTag
from django.core.management.base import BaseCommand
from django.db.models import Count

class Command(BaseCommand):
    help = 'Populate database with project data'

    def handle(self, *args, **kwargs):
        # get project data
        html_data = get_projects(r'https://cs50.harvard.edu/x/2023/gallery/')
        project_data = generate_tags(parse_projects(html_data))

        # create projects
        for project in project_data:
            project_obj, created = Project.objects.get_or_create(
                title=project['title'],
                defaults={
                    'author': project['author'],
                    'description': project['description'],
                    'video': project['video'],
                    'thumbnail': project['thumbnail']
                }
            )
            if created:
                # create tags
                for tag_name in project['tags']:
                    tag_obj, created = Tag.objects.get_or_create(name=tag_name)

                    # tag count
                    if created:
                        tag_obj.count = 1
                    else:
                        tag_obj.count += 1
                    tag_obj.save()
                    
                    # create relationship between project and tag
                    ProjectTag.objects.get_or_create(project=project_obj, tag=tag_obj)
                    
                self.stdout.write(f"Created new project: {project['title']}")
            else:
                self.stdout.write(f"Project already exists: {project['title']}")
        
        self.stdout.write(self.style.SUCCESS('Database populated with project data with tag counts!'))

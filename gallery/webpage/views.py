from django.shortcuts import render
from .models import Project, Tag, ProjectTag, Favorite
from .filters import ProjectFilter
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import throttle_classes, api_view
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

import json

# Create your views here.

@api_view(['GET'])
@throttle_classes([UserRateThrottle, AnonRateThrottle])
def index(request):
    projects = []
    project_filter = ProjectFilter(request.GET, 
                                   queryset=Project.objects.all().distinct())

    PAGE_SIZE = 30
    page_num = request.GET.get('page', 1)
    page_obj = Paginator(project_filter.qs, PAGE_SIZE).get_page(page_num)

    # Retrieve tags for each project in the current page
    for element in page_obj:
        project_tags = ProjectTag.objects.filter(project=element)
        projects.append({'project': element, 'tags': project_tags})
    
    tags = Tag.objects.all()[:25]
    return render(request, 'index.html', {'projects': projects, 'tags': tags, 'filter': project_filter, 'page_obj': page_obj})

def autocomplete(request):
    query = request.GET.get('term', '')
    tags = Tag.objects.filter(name__icontains=query)[:10]
    # Format the results for the autocomplete widget    
    results = [{'label': f"{tag.name} ({tag.count})", 'value': tag.name} for tag in tags]
    data = json.dumps(results)
    mimetype = "application/json"
    return HttpResponse(data, mimetype)

def add_to_favorites(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, project=project)

    if created:
        return JsonResponse({'message': 'Project added to favorites', 'status': 'added'})
    else:
        return JsonResponse({'message': 'Project is already in your favorites', 'status': 'exists'})

def remove_from_favorites(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    favorite = Favorite.objects.get(user=request.user, project=project)
    favorite.delete()
    return JsonResponse({'message': 'Project removed from favorites', 'status': 'removed'})

def favorites(request):
    # Retrieve the user's favorite projects
    favorites = Favorite.objects.filter(user=request.user)
    favorite_projects = Favorite.objects.filter(user=request.user).values_list('project', flat=True)

    projects = []
    project_filter = ProjectFilter(request.GET, 
                                   queryset=Project.objects.filter(id__in=[favorite.project.id for favorite in favorites]).distinct())

    PAGE_SIZE = 30
    page_num = request.GET.get('page', 1)
    page_obj = Paginator(project_filter.qs, PAGE_SIZE).get_page(page_num)

    # Retrieve tags for each project in the current page
    for element in page_obj:
        project_tags = ProjectTag.objects.filter(project=element)
        projects.append({'project': element, 'tags': project_tags})

   
    tags = Tag.objects.filter(project__in=favorite_projects).distinct()[:25]

    return render(request, 'favorite.html', {'projects': projects, 'tags': tags, 'filter': project_filter, 'page_obj': page_obj})

def project(request, pk):
    project = Project.objects.get(id=pk)

    # Convert the YouTube video URL to an embed URL
    embed_url = project.video.replace('watch?v=', 'embed/')

    # Get the tags for the project
    project_tags = ProjectTag.objects.filter(project=project)

    # Extract the tag names from the project tags
    tag_names = [pt.tag.name for pt in project_tags]

    return render(request, 'project.html', {'project': project, 'tags': tag_names , 'embed_url': embed_url,})
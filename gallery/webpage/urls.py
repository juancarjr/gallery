from webpage import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('project/<int:pk>', views.project, name='project'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('add_to_favorites/<int:project_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/<int:project_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('favorites/', views.favorites, name='favorites'),

]
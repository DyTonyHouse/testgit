from django.urls import path,re_path
from . import views
urlpatterns = [
    path(r'', views.index, name='table_index'),
    # re_path(r'(\w+)/(\w+)/$', views.display_table, name='table_obj'),
    path(r'<app_name>/<table_name>/', views.display_table, name='table_obj'),
    re_path(r'(\w+)/(\w+)/(\d+)/change/$', views.table_obj_change, name='table_obj_change'),
    re_path(r'(\w+)/(\w+)/add/$', views.table_obj_add, name='table_obj_add'),
    re_path(r'(\w+)/(\w+)/(\d+)/delete/$', views.table_obj_delete, name='table_obj_delete'),
]
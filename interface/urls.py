from django.conf.urls import url
from django.views.generic.base import TemplateView
from . import views

urlpatterns=[
    url(r'^home',TemplateView.as_view(template_name='index.html'),name='index'),
    url(r'^python/$',views.exe,name='exe'),
]

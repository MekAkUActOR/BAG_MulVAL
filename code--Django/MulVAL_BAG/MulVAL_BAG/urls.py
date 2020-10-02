"""MulVAL_BAG URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mulvala2b import views
from django.views import static
from django.conf import settings
from django.conf.urls import url

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('mulval/window/', views.window),
    path('mulval/mulval/', views.mulval),
    path('mulval/download/', views.download),
    path('mulval/a2b/', views.a2b),
    path('mulval/mulvalerror1/', views.mulvalerror1),
    path('mulval/mulvalsuccess/', views.mulvalsuccess),
    path('mulval/mulvalerror2/', views.mulvalerror2),
    path('mulval/a2berror/', views.a2berror),
    url(r'^static/(?P<path>.*)$', static.serve,{'document_root': settings.STATIC_ROOT}, name='static'),
]
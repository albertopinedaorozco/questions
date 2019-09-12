"""preguntamoss URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from question.views import probar
from question import urls as question_urls
from people import urls as people_urls
from blog import urls as blog_urls

#from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^login/$', auth_views.login, name='login'),
    ##comentariado url(r'^logout/$', auth_views.logout, name='logout'),
    #url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),


    url(r'^', include(question_urls)),
    url(r'^', include(people_urls)),
    url(r'^', include(blog_urls)),

]

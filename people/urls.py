from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from .views import getColaboradorDetail, ColaboradorCreate, ColaboradorList, profile,edit_profile,change_password

from django.contrib.auth.views import login,logout

urlpatterns = [
url(r'^people/(?P<id>\d+)/$', getColaboradorDetail, name='people_detail_colaborador'),
url(r'^colaborador/create/$', ColaboradorCreate.as_view(), name='people_colaborador_create'),
url(r'^colaborador/list/$',ColaboradorList, name='people_colaborador_list'),
url(r'^login/$', login, {'template_name':'people/login.html'}, name='login'),
url(r'^logout/$', logout, {'template_name':'people/logout.html'}, name='logout'),
url(r'^profile/$', profile,  name='profile'),
url(r'^profile/edit/$', edit_profile,  name='edit_profile'),
url(r'^profile/password/$', change_password,  name='change_password'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
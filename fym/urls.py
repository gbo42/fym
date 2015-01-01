from django.conf.urls import patterns, url
from fym import views
from django.conf import settings
from django.conf.urls.static import static

if not settings.DEBUG:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name = 'about'),
    #url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^trilha/(?P<trilha_slug>[\w\-]+)/$', views.trilha, name='trilha'),
    url(r'^trilha/(?P<trilha_slug>[\w\-]+)/add_bloco/$', views.add_bloco, name='add_bloco'),
    url(r'^add_trilha/$', views.add_trilha, name='add_trilha'),
    url(r'^signup/$', views.signup, name='signup'),
    )

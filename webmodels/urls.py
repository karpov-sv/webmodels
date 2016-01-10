from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url
#from django.contrib import admin

import settings

import views

urlpatterns = patterns('',
                       url(r'^/?$', views.index, name="index"),

                       url(r'^models/?$', views.models_list, name="models_list"),
                       url(r'^models/(?P<id>\d+)/?$', views.model_details, name="model_details"),

                       url(r'^models/(?P<id>\d+)/plot/select/?$', views.model_plot_select, name="model_plot_select"),
                       url(r'^models/(?P<id>\d+)/plot/(?P<mode>\w+)/?$', views.model_plot, {'size':800}, name="model_plot"),
                       url(r'^models/(?P<id>\d+)/plot/(?P<mode>\w+)/(?P<lmin>.+)/(?P<lmax>.+)/?$', views.model_plot, {'size':800}, name="model_plot_limits"),

                       # Robots
                       url(r'^robots.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", content_type="text/plain")),
)

urlpatterns += staticfiles_urlpatterns()

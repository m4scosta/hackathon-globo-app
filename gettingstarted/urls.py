from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import hello.views
import grade_parser.views

urlpatterns = patterns('',
    url(r'^$', hello.views.index, name='index'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^fetch_api/$', grade_parser.views.fetch_api, name='fetch_api'),
    url(r'^generate_features_vec/$', grade_parser.views.generate_features_vec, name='generate_features_vec'),
    url(r'^get_features_vec/$', grade_parser.views.get_features_vec, name='get_features_vec'),
)

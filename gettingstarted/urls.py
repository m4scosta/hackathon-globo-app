from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import hello.views
import grade_parser.views
import recommendations.views

urlpatterns = patterns('',
    url(r'^$', hello.views.index, name='index'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^fetch_api/$', grade_parser.views.fetch_api, name='fetch_api'),
    url(r'^set_keywords/$', grade_parser.views.set_keywords, name='set_keywords'),
    url(r'^get_keywords/$', grade_parser.views.get_keywords, name='get_keywords'),
    url(r'^create_user_preferences/(?P<fb_id>\d+)/$', recommendations.views.create_user_preferences, name='create_user_preferences'),
)

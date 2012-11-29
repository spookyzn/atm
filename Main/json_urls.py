from django.conf.urls.defaults import *

urlpatterns = patterns('Main.json_views',
    url(r'^daily_count/', 'daily_count'),
)
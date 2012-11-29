from django.conf.urls import patterns, include, url
import ATM.settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ATM.views.home', name='home'),
    # url(r'^ATM/', include('ATM.foo.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^resources/(?P<path>.*)$', 'django.views.static.serve', {'document_root': ATM.settings.RESOURCE_DIR}),
    url(r'^json/', include('Main.json_urls'))
)

urlpatterns += patterns('Main.views',
    url(r'^$', 'index')
)
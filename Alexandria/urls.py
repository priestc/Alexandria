from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('Alexandria.views',
    url(r'^admin/', include(admin.site.urls)),
    url(r'dialog', 'publish_dialog'),
    url(r'api/publish', 'publish'),
    url(r'api/query`', 'query'),
    url(r'api/request_authorization', 'request_authorization'),
    url(r'api/append_transfer_query', 'append_transfer_query'),
)

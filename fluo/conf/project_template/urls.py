# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

if settings.DEBUG:
    urlpatterns = patterns('',
        (r'^%s/(?P<path>.*)$' % settings.MEDIA_URL[1:-1], 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT, }),
    )
else:
    urlpatterns = patterns('')

urlpatterns += patterns('',
    # Example:
    # (r'^{{ project_name }}/', include('{{ project_name }}.foo.urls')),

    # uncomment to enable i18n
    #(r'^i18n/', include('django.conf.urls.i18n')),
    #url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', name='jsi18n'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)


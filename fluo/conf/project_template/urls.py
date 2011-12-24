# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import url, include, patterns
# Uncomment to enable i18n urls
#from django.conf.urls.i18n import i18n_patterns

# Comment the next two lines to disable the admin:
import {{ project_name }}.admin
from fluo import admin

# Uncomment the next lines to enable custom handlers:
#from django.conf.urls import handler403, handler404, handler500
#handler403 = '{{ project_name }}.views.handler403'
#handler404 = '{{ project_name }}.views.handler404'
#handler500 = '{{ project_name }}.views.handler500'

from fluo.views import TemplateView
from fluo.urls import Urls, MediaUrls

class {{ ProjectName }}Urls(Urls):
    def get_urls(self):
        urlpatterns = patterns('',
            # Example:
            #url(r'^{{ project_name }}/', include('{{ project_name }}.foo.urls')),
            url(r'^robots.txt', TemplateView(
                template_name='robots.txt',
                mimetype='text/plain',
            )),
            url(r'^crossdomain.xml$', TemplateView(
                template_name='crossdomain.xml',
                mimetype='application/xml',
            )),

            # Comment to disable i18n
            url(r'^i18n/', include('django.conf.urls.i18n')),
            url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', name='jsi18n'),

            # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
            # to INSTALLED_APPS to enable admin documentation:
            #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

            # Comment the next line to disable the admin:
            url(r'^admin/', include(admin.site.urls)),
        ) + MediaUrls().urls

        # Uncomment to enable i18n urls
        #urlpatterns += i18n_urlpatterns(''
            #url(r'^{{ project_name }}/', include('{{ project_name }}.foo.urls')),
        #)

        return urlpatterns

urlpatterns = {{ ProjectName }}Urls().urls


from django.conf.urls import patterns, include, url
from cm.view import HomeView
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', HomeView.as_view(), name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^css/(?P<path>.*)$','django.views.static.serve', {'document_root':settings.STATICFILES_CSS_DIRS, 'show_indexes': True}),
    url(r'^js/(?P<path>.*)$','django.views.static.serve', {'document_root':settings.STATICFILES_JS_DIRS, 'show_indexes': True}),
    url(r'^admin/', include(admin.site.urls)),
)

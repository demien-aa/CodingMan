from django.conf.urls import patterns, include, url
from web.views import HomeView

import pdb; pdb.set_trace()
urlpatterns = patterns('',
    # Examples:
    url(r'^home/', HomeView.as_view(), name='home'),
)

from django.conf.urls import include, url
from django.contrib import admin

from . import views

from django.views.generic import View

urlpatterns = [
    # Examples:
    # url(r'^$', 'control.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.Index.as_view()),
    url(r'^test$', views.test.as_view()),
    url(r'^plot$', views.plot.as_view()),
    url(r'^drag$', views.drag.as_view()),
    url(r'^newindex', views.newindex.as_view()),
    url(r'^demodul', views.demodul.as_view()),
    url(r'^analysis', views.analysis.as_view()),
    url(r'^addmodal', views.addmodal.as_view()),
    url(r'^addModalDemodul', views.addmodalDemodul.as_view()),
    url(r'^addModalType', views.addmodalType.as_view()),
    url(r'^modu/', include('control.apps.modu.urls')),
    url(r'^demod/', include('control.apps.demod.urls')),
    # url(r'^account/', include('account.urls')),
]

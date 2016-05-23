from django.conf.urls import include, url

from . import views as modu_view

urlpatterns = [
    url(r'createsignal$', modu_view.CreateSignal.as_view()),
    # url(r'describe$', modu_view.DescribeSignal.as_view()),
    # url(r'delete$', modu_view.DeleteSignal.as_view()),
    # url(r'get$', modu_view.GetSignal.as_view()),


]
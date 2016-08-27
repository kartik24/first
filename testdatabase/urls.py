from django.conf.urls import  include, url
from contact import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^pathlab/', views.GetPathlab.as_view()),
    url(r'^pathlabinfo/', views.GetPathlabInfo.as_view()),
    url(r'^addpathlab/$', views.RegisterPathlab.as_view()),
    url(r'^addpathlabinfo/$', views.RegisterPathlabInfo.as_view()),

    url(r'^admin/', include(admin.site.urls)),

]

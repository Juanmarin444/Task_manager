from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register', views.register),
    url(r'^login', views.login),
    url(r'^show$', views.show),
    url(r'^logout', views.logout),
    url(r'^add/appointment', views.add_appt),
    url(r'^edit/(?P<appt_id>\d+)', views.edit),
    url(r'^update/(?P<appt_id>\d+)', views.update),
    url(r'^delete/(?P<appt_id>\d+)', views.delete)
]

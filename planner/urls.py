from django.conf.urls import patterns, url

from planner import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^assignments/$', views.assignments, name='assignments'),
    url(r'^assignments/(?P<assignment_id>[0-9]+)/$', views.assignment_detail, name='assignments'),
    url(r'^courses/$', views.courses, name='courses'),
    #url(r'^logout/$', views.logout_user, name='logout_user')

)
from django.conf.urls import patterns, url

from planda import views

urlpatterns = patterns('',
    # universal patterns
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^preferences/$', views.preferences, name='preferences'),
    url(r'^create/$', views.create_account, name='create_account'),

    # assignment patterns
    url(r'^assignments/$', views.assignments, name='assignments'),
    url(r'^assignments/(?P<assignment_id>[0-9]+)/$', views.assignment_detail, name='assignments'),
    url(r'^assignments/(?P<assignment_id>[0-9]+)/toggle_completed/$', views.assignment_toggle_completed, name='assignment_toggle_completed'),
    url(r'^assignments/delete/(?P<assignment_id>[0-9]+)/$', views.assignment_delete, name='assignment_delete'),
    url(r'^assignments/edit/$', views.assignment_edit, name='assignment_edit'),
    url(r'^assignments/add/$', views.assignment_add, name='assignment_add'),

    # course patterns
    url(r'^courses/$', views.courses, name='courses'),
    url(r'^courses/(?P<course_id>[0-9]+)/$', views.course_detail, name='course_detail'),
    url(r'^courses/edit/$', views.course_edit, name='course_edit'),
    url(r'^courses/delete/(?P<course_id>[0-9]+)/$', views.course_delete, name='course_delete'),
    url(r'^courses/add/$', views.course_add, name='course_add'),

)
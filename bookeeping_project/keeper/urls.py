from django.conf.urls import patterns, url

from keeper import views


urlpatterns=patterns('', 
		url(r'^$', views.user_login, name='user_login'),
		url(r'^register/$', views.register, name='register'),
		url(r'^logout/$', views.user_logout, name='logout'),
		url(r'^dashboard/$', views.dashboard, name='dashboard'),
		url(r'^addProject/$', views.addProject, name='addProject'),
		url(r'^success.html/', views.success, name='success'),
		url(r'^addContractor/', views.addContractor, name='addContractor_unhired'),
		url(r'^project/(?P<project_name_slug>[\w\-]+)/$', views.project_details, name='project_details'),	
		url(r'^contractor/(?P<contractor_name_slug>[\w\-]+)/$', views.contractor_details, name='contractor_details'),
		url(r'^update_contractor/(?P<project_slug>[\w\-]+)/$', views.update_contractor, name='update_contractor'),
		




	)
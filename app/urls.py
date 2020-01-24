from django.conf.urls import url
from app import views


urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    # url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^user_login/$', views.UserLogin.as_view(), name='user_login'),
    url(r'^dashboard/$', views.Dashboard.as_view(), name='dashboard'),

]

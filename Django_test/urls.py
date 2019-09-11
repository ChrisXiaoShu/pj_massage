"""Django_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from test_app.views import post_reservation, get_reservation, delete_reservation, get_freetime, get_customer, post_customer, get_group

urlpatterns = [
    path('admin/', admin.site.urls),
    #url(r'^reservation_sample/post/(?P<m_id>[0-9]+)/(?P<c_id>[0-9]+)/(?P<d>[0-9]{10})/(?P<name>c[\w]+)/(?P<phone>[\w]+)$', make_r_s),
    #url(r'^reservation_sample/get/(?P<lineid>[0-9]+)$', get_r_s),
    #url(r'^reservation/post/(?P<mid>[0-9]+)/(?P<dt>[0-9]+)$', post_reservation, name='post_reservation'), #lineid name phone #{status : 'success or fail', order name phone date}
    url(r'^reservation/post/$', post_reservation, name='post_reservation'), #line_id name phone #{status : 'success or fail', order name phone date}
    url(r'^reservation/get/$', get_reservation, name='get_reservation'), #?line_id=line_id
    url(r'^reservation/delete/$', delete_reservation, name='delete_reservation'),
    url(r'^freetime/get/$', get_freetime, name='get_freetime'), #?gid=gid
    url((r'^customer/get/$', get_customer, name='get_customer'), #?line_id=line_id
    url((r'^customer/post/$', post_customer, name='post_customer'), #?line_id=line_id
    url((r'^group/get/$', get_group, name='get_group')        
]

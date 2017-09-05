from django.conf.urls import url
from blog import views

urlpatterns = [
	
	url(r'^$',views.ApiRoot.as_view(),name=views.ApiRoot.name),

	url(r'^users/$',views.UserList.as_view(),name=views.UserList.name),
	url(r'^users/(?P<pk>\d+)/$',views.UserDetail.as_view(),name=views.UserDetail.name),

	url(r'^profiles/$',views.ProfileList.as_view(),name=views.ProfileList.name),
	url(r'^profiles/(?P<pk>\d+)/$',views.ProfileDetail.as_view(),name=views.ProfileDetail.name),

	url(r'^posts/$',views.PostList.as_view(),name=views.PostList.name),
	url(r'^posts/(?P<pk>\d+)/$',views.PostDetail.as_view(),name=views.PostDetail.name),

	url(r'^comments/$',views.CommentList.as_view(),name=views.CommentList.name),
	url(r'^comments/(?P<pk>\d+)/$',views.CommentDetail.as_view(),name=views.CommentDetail.name),


]

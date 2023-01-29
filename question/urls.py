from django.urls import path
from question import views

urlpatterns = [
	path('',views.Question_list, name='home'),
	path('question/views',views.Question_list_views, name='home_views'),
	path('question/create/', views.Question_create,name='create'),
	path('question/<int:id>/<str:url>/', views.Question_detail,name='detail'),
	path('question/update/<int:id>/<str:url>/', views.Question_update,name='update'),
	path('question/delete/<int:id>/<str:url>/', views.Question_delete,name='delete'),
	path('question/ansupdate/<int:id>/', views.Answer_update,name='ans_update'),
	path('question/ansdelete/<int:id>)/', views.Answer_delete,name='ans_delete'),
	path('question/ansaccept/<int:id>)/', views.Answer_accept,name='accept'),
	path('question/ansunaccept/<int:id>/', views.Answer_unaccept,name='unaccept'),
	path('question/upvote/<int:id>/', views.vote_up,name='up'),
	path('question/downvote/<int:id>/', views.vote_down,name='down'),
	]

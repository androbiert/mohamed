from django.urls import path,include
from . import views
app_name ='polls' 

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/',views.details, name="details"),
    path('<int:question_id>/results/',views.results,name='results'),
    path("<int:question_id>/votes/", views.votes , name="votes"),
    path("<int:question_id>/delete/", views.delete_question , name="delete_question"),
    
]

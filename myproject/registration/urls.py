from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('success/', views.success, name='success'),
    path('upload_question/', views.upload_question, name='upload_question'),
    path('view_submissions/', views.view_submissions, name='view_submissions'),
    path('grade_submission/<int:submission_id>/', views.grade_submission, name='grade_submission'),
    path('questions/', views.question_list, name='question_list'),
    path('submit_answer/', views.submit_answer, name='submit_answer'),
    path('view_grades/', views.view_grades, name='view_grades'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('logged-out/', views.logged_out_view, name='logged_out'),
    path('admin_base/', views.admin_base, name='admin_base'),
    path('user_base/', views.user_base, name='user_base'),
]

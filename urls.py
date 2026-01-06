from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'students',views.StudentViewSet, basename='student')

urlpatterns = [
    path('',views.show_students,name='show_students'),
    path('add/',views.add_student,name='add_student'),
    path('edit/<int:id>/',views.edit_student,name='edit_student'),
    path('delete/<int:id>/',views.delete_student,name='delete_student'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('accounts/login/', views.login_view,name='login'),
    #API
    path('api/',include(router.urls)),
]

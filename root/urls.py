from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('home', views.home, name = "adminHomePage"),
    path('assign', views.assign, name = "assign"),
    path('update_assign/<int:pk>',views.update_assign,name="update-assign"),
    path('delete_assign/<int:pk>',views.delete_assign,name="delete-assign"),
    path('teacherLogin/', views.teacherLogin, name = "teacherlogin"),
  

]
if settings.DEBUG:
    urlpatterns += static(settings. MEDIA_URL, document_root = settings.MEDIA_ROOT)
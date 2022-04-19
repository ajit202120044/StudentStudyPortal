from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.home,name = "home"),
    path('home',views.home,name = "home"),
    path('login/', views.loginPage, name="login"),
    #notes

    path('notes',views.notes, name = "notes"),
    path('delete_note/<int:pk>',views.delete_note, name = "delete-notes"),
    path('notes_detail/<int:pk>',views.NotesDetailView.as_view(), name = "notes-detail"),


    
#homework


    path('homework',views.homework,name="homework"),
    path('update_homework/<int:pk>',views.update_homework,name="update-homework"),
    path('delete_homework/<int:pk>',views.delete_homework,name="delete-homework"),
 #youtube

    path('youtube',views.youtube,name="youtube"),

 # todo

    path('todo',views.todo,name="todo"),
    path('update_todo/<int:pk>',views.update_todo,name="update-todo"),
    path('delete_todo/<int:pk>',views.delete_todo,name="delete-todo"),


    #books
    path('book',views.book,name="book"),

    #dictionary
    path('dictionary',views.dictionary,name="dictionary"),


    #wikipedia
     path('wiki',views.wiki,name="wiki"),



    #conversion
    path('conversion',views.conversion,name="conversion"),
    

    


]
if settings.DEBUG:
    urlpatterns += static(settings. MEDIA_URL, document_root = settings.MEDIA_ROOT)
    
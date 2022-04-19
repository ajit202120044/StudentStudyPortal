from django.shortcuts import render
from . forms import *
from root.models import Assignment
from django.contrib import messages
from django.views import generic
from django.shortcuts import redirect
# from django.utils.datastructures import MultiValueDictKeyError
from youtubesearchpython import VideosSearch
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login , logout
import requests
import wikipedia
# import wikipedia

# Create your views here.
def home(request):
    return render(request,'dashboard/home.html')
@login_required
def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if  form.is_valid():
            notes = Notes(user= request.user,title = request.POST['title'], description = request.POST['description'])
            notes.save()
        messages.success(request,f"Notes Added from {request.user.username} Successfully")
        # messages.success(request, 'Profile details updated.')
    else:

        form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
  
    return render(request, 'dashboard/note.html', {'notes': notes,'form':form})
#deleting notes
@login_required
def delete_note(request,pk=None):
    Notes.objects.get(id = pk).delete()
    return redirect("notes")

class NotesDetailView(generic.DetailView):
    model = Notes    

    # homework

@login_required
def homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
          
            homeworks = Homework(
                    user = request.user,
                    subject = request.POST['subject'],
                    title = request.POST['title'],
                    description = request.POST['description'],
                    due = request.POST['due'],
                    is_finished = finished
              
            )    
            homeworks.save()
            messages.success(request,f"homework Added from {request.user.username} Successfully")  
    else:
        form = HomeworkForm()
    homework = Homework.objects.filter(user=request.user)

    homework_by_teacher = Assignment.objects.all()


    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
        
    return render(request,'dashboard/homework.html', {'homeworks':homework, 'homework_done': homework_done,'form':form, 'homeworkbyteacher' : homework_by_teacher })

# upadting homework
@login_required
def update_homework(request,pk = None):
    homework = Homework.objects.get(id =pk)
    if homework.is_finished == True:
        homework.is_finished =False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')

'''
def assignent:
    all_assignment = Assignment.objects.all();
    return redirect('Allassignent'{allAssign: all_assignment})
'''

# delete homework
@login_required
def delete_homework(request,pk= None):
     Homework.objects.get(id =pk).delete()
     return redirect("homework")


#youtube section 


def youtube(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video= VideosSearch(text,limit=20)
        result_list = []
        for i in video.result()['result']:

            result_dict ={
                'input':text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime']
            }
            desc = ''
            if  i['descriptionSnippet']:
                for  j in i['descriptionSnippet']:
                    desc  += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
        return render(request,'dashboard/youtube.html',{'form': form,'results':result_list})
      
    else:
        form = DashboardForm()
    return render(request,'dashboard/youtube.html',{'form': form})


    # todo 
@login_required
def todo (request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if  form .is_valid():
            try:
                finished = request.POST["is_finished"]
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = Todo(
                user = request.user,
                title = request.POST['title'],
                is_finished = finished
            ) 
            todos.save()
            messages.success(request,f"Todo added from {request.user.username}!!")
    else:
        form = TodoForm()
    todo =Todo.objects.filter(user=request.user)
    if len(todo)== 0:
        todo_done = True
    else:
        todo_done = False


    return render (request,"dashboard/todo.html", {'todos':todo,'form':form,'todo_done':todo_done})


    #update todo
@login_required
def update_todo(request,pk= None):
    todo = Todo.objects.get(id =pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('todo')
@login_required
def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')



    #books


def book(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict ={
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink'),
                'author':answer['items'][i]['volumeInfo']['authors'][0],
                'publishdate':answer['items'][i]['volumeInfo'].get('publishDate'),
                'publisher':answer['items'][i]['volumeInfo'].get('publisher')

               
            }

            
            result_list.append(result_dict)
        return render(request,'dashboard/books.html',{'form': form,'results':result_list})
      
    else:
        form = DashboardForm()
    return render(request,'dashboard/books.html',{'form': form})
 

  # dictionar


def dictionary(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                    
                    'form': form,
                    'input':text,
                    'phonetics':phonetics,
                    'audio':audio,
                    'definition':definition,
                    'example':example,
                    'synonyms':synonyms

            }
        except:
            context = {
                'form': form,
                'input':''
            }
        return render(request,"dashboard/dictionary.html",context)
    else:

        form = DashboardForm()
    return render (request,"dashboard/dictionary.html",{'form':form})


#wikipedia
def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = DashboardForm(request.POST)
        search = wikipedia.page(text)
        
        context = {
                'form':form,
                'title':search.title,
                'link':search.url,
                'details':search.summary


        }
        return render (request,"dashboard/wiki.html",context)
    else:
        form = DashboardForm()
    return render (request, "dashboard/wiki.html",{'form':form})


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username = username , password = password)
        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect('/manage/home') 
            else:
                return redirect('home')
        else:
            return redirect('login')
    context ={

    }
    return render (request,"dashboard/login.html",context)

# conversion
@login_required
def conversion(request):
    if request.method == 'POST':
        form = ConversionForm(request.POST)
        if request.POST['measurement'] == 'length':
            measurement_form = ConversionLengthForm()
            context = {
                'form': form,
                'm_form': measurement_form,
                'input': True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int (input)>= 0:
                    if  first == 'yard' and second == 'foot':
                        answer = f"{input} yard = {int(input)*3} foot"
                    if  first == 'foot' and second == 'yard':
                        answer = f"{input} foot = {int(input)/3} yard"
                context = {
                        'form':form,
                        'm_form':measurement_form,
                        'input':True,
                        'answer':answer

                }
       
        if request.POST['measurement'] == 'mass':
            measurement_form = ConversionMassForm()
            context = {
                'form': form,
                'm_form': measurement_form,
                'input': True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int (input)>= 0:
                    if  first == 'pound' and second == 'kilogram':
                        answer = f"{input} pound = {int(input)*0.453592} kilogram"
                    if  first == 'kilogram' and second == 'pound':
                        answer = f"{input} kilogram = {int(input)*2.20462} pound"
                context = {
                        'form':form,
                        'm_form':measurement_form,
                        'input':True,
                        'answer':answer

                }
    else:

        form = ConversionForm()
        context = {
            'form':form,
            'input':False
        }

    return render (request, "dashboard/conversion.html",context)






#registartion
def register(request):
    if request.method  == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username =form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
       
            messages.success(request,f" Congratulations!! Account Created for {username}!!!")
            #redirect to login
            return redirect("login")
    else:
        form = UserRegistrationForm()
    return render(request,"dashboard/register.html",{'form':form})






    #profile
@login_required
def profile(request):
    homeworks = Homework.objects.filter(is_finished= False, user = request.user)
    todos = Todo.objects.filter(is_finished= False, user = request.user)
    if len(homeworks)== 0:
        homework_done = True
    else:
        homework_done = False

    if len(todos)== 0:
        todo_done = True
    else:
        todo_done = False

    return render(request,"dashboard/profile.html",{'homeworks':homeworks,
    'todos':todos,
    'homework_done':homework_done,
    'todo_done':todo_done})

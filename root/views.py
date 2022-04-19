from django.shortcuts import render, redirect
from root.models import Assignment
from django.contrib.auth.models import auth, User
from . form import AssignmentForm
from django.contrib import messages




def home(request):
    if request.user.is_superuser:
        return render(request, 'adminHome.html')
    else:
        return render(request, '404.html')

def assign(request):
    if request.user.is_superuser:
        if request.method == "POST":
            form = AssignmentForm(request.POST)
            if form.is_valid():
                assigns = Assignment(
                            user = request.user,
                            subject = request.POST['subject'],
                            title = request.POST['title'],
                            description = request.POST['description'],
                            due = request.POST['due'],
                            marks = request.POST['marks'],
                    )

                assigns.save()
                messages.success(request,f" assignment Added from {request.user.username} Successfully")

        else:
            form = AssignmentForm()
        assign = Assignment.objects.filter(user=request.user)
    

    
        if len(assign) == 0:
            assign_done = True
        else:
            assign_done = False
        
        
        return render(request,'assign.html', {'assigns':assign, 'form':form,'assign_done' : assign_done})
    else:
        return render(request, '404.html')



def delete_assign(request,pk= None):
     Assignment.objects.get(id =pk).delete()
     return redirect("assign")

def update_assign(request,pk = None):
    assign = Homework.objects.get(id =pk)
    if assign.is_finished == True:
        assign.is_finished =False
    else:
        assign.is_finished = True
    assign.save()
    return redirect('assign')


def teacherLogin(request):
    if request.user.is_superuser:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request,username = username , password = password)
            if user is not None:
                login(request, user)
                if request.user.is_superuser:
                    return redirect('home') 
                else:
                    return redirect('home')
            else:
                return redirect('teacherLogin')
        context ={

        }
        return render (request,"teacher_login.html",context)
    else:
        return render(request, "teacher_login.html")


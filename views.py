from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Student
from .forms import StudentForm 

#------web views(CRUD)-------
@login_required
def show_students(request):
    query = request.GET.get('q')
    if query:
        students = Student.objects.filter(Q(name__icontains=query)| Q(city__icontains=query))
    else:
        students = Student.objects.all()

    paginator = Paginator(students, 5)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    return render(request,'studentapp/show_students.html',{'page_obj':page_obj, 'query': query})

@login_required 
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Student added sucessfully.")
            return redirect('home')
        else:
            messages.error(request,"Please fix the errors below.")
    else:
        form = StudentForm()
    return render(request,'studentapp/add_student.html',{'form': form})
      
@login_required
def edit_student(request, id):
    student = get_object_or_404(Student,id=id)
    form = StudentForm(request.POST or None, instance=student)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request,"Student updated.")
        return redirect('show_students')
    return render(request,'studentapp/edit_student.html',{'form': form})

@login_required
def delete_student(request, id):
    student = get_object_or_404(Student,id=id)
    if request.method == "POST":
        student.delete()
        messages.success(request,"Student deleted.")
        return redirect('show_students')
    return render(request,'studentapp/delete_student.html',{'student':student})

#------Auth views---------
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Account created. you can log in.")
            return redirect('login')
        else:
            messages.error(request,"please correct the error below")
    else:
        form = UserCreationForm()
    return render(request,'studentapp/signup.html',{'form': form})
   

def login_view(request):
    if request.user.is_authenticated:
        return redirect('show_students')
    if request.method == 'POST':
        username = request.POST.get('username','').strip()
        password = request.POST.get('password','')
        user = authenticate(request, username=username,password=password)
    
        if user is not None:
            login(request, user)
            messages.success(request,f"Welcome, {user.username}!")
            return redirect('show_students')
        else:
            messages.error(request,"Invalid username or password.")
    return render(request,'studentapp/login.html')
   
def logout_view(request):
    logout(request)
    messages.info(request,"you have been logged out.")
    return redirect('login')





from rest_framework import viewsets
from .serializers import StudentSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
                                       







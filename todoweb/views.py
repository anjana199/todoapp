
from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView,CreateView,FormView,ListView,DetailView
from todoweb.forms import UserRegistrationForm,LoginForm,TodoForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from api.models import ToDosn
from django.utils.decorators import method_decorator
from django.contrib import messages


def signin_required(fn):
    def wrapper(request,*args,**kw):
        if not request.user.is_authenticated:
            messages.error(request,"you must login first")
            return redirect("signin")
        else:
            return fn(request,*args,**kw)
    return wrapper            

from django.urls import reverse_lazy
class RegisterView(CreateView):
    template_name="register.html"
    form_class=UserRegistrationForm
    model=User
    success_url=reverse_lazy("signin")


    # def get(self,request,*args,**kw):
    #     form=UserRegistrationForm()
    #     return render(request,"register.html",{"form":form})


    # def post(self,request,*args,**kw):
    #     form=UserRegistrationForm(request.POST)
    #     if form.is_valid():
    #         User.objects.create_user(**form.cleaned_data)
    #         messages.success(request,"Your account create successfully")
    #         return redirect("signup")
    #     else:
    #         messages.error(request,"registartion failed")
    #         return render(request,"register.html",{"form":form})        


class LoginView(FormView):
    template_name="login.html"
    form_class=LoginForm
    
    # def get(self,request,*args,**kw):
    #     form=LoginForm()
    #     return render(request,"login.html",{"form":form})          

    def post(self,request,*args,**kw):
        form=LoginForm(request.POST)

        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pswd=form.cleaned_data.get("password")
            print(uname,pswd)
            usr=authenticate(request,username=uname,password=pswd)
            if usr:
                login(request,usr)
                return redirect("home")
            else:
                messages.error(request,"invalid credentials")
                print("invalid")
                return redirect("signin")    


@method_decorator(signin_required,name="dispatch")
class IndexView(TemplateView):
    template_name="index.html"

    #def get(self,request,*ags,**kw):
     #   return render(request,"index.html")
@method_decorator(signin_required,name="dispatch")
class TodoListView(ListView):
    template_name="todos-list.html"
    model=ToDosn
    context_object_name="todos"

    def get_queryset(self):
        return ToDosn.objects.filter(User=self.request.user)



    # def get(self,request,*args,**kw):
    #     qs=ToDosn.objects.filter(User=request.user)
    #     return render(request,"todos-list.html",{"todos":qs})   

@method_decorator(signin_required,name="dispatch")
class TodoAddView(CreateView):#todocreate
    template_name="todo-add.html"
    form_class=TodoForm
    model=ToDosn
    success_url=reverse_lazy("todo-list")

    def form_valid(self, form): 
        form.instance.User=self.request.user
        messages.success(self.request,"todo created")
        return super().form_valid(form)


    # def get(self,request,*args,**kw):
    #     form=TodoForm()
    #     return render(request,"todo-add.html",{"form":form})     

    # def post(self,request,*args,**kw):
    #     form=TodoForm(request.POST)
    #     if form.is_valid():
    #         instance=form.save(commit=False)
    #         instance.User=request.user
    #         instance.save()
    #         messages.success(request,"todo created")
    #         return redirect("todo-list")
    #     else:
    #         messages.error(request,"failed to create todo")
    #         return render(request,"todo-add.html",{"form":form})                 

@method_decorator(signin_required,name="dispatch")
class TodoDetailView(DetailView):
    template_name="todo-detail.html"
    model=ToDosn
    context_object_name="todo"
    pk_url_kwarg="id"

    # def get(self,request,*args,**kw):
    #     id=kw.get("id")
    #     qs=ToDosn.objects.get(id=id)
    #     return render(request,"todo-detail.html",{"todo":qs})



@signin_required
def todo_delete_view(request,*args,**kw):
    id=kw.get("id")
    qs=ToDosn.objects.get(id=id).delete()
    messages.success(request,"Todo has been deleted")
    return redirect("todo-list")  

@signin_required
def sign_out_view(request,*args,**kw):
    logout(request)
    return redirect("signin")          



from django.shortcuts import render,redirect
from SocialWeb.models import Post,Comments,UserProfile
from django.views.generic import View,CreateView,ListView,UpdateView,DetailView,TemplateView,FormView
from SocialWeb.forms import RegistartionForm,LoginForm,PostForm,ProfileForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator


# Create your views here.
def signin_requried(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

desc=[signin_requried,never_cache]


class SignupView(CreateView):
    model=User
    form_class=RegistartionForm
    template_name="register.html"
    success_url=reverse_lazy("login")

    def post(self,request,*args,**kwargs):
        form=RegistartionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            return render(request,"register.html",{"form":self.form_class})

class SignInView(FormView):
    form_class=LoginForm
    template_name="login.html"
    
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            psd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=psd)
            if usr:
                login(request,usr)
                return redirect("index")
            else:
                return render(request,"login.html",{"form":self.form_class})
            
@method_decorator(desc,name="dispatch")
class IndexView(CreateView,ListView):
    template_name="index.html"
    model=Post
    form_class=PostForm
    success_url=reverse_lazy("index")
    context_object_name="posts"
    
    def form_valid(self, form):
         form.instance.user=self.request.user
         return super().form_valid(form)
    
    def get_queryset(self):
        return Post.objects.all().order_by("-created_date")
 
@method_decorator(desc,name="dispatch")
class AddCommentView(View):
    def post(self,request,*args,**kwargs):
        pid=kwargs.get("id")
        pot=Post.objects.get(id=pid)
        cmt=request.POST.get("comment")
        usr=request.user
        Comments.objects.create(user=usr,post=pot,comment=cmt)
        return redirect("index")

@method_decorator(desc,name="dispatch")
class LikeView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        pot=Post.objects.get(id=id)
        pot.likes.add(request.user)
        pot.save()
        return redirect("index")

@method_decorator(desc,name="dispatch")   
class LikeRemoveView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        pot=Post.objects.get(id=id)
        pot.likes.remove(request.user)
        pot.save()
        return redirect("index")

@method_decorator(desc,name="dispatch")
class CmtLikeView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        cmt=Comments.objects.get(id=id)
        cmt.like.add(request.user)
        cmt.save()
        return redirect("index")

@method_decorator(desc,name="dispatch")    
class CmtRemoveLikeView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        cmt=Comments.objects.get(id=id)
        cmt.like.remove(request.user)
        cmt.save()
        return redirect("index")

@method_decorator(desc,name="dispatch")   
class SignoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("login")

@method_decorator(desc,name="dispatch")
class AddprofileView(CreateView):
    model=UserProfile
    template_name="profile-add.html"
    form_class=ProfileForm
    success_url=reverse_lazy("index")

    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)

@method_decorator(desc,name="dispatch")  
class EditProfileView(TemplateView):
    template_name="profile-view.html"

@method_decorator(desc,name="dispatch")
class ProfileUpdateView(UpdateView):
    model=UserProfile
    form_class=ProfileForm
    template_name="profile-edit.html"
    success_url=reverse_lazy("index")
    pk_url_kwarg="id"

@method_decorator(desc,name="dispatch")
class CmntDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        Comments.objects.filter(user=request.user,id=id).delete()
        return redirect("index")

@method_decorator(desc,name="dispatch")
class PostDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Post.objects.get(id=id).delete()
        return redirect("index")
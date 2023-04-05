from django.shortcuts import render
from api.serializers import UserSerializer,ProfileSerializer,PostSerializer,CommentSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework .viewsets import ModelViewSet,GenericViewSet
from rest_framework import mixins,serializers
from django.contrib.auth.models import User
from SocialWeb.models import UserProfile,Post,Comments
from rest_framework import authentication,permissions
from rest_framework.decorators import action
# Create your views here.
#class UsersView(ViewSet):
    #serializer_class=UserSerializer

    #def create(self,request,*args,**kwargs):
        #serializer=UserSerializer(data=request.data)
        #if serializer.is_valid():
            #serializer.save()
            #return Response(data=serializer.data)
        #else:
            #return Response(data=serializer.errors)
class UsersView(mixins.CreateModelMixin,GenericViewSet):
    serializer_class=UserSerializer
    queryset=User.objects.all()

class ProfileView(ModelViewSet):
    serializer_class=ProfileSerializer
    queryset=UserProfile.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    #def get_queryset(self):
       # return UserProfile.objects.filter(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        pro=self.get_object()
        if pro.user != request.user:
            raise serializers.ValidationError("not allowed to perform")
        else:
            return super().destroy(request,*args,**kwargs)

class PostView(ModelViewSet):
    serializer_class=PostSerializer
    queryset=Post.objects.all().order_by("-created_date")
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    #localhost:8000/api/questions/{id}/add_answer
    @action(methods=["post"],detail=True)
    def add_comment(self,request,*args,**kwargs):
        serializer=CommentSerializer(data=request.data)
        id=kwargs.get("pk")
        postss=self.get_object()
        user=request.user
        if serializer.is_valid():
            serializer.save(user=user,post=postss)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
        #localhost:8000/api/post/{id}/add_like/  
    @action(methods=["post"],detail=True)
    def add_like(self,request,*args,**kwargs):
        post=self.get_object()
        post.likes.add(request.user)
        post.save()
        return Response(data="liked")

#localhost:8000/api/posts/{id}/dislike/ 
    @action(methods=["post"],detail=True)
    def dis_like(self,request,*args,**kwargs):
        post=self.get_object()
        post.likes.remove(request.user)
        post.save()
        return Response(data="disliked")
        
class CommentView(ModelViewSet):
    serializer_class=CommentSerializer
    queryset=Comments.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        raise serializers.ValidationError("method not allowed")
    
    #localhost:8000/api/comments/{id}/add_like/  
    @action(methods=["post"],detail=True)
    def add_like(self,request,*args,**kwargs):
        comment=self.get_object()
        comment.like.add(request.user)
        comment.save()
        return Response(data="liked")

#localhost:8000/api/comment/{id}/dislike/ 
    @action(methods=["post"],detail=True)
    def dis_like(self,request,*args,**kwargs):
        comment=self.get_object()
        comment.like.remove(request.user)
        comment.save()
        return Response(data="disliked")
    
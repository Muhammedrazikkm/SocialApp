from django.urls import path
from api import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import ObtainAuthToken
router=DefaultRouter()
router.register("users",views.UsersView,basename="users")
router.register("users/profile",views.ProfileView,basename="profile")
router.register("posts",views.PostView,basename="post")
router.register("comments",views.CommentView,basename="comment")
urlpatterns=[
    path('token/',ObtainAuthToken.as_view())
]+router.urls
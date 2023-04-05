from django.urls import path,include
from SocialWeb import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns=[
    path('register',views.SignupView.as_view(),name="register"),
    path('signin',views.SignInView.as_view(),name="login"),
    path('index',views.IndexView.as_view(),name="index"),
    path('posts/<int:id>/comments/',views.AddCommentView.as_view(),name="add-comment"),
    path('post/<int:id>/likes/add',views.LikeView.as_view(),name="like"),
    path('post/<int:id>/likes/remove',views.LikeRemoveView.as_view(),name="like-remove"),
    path('profile/add',views.AddprofileView.as_view(),name="profile-add"),
    path('profile/view',views.EditProfileView.as_view(),name="profile-view"),
    path('profile/<int:id>/change',views.ProfileUpdateView.as_view(),name="profile-edit"),
    path('logout/',views.SignoutView.as_view(),name="logout"),
    path('comment/<int:id>/delete',views.CmntDeleteView.as_view(),name="delete"),
    path('comment/<int:id>/like/add',views.CmtLikeView.as_view(),name="add-like"),
    path('comment/<int:id>/like/remove',views.CmtRemoveLikeView.as_view(),name="remove-like"),
    path('post/<int:pk>/remove',views.PostDeleteView.as_view(),name="post-delete"),
    path('api/',include("api.urls"))
   

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
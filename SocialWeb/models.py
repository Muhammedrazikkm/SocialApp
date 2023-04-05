from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

# Create your models here.
class Post(models.Model):
    description=models.CharField(max_length=200)
    image=models.ImageField(upload_to="images",null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    likes=models.ManyToManyField(User,related_name="pic")

    def __str__(self):
        return self.post
    
    @property
    def post_comment(self):
        return Comments.objects.filter(post=self).annotate(ucount=Count('like')).order_by('-ucount')
    
    
    @property
    def like_count(self):
        return self.likes.all().count()

class Comments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    comment=models.CharField(max_length=200)
    created_date=models.DateTimeField(auto_now_add=True)
    like=models.ManyToManyField(User,related_name="comment")

    @property
    def likes_count(self):
        return self.like.all().count()
    
  

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    profile_pic=models.ImageField(upload_to="profile",null=True)
    bio=models.CharField(max_length=200)

    @property
    def post_count(self):
        return Post.objects.filter(user=self.user).count()
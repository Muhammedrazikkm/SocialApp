from SocialWeb.models import Post,Comments
def Activities(request):
    if request.user.is_authenticated:
        pt=Post.objects.filter(user=request.user).count()
        cmt=Comments.objects.filter(user=request.user).count()
        return {"pcount":pt ,"ccomment":cmt}
    else:
        return {"pcount":0,"ccoment":0}
    
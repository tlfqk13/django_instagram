from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from djangogram.users.models import User as user_model

from . import models
from .forms import CreatePostForm

# Create your views here.
def index(request):
    # 인증확인 분기 추가 
    if request.method == "GET":
        # 로그인한 나의 포스트와 팔로잉 유저를 피드에
        if request.user.is_authenticated:
            user = get_object_or_404(user_model, pk=request.user.id) # 로그인된 유저
            following = user.following.all() #유저가 팔로잉하는 모든 애새들
            posts = models.Post.objects.filter(
                Q(author__in=following) | Q(author=user)
            )# Q 객체. or 조건을 사용하기 위해 

            return render(request, 'posts/base.html')

def post_create(request):
    if request.method == 'GET':
        form = CreatePostForm()
        return render(request, 'posts/post_create.html')

    elif request.method == 'POST':
        if request.user.is_authenticated:
            user = get_object_or_404(user_model, pk=request.user.id)
            # image = request.FILES['image']
            # caption = request.POST['caption']

            # new_post = models.Post.objects.create(
            #     author = user,
            #     image = image,
            #     caption = caption
            # )
            # new_post.save()

            form = CreatePostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = user
                post.save()
            else:
                print(form.errors)

            return render(request, 'posts/base.html')

        else:
            return render(request, 'users/main.html')
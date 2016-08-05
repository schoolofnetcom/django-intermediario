from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from blog.forms import PostForm
from blog.models import Category, Post


def home(request):
    name = "Wesley"
    # categories = ['PHP', 'Java', 'Ruby']
    # for category in categories:
    #     Category.objects.create(name=category)
    all_categories = Category.objects.all()

    category_python = Category.objects.get(name='Ruby')
    posts = Post.objects.filter(status='Published')

    # post = Post()
    # post.name = "Show Post 3"
    # post.content = "Content"
    # post.status = "Published"
    # post.category = category_python
    # post.save()

    context = {
        'name': name,
        'categories': all_categories,
        'posts': posts,
    }

    return render(request, 'blog/home.html', context)


def show_posts_by_category(request, category_id):
    all_categories = Category.objects.all()
    category = Category.objects.get(pk=category_id)
    posts = Post.objects.filter(category=category, status='Published')

    context = {
        'posts': posts,
        'categories': all_categories,
        'category': category
    }

    return render(request, 'blog/home.html', context)

def auth(request):
    error = False

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user == None:
            error = True
        else:
            error = False
            login(request, user)

    context = {
        'error': error
    }
    return render(request, 'blog/auth.html', context)

def logout_view(request):
    logout(request)
    return redirect('blog.home')

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = Post()
            post.author = request.user
            post.category = form.cleaned_data['category']
            post.name = form.cleaned_data['name']
            post.content = form.cleaned_data['content']
            post.status = form.cleaned_data['status']
            post.save()
            return redirect('blog.home')
    else:
        form = PostForm()

    return render(request, 'blog/post_create.html', {'form': form})
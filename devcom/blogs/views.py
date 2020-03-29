from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.utils import timezone
import datetime as dt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


@login_required
def intermediate(request):
    return redirect(dashboard, user_id=request.user.id)


def home(request):
    return render(request, 'blogs/home.html', )


def signup(request):
    if request.method == 'POST':
        form = Signup_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/blogs/login/')
    else:
        form = Signup_form()

    args = {'form': form}
    return render(request, 'blogs/signup.html', args)


@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect(home)


@login_required
def logout_view(request):
    return render(request, 'blogs/logout.html', {'user': request.user})


@login_required
def dashboard(request, user_id):
    if request.user.id == user_id:
        user = User.objects.get(pk=user_id)
        list = user.blog_set.all().order_by('-datetime')
        return render(request, 'blogs/dashboard.html', {'list': list, 'user': user})
    else:
        return render(request, 'blogs/access_denied.html', {'user_id': request.user.id})


@login_required
def add(request, user_id):
    if request.user.id == user_id:
        user = User.objects.get(pk=user_id)
        if request.method == 'POST':
            text_entered = request.POST.get("text")
            title_entered = request.POST.get("title")
            user.blog_set.create(blog_title=title_entered, blog_text=text_entered)
            return redirect(dashboard, user_id=user.id)
        else:
            form = Blog_form()

        return render(request, 'blogs/add.html', {'form': form})
    else:
        return render(request, 'blogs/access_denied.html', {'user_id': request.user.id})


@login_required
def blog(request, user_id, blog_id):
    if request.user.id == user_id:
        user = User.objects.get(pk=user_id)
        blog = user.blog_set.get(pk=blog_id)
        return render(request, 'blogs/blog.html', {'blog': blog})
    else:
        return render(request, 'blogs/access_denied.html', {'user_id': request.user.id})


@login_required
def edit(request, user_id, blog_id):
    if request.user.id == user_id:
        user = User.objects.get(pk=user_id)
        blog = user.blog_set.get(pk=blog_id)
        if request.method == 'POST':
            text_entered = request.POST.get("text")
            title_entered = request.POST.get("title")
            blog.blog_title = title_entered
            blog.blog_text = text_entered
            blog.save()
            return redirect(dashboard, user_id=user.id)
        else:
            form = Blog_form(initial={'title': blog.blog_title,
                                      'text': blog.blog_text})

        return render(request, 'blogs/add.html', {'form': form})
    else:
        return render(request, 'blogs/access_denied.html', {'user_id': request.user.id})


def blog_view(request, user_id, blog_id):
    user = User.objects.get(pk=user_id)
    blog = user.blog_set.get(pk=blog_id)
    if request.method == 'POST':
        if 'upvote' in request.POST:
            blog.votes += 1
            blog.save()
            return redirect(blog_view, user_id=user_id, blog_id=blog.id)
        elif 'downvote' in request.POST:
            blog.votes -= 1
            blog.save()
            return redirect(blog_view, user_id=user_id, blog_id=blog.id)
        else:
            return redirect(blog_view, user_id=user_id, blog_id=blog.id)
    else:
        return render(request, 'blogs/blog_view.html', {'blog': blog})


def dashboard_view(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request, 'blogs/dashboard_view.html', {'user': user})


def trending(request, days):
    if days == 1:
        blogs_list = Blog.objects.filter(datetime__date=dt.date.today()
                                         ).order_by('-votes')
        text = "today"
    else:
        blogs_list = Blog.objects.filter(datetime__gte=timezone.now() - dt.timedelta(days=days)
                                         ).order_by('-votes')
        if days == 7:
            text = "this week"
        elif days == 31:
            text = "this month"
        elif days == 365:
            text = "this year"
    return render(request, 'blogs/trending.html', {'list': blogs_list, 'text': text})


@login_required
def delete(request, user_id, blog_id):
    if request.user.id == user_id:
        user = User.objects.get(pk=user_id)
        blog = user.blog_set.get(pk=blog_id)
        if 'delete' in request.POST:
            blog.delete()
            return redirect(dashboard, user_id=user_id)
        else:
            return render(request, 'blogs/delete.html', {'blog': blog})
    else:
        return render(request, 'blogs/access_denied.html', {'user_id': request.user.id})


@login_required
def comment(request, user_id, blog_id):
    blog_obj = Blog.objects.get(pk=blog_id)
    commentor = request.user
    if request.method == 'POST':
        comment_entered = request.POST.get("text")
        blog_obj.comment_set.create(commentor=commentor, comment_text=comment_entered)
        if request.user == blog_obj.user:
            return redirect(blog, user_id=user_id, blog_id=blog_id)
        else:
            return redirect(blog_view, user_id=user_id, blog_id=blog_id)
    else:
        form = Comment_form()
        return render(request, 'blogs/comment.html', {'form': form})

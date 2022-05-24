from django.contrib.auth import logout
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, login, logout, authenticate
from django.utils import timezone
from blog.forms import PostForm, CommentForm, SignUpForm, ChangePasswordForm, loginForm
from blog.models import Post, Comment

# Create your views here.

def post_list(request):
    stuff_for_frontend= Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': stuff_for_frontend})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    isAuthor = False
    if str(post.author) == str(request.user) :
        isAuthor = True
    stuff_for_frontend = {'post': post, 'isAuthor': isAuthor}
    return render(request, 'blog/post_detail.html', stuff_for_frontend)


@login_required(login_url='/login/')
def post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid:
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = None
            post.save()
            return redirect('post_detail', pk=post.pk)
            

    form = PostForm()
    stuff_for_frontend = {'form': form}
    return render(request, 'blog/post_edit.html', stuff_for_frontend)


@login_required(login_url='/login/')
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = None
            post.save()
            return redirect('post_detail', pk=post.pk)

    else:
        form = PostForm(instance=post)
        stuff_for_frontend = {'form': form , 'post':post}
    
    return render(request, 'blog/post_edit.html', stuff_for_frontend)


# Delete a post 
@login_required(login_url='/login/')
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if str(request.user) == str(post.author) or request.user.is_superuser:
        post.delete()   
    return redirect('post_list')
    

@login_required(login_url='/login/')
def post_draft_list(request):
  
    posts = Post.objects.filter(author=request.user, published_date__isnull=True).order_by('-created_date')

    stuff_for_frontend = {
        'posts': posts,
    }
    return render(request, 'blog/post_draft_list.html', stuff_for_frontend)


@login_required(login_url='/login/')
def post_publish(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.published_date = timezone.now()
    post.save()
    return redirect('post_detail', pk=pk)


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('post_list')


@login_required(login_url='/login/')
def add_comment_on_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})
    
@login_required(login_url='/login/')
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    c_id = comment.post.pk
   
    if str(request.user) == str(comment.author) or request.user.is_superuser:
        comment.delete()
        return redirect('post_detail', pk=c_id)
        
    return redirect('post_list')


def signUp(request):
    if request.user.is_authenticated:
        return redirect('post_list')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            
            return redirect('login')
    else: 
        form = SignUpForm()

    return render(request,'blog/signupForm.html', {'form':form})


@login_required(login_url='/login/')
def password_change(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('profile')
      
    form = ChangePasswordForm(request.user)
    return render(request, 'blog/password_change.html', {'form': form})


def my_posts(request):
    
    posts = Post.objects.filter(author=request.user, published_date__isnull=False).order_by('-published_date')
    fronted_stuff = {
        'posts': posts,
    }
    return render(request, 'blog/my_posts.html', fronted_stuff)


def login_view(request):
    if request.user.is_authenticated:
            return redirect('post_list')
    elif request.method == "POST":
            form = loginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = request.POST['username']
                pword = request.POST['password']
                user = authenticate(username=uname, password=pword)
                if user is not None:
                    login(request, user)
                    return redirect('post_list')
                else:
                    return redirect('login')

    form = loginForm()
    stuff_for_frontend = {
        'form': form,
    }
    return render(request, 'blog/login.html', stuff_for_frontend)


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('login')

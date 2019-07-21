from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django import forms
from django.http import HttpResponseRedirect
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostCreate

deutsch = ['Haus', 'Weihnachten', 'Wollen', 'möchten', 'sprechen', 'besuchen']
italienisch = ['Casa', 'Natale', 'volere', 'prendere', 'parlare', 'visitare']

def home(request):
    context = {
        'posts': Post.objects.all(),
        'deutsch': deutsch,
        'italienisch': italienisch
    }
    return render(request, 'blog/home.html', context)

class PostListView(LoginRequiredMixin, ListView):

    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html in diesem fall blog/post_list.html
    model = Post
    context_object_name = 'posts'
    ordering = ['-date_posted'] # das heißt vom neuesten zum ältesten
    paginate_by = 5 #das heißt, dass nach dem 2. Post eine neue Seite kommt


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        posts = Post.objects.filter(Q(author=user) | Q(linked=user)).order_by('-date_posted') #selbstgemacht!
        return posts




class PostDetailView(DetailView, LoginRequiredMixin):
    model = Post


class PostCreateView(LoginRequiredMixin ,CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

@login_required
def post_create(request):
    users = User.objects.all()
    linked = []
    if request.method == 'POST':
        content_form = PostCreate(request.POST)
        if content_form.is_valid():
            title = request.POST.get('title')
            content = content_form.cleaned_data.get('content')

            for x, letter in enumerate(title):
                if letter == '@':
                    word = title[x+1:].split(' ')[0]
                    if word in [user.username for user in users]:
                        user = User.objects.get(username=word)
                        linked.append(user)
        post = Post.objects.create(title=title, content=content, author=request.user)
        post.linked.set(linked)
        return HttpResponseRedirect(reverse("post-detail", args=[post.id]))

    else:
        content_form = PostCreate()
    return render(request, 'blog/new_post.html', {'content_form': content_form, 'users': users})

@login_required
def update_post(request, pk):
    blogpost = get_object_or_404(Post, id=pk)

    if request.user == blogpost.author:
        users = User.objects.all()
        linked = []
        class UpdatePost(forms.ModelForm):
            content = forms.CharField(initial=blogpost.content, widget=forms.Textarea(attrs={'cols': 10, 'rows': 12}))

            class Meta:
                model = Post
                fields = ['content']

        if request.method == 'POST':
            content_form = UpdatePost(request.POST)
            if content_form.is_valid():
                title = request.POST.get('title')
                content = content_form.cleaned_data.get('content')
                for x, letter in enumerate(title):
                    if letter == '@':
                        word = title[x+1:].split(' ')[0]
                        if word in [user.username for user in users]:
                            user = User.objects.get(username=word)
                            linked.append(user)
                blogpost.linked.set(linked)
                blogpost.title = title
                blogpost.content = content
                blogpost.save()

            return HttpResponseRedirect(reverse("post-detail", args=[pk]))

        else:
            content_form = UpdatePost()
        return render(request, 'blog/update_post.html', {'content_form': content_form, 'users': users, 'title': str(blogpost.title)})
    else:
        return redirect('/')

@login_required
def post_detail(request, pk):
    blogpost = get_object_or_404(Post, id=pk)
    title = blogpost.title
    user = request.user
    links = []
    html_title = {}
    content_form = None
    users = User.objects.all()
    linked = []


    if request.method == 'POST':
        content_form = PostCreate(request.POST)
        if content_form.is_valid():
            title = request.POST.get('title')
            content = content_form.cleaned_data.get('content')

            for x, letter in enumerate(title):
                if letter == '@':
                    word = title[x + 1:].split(' ')[0]
                    if word in [user.username for user in users]:
                        user = User.objects.get(username=word)
                        linked.append(user)
        post = Post.objects.create(title=title, content=content, author=request.user)
        post.linked.set(linked)
        return HttpResponseRedirect(reverse("post-detail", args=[post.id]))
    else:

        if user in blogpost.linked.all():

            viewed_users = blogpost.viewed
            if not viewed_users:
                blogpost.viewed = f'{user.id},'
                blogpost.save()
            else:
                splitted = viewed_users.split(',')
                print(splitted)
                if str(user.id) not in splitted:
                    blogpost.viewed = blogpost.viewed + f'{user.id},'
                    blogpost.save()

        startpoint = 0
        abschnitt = 0
        linked_user = 0
        if not '@' in title:
            html_title['ohne@'] = title

        else:
            for x, letter in enumerate(title):
                if letter == '@':
                    word = title[x + 1:].split(' ')[0]
                    if word in [str(title) for title in blogpost.linked.all()]:
                        user = User.objects.get(username=word)
                        endpoint = x + 1 + len(word)

                        html_title[abschnitt-1] = title[startpoint:x] #davor
                        html_title[user.username + str(linked_user)] = title[x+1:endpoint]
                        links.append(user.username + str(linked_user))
                        linked_user += 1

                        startpoint += endpoint
                        html_title[abschnitt] = title[endpoint:] #danach
                        abschnitt += 1
                    else:
                        html_title[abschnitt - 1] = title[startpoint:x]
                        
                        html_title[abschnitt] = title[x:]

        if request.user in blogpost.linked.all():
            content_form = PostCreate()



    return render(request, 'blog/post_detail.html', {'object': blogpost, 'user': request.user, 'title': html_title, 'links_all': links,
                                                     'content_form': content_form, 'users': users})

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    def get_success_url(self):
        return reverse('blog-home')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About me'})

from django.http import  HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.views.generic import (ListView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView,
                                  DetailView,
                                   View)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormMixin
from .forms import PostCreateForm, CommentForm, ReplayForm
from .models import User, Comment, CommentReplay
from tempcheck.models import Post
from django.http import JsonResponse
from tempcheck.filters import PostFilter
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from activity_log.models import ActivityLog
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User



def AjaxNotificationComment(request):
    comment_id = request.GET.get('comment_id', None)
    c=Comment.objects.filter(id=comment_id)
    for i in c:
        if i.comment_notifi == False:
            i.comment_notifi = True
            i.save()


def AjaxNotificationReply(request):
    reply_id = request.GET.get('reply_id',None)
    print("reply id",reply_id)
    r=CommentReplay.objects.filter(id=reply_id)
    for i in r:
        if i.reply_notifi == False:
            i.reply_notifi = True
            i.save()


def validate_username(request):
    username = request.GET.get('username', None)
    data = {}
    data['is_taken'] = User.objects.filter(username__iexact=username).exists()
    print(data)
    return JsonResponse(data)


class PaginatedFilterViews(View):
    def get_context_data(self, **kwargs):
        context = {}
        if self.request.GET:
            query = self.request.GET.copy()
            if self.request.GET.get('page'):
                del query['page']
            context['query'] = query.urlencode()
        return context


class PostListView(ListView):
    model = Post
    template_name = 'Blog_new/pages/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        post_filter = PostFilter(self.request.GET, queryset=self.get_queryset())
        filterqs = post_filter.qs
        page = self.request.GET.get('page', 1)
        paginator = Paginator(filterqs, 9)
        try:
            blog_posts = paginator.page(page)
        except PageNotAnInteger:
            blog_posts = paginator.page(1)
        except EmptyPage:
            blog_posts = paginator.page(paginator.num_pages)
        if self.request.GET:
            query = self.request.GET.copy()
            if self.request.GET.get('page'):
                del query['page']
            context['query'] = query.urlencode()
        context['filter'] = post_filter
        context['blog_posts'] = blog_posts
        context['comment'] = Comment.objects.filter(approved_comment=True).count()
        context['count'] = Post.objects.count()
        return context


class UserPostListView(ListView):
    model = Post
    template_name = 'Blog_new/pages/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = 'Blog_new/pages/detail.html'
    form_class = CommentForm

    def get_context_data(self,  **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['form'] = CommentForm
        context['form2'] = ReplayForm
        context['likescount'] = self.object.likes.count()
        print("like count in detail view", context['likescount'])
        context['is_liked'] = self.object.likes.filter(id=self.request.user.id).exists()
        po = get_object_or_404(Post, pk=self.kwargs['pk'])
        context['commentcount'] = po.comments.filter(approved_comment=True).count()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/login')
        self.object = self.get_object()

        if request.method == 'POST' and 'commentpost' in request.POST:
            form = CommentForm(self.request.POST)
            if form.is_valid():
                comment_name = form.cleaned_data.get('text')
                form.instance.author = self.request.user
                form.instance.post = Post.objects.get(pk=self.kwargs['pk'])
                form.save()
                activity_log = Post.objects.filter(pk=self.kwargs['pk'])
                for i in activity_log:
                    ActivityLog.objects.create(user=self.request.user, activity="Commented \"{}\" on \"{}\"".format(comment_name, i.title))
                return super(PostDetailView, self).form_valid(form)
            else:
                return CommentForm()
        elif request.method == 'POST' and 'replypost' in request.POST:
            form = ReplayForm(self.request.POST)
            if form.is_valid():
                reply_name = form.cleaned_data.get('Replay')
                form.instance.author = self.request.user
                form.instance.post = Post.objects.get(pk=self.kwargs['pk'])
                form.instance.comment = Comment.objects.get(pk=self.request.POST.get('replyid'))
                post_log = Post.objects.filter(pk=self.kwargs['pk'])
                comment_log = Comment.objects.filter(pk=self.request.POST.get('replyid'))
                for i in post_log:
                    for j in comment_log:
                        ActivityLog.objects.create(user=self.request.user,
                                                    activity="Replied  \"{}\" on \"{}\" in \"{}\"".format(reply_name, j.text, i.title))
                form.save()
                return super(PostDetailView, self).form_valid(form)
            else:
                return ReplayForm()
        elif request.method == 'POST' and 'post_id' in request.POST:
            post = get_object_or_404(Post, pk=self.kwargs['pk'])
            if post.likes.filter(id=request.user.id).exists():
                post.likes.remove(request.user)
                print("post title is",post.title)
                ActivityLog.objects.create(user=self.request.user, activity="Unliked in \"{}\"".format(post.title))

            else:
                post.likes.add(request.user)
                ActivityLog.objects.create(user=self.request.user, activity="Liked in \"{}\"".format(post.title))
        return HttpResponseRedirect(reverse('temp_post-detail', kwargs={'pk': self.kwargs['pk']}))

    def get_success_url(self):
        return reverse('temp_post-detail', kwargs={'pk': self.kwargs['pk']})


class LikeAPIview(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None, format=None):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        print("like api view",post)
        updated = False
        liked = False
        like_count = 0
        print("like count",like_count)
        user = self.request.user
        if user.is_authenticated:
            if post.likes.filter(id=request.user.id).exists():
                liked = False
                post.likes.remove(request.user)
                like_count = post.likes.count()

            else:
                liked = True
                post.likes.add(request.user)
                like_count = post.likes.count()

            updated = True
        data = {
            "updated": updated,
            "liked": liked,
            "like_count": like_count,
        }
        return Response(data)



class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm

    def form_valid(self, form):
        title = form.cleaned_data.get('title')
        form.instance.author = self.request.user
        ActivityLog.objects.create(user=self.request.user, activity="Post : \"{}\" was created".format(title))
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostCreateForm

    def get_success_url(self):
        return reverse('temp_post-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        title = form.cleaned_data.get('title')
        # content = form.cleaned_data.get('content')
        form.instance.author = self.request.user
        ActivityLog.objects.create(user=self.request.user, activity="Post: \"{}\" Updated".format(title))
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post

    def get_success_url(self):
        post_delete = self.model.objects.filter(id=self.kwargs['pk'])
        for i in post_delete:
            ActivityLog.objects.create(user=self.request.user, activity="Post \"{}\" deleted".format(i.title))
        return reverse('temp_user-posts', kwargs={'username': self.request.user})

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'Blog_new/pages/comments.html'

    def form_valid(self, form):
        comment_name = form.cleaned_data.get('text')
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs['pk_1'])
        comment_log = Comment.objects.filter(id=self.kwargs['pk'])
        for i in comment_log:
            ActivityLog.objects.create(user=self.request.user, activity="updated comment \"{}\" to \"{}\"".format(i.text, comment_name))
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        else:
            return False


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'Blog_new/pages/comment_confirm_delete.html'

    def get_success_url(self):
        comment_delete = self.model.objects.filter(id=self.kwargs['pk'])
        for i in comment_delete:
            ActivityLog.objects.create(user=self.request.user, activity="Comment \"{}\" deleted in \"{}\"".format(i.text, i.post.title))
        return reverse('temp_post-detail', kwargs={'pk': self.object.post_id})
    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        else:
            return False


class ReplayCreateView(LoginRequiredMixin, CreateView):
    model = CommentReplay
    form_class = ReplayForm
    template_name = 'Blog_new/pages/comment_replay.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs['pk_1'])
        form.instance.comment = Comment.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)


class ReplyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CommentReplay
    form_class = ReplayForm
    template_name = 'Blog_new/pages/comment_replay.html'

    def form_valid(self, form):
        rply = form.cleaned_data.get('Replay')
        form.instance.author = self.request.user
        form.instance.comment = Comment.objects.get(pk=self.kwargs['pk_2'])
        form.instance.post = Post.objects.get(pk=self.kwargs['pk_1'])
        comment_rply_log = CommentReplay.objects.filter(id= self.kwargs['pk'])
        for i in comment_rply_log:
            ActivityLog.objects.create(user=self.request.user, activity="updated \"{}\" to \"{}\" in \"{}\" in \"{}\"".format(i.Replay, rply, i.comment.text, i.post.title))
        return super().form_valid(form)

    def test_func(self):
        reply = self.get_object()
        if self.request.user == reply.author:
            return True
        else:
            return False


class ReplyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CommentReplay

    def get_success_url(self):

        return reverse('temp_post-detail', kwargs={'pk': self.object.post_id})

    def test_func(self):
        reply = self.get_object()
        if self.request.user == reply.author:
            return True
        else:
            return False


class ReplyListView(ListView):
    model = CommentReplay
    template_name = 'Blog_new/pages/reply_template.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['obj'] = CommentReplay.objects.filter(comment_id=self.kwargs['pk'])
        return context

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('temp_post-detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('temp_post-detail', pk=comment.post.pk)


@login_required
def reply_approve(request, pk):
    reply = get_object_or_404(CommentReplay, pk=pk)
    reply.approve()
    return redirect('temp_post-detail', pk=reply.post.pk)


@login_required
def reply_remove(request, pk):
    reply = get_object_or_404(CommentReplay, pk=pk)
    print("inside reply delete view")
    reply_delete = CommentReplay.objects.filter(id=pk)
    for i in reply_delete:
        print("inside replay delete for loop")
        ActivityLog.objects.create(user=request.user,
                                   activity="Deleted \"{}\" in \"{}\" in \"{}\"".format(i.Replay, i.comment.text, i.post.title))
    reply.delete()
    return redirect('temp_post-detail', pk=reply.post.pk)

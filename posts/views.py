from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from .models import Post, Status
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# Create your views here.
class PostListView(ListView):
    template_name = "posts/list.html"
    model = Post

    def get_context_data(self, **kwarg):
        context = super().get_context_data(**kwarg)

        publish_status = Status.objects.get(name="published")

        context["post_list"] = (
            Post.objects.filter(status=publish_status).order_by("created_on").reverse()
        )

        return context


class DraftListView(ListView):
    template_name = "posts/list.html"
    model = Post

    def get_context_data(self, **kwarg):
        context = super().get_context_data(**kwarg)

        draft_status = Status.objects.get(name="draft")

        context["post_list"] = (
            Post.objects.filter(status=draft_status).order_by("created_on").reverse()
        )

        return context


class ArchiveListView(LoginRequiredMixin, ListView):
    template_name = "posts/list.html"
    model = Post

    def get_context_data(self, **kwarg):
        context = super().get_context_data(**kwarg)

        archived_status = Status.objects.get(name="archived")

        context["post_list"] = (
            Post.objects.filter(status=archived_status).order_by("created_on").reverse()
        )

        return context


class PostDetailView(DetailView):
    template_name = "posts/detail.html"
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = "posts/new.html"
    model = Post
    fields = ["title", "subtitle", "body", "status"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "posts/edit.html"
    model = Post
    fields = ["title", "subtitle", "body", "status"]

    def test_func(self):
        # This MUST return True or False
        post = self.get_object()
        return post.author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "posts/delete.html"
    model = Post
    success_url = reverse_lazy("list")

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
# from django.utils import timezone

from .models import BlogPost
from .forms import BlogPostModelForm

def blog_post_list_view(request):
    # now = timezone.now()
    # qs = BlogPost.objects.filter(publish_date__lte=now)
    qs = BlogPost.objects.all().published()
    # qs = BlogPost.objects.published()

    if request.user.is_authenticated:
        my_qs = BlogPost.objects.filter(user=request.user)
        qs = (qs | my_qs).distinct()
    template_name = 'blog/list.html'
    context = {"object_list": qs}
    return render(request, template_name, context)

def blog_post_detail_view(request, post_slug):
    obj = get_object_or_404(BlogPost, slug=post_slug)
    template_name = 'blog/detail.html'
    context = {"object": obj}
    return render(request, template_name, context)

# @login_required(login_url='/login')
# @login_required # already setted path in settings.py
@staff_member_required # redirect to login, enable permission in front
def blog_post_create_view(request):
    form = BlogPostModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        print(request.FILES)
        # form.save()
        obj = form.save(commit=False)
        # obj.title = form.cleaned_data.get('title') + " add"
        # obj.slug = form.cleaned_data.get('slug') + "_add"
        obj.user = request.user # logged user
        obj.save()
        form = BlogPostModelForm()

    template_name = 'form.html'
    context = {"form": form}
    return render(request, template_name, context)

@staff_member_required
def blog_post_update_view(request, post_slug):
    obj = get_object_or_404(BlogPost, slug=post_slug)
    form = BlogPostModelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
    template_name = 'form.html'
    context = {'form': None, "title": f"Update {obj.title}", "form": form}
    return render(request, template_name, context)

@staff_member_required
def blog_post_delete_view(request, post_slug):
    obj = get_object_or_404(BlogPost, slug=post_slug)
    template_name = 'blog/delete.html'
    if request.method == "POST":
        obj.delete()
        return redirect("/blog")
    context = {"object": obj}
    return render(request, template_name, context)
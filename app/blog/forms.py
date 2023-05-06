from django import forms
from .models import BlogPost

class BlogPostForm(forms.Form):
    title = forms.CharField()
    slug = forms.SlugField()
    content = forms.CharField(widget=forms.Textarea)

class BlogPostModelForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'image', 'slug', 'content', 'publish_date']

    # Validation insode model form
    def clean_title(self, *args, **kwargs):
        # print(dir(self)) # all the possible options to extract infos
        instance = self.instance
        print(instance)

        # also detects slug duplicate
        title = self.cleaned_data.get('title')
        qs = BlogPost.objects.filter(title__iexact=title)
        if instance is not None: # exclude current register from exists() validation
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise forms.ValidationError("This title has already been used. Please try another")

        return title

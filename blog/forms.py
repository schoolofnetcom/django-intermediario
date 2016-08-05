from django.forms import ModelForm

from blog.models import Post


class PostForm(ModelForm):
    def __init__(self, * args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })

    class Meta:
        model = Post
        fields = ['category','name', 'content', 'status']
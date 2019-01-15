from django.forms import ModelForm
from comment.models import UserComment


class CommentForm(ModelForm):
    class Meta:
        model = UserComment
        fields = ['content']

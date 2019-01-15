from django.forms import ModelForm, Textarea
from picture.models import PictureEntry


class PublishImgForm(ModelForm):

    class Meta:
        model = PictureEntry
        fields = ['img_url', 'description']
        widgets = {
            'img_url': Textarea(attrs={'cols': 50, 'rows': 10}),
            'description': Textarea(attrs={'cols': 50, 'rows': 20}),
        }

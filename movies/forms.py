from django import forms
from django.contrib.auth.models import User

from .models import Movie, Review


def _style_fields(form):
    for field in form.fields.values():
        widget = field.widget
        if isinstance(widget, (forms.CheckboxInput, forms.CheckboxSelectMultiple)):
            widget.attrs.setdefault('class', 'form-check-input')
        elif isinstance(widget, forms.Select):
            widget.attrs.setdefault('class', 'form-select')
        else:
            existing = widget.attrs.get('class', '')
            widget.attrs['class'] = f'{existing} form-control'.strip()


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['name', 'price', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _style_fields(self)
        if self.instance and self.instance.pk:
            self.fields['image'].required = False


class StaffReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['movie', 'user', 'comment', 'is_hidden']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.order_by('username')
        self.fields['movie'].queryset = Movie.objects.order_by('name')
        _style_fields(self)


class ReviewReportForm(forms.Form):
    reason = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Optional reason',
        }),
    )

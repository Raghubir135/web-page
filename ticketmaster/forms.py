from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = [
            'user']  # show all field from the model, but exclude user (primary key) as this is not something user should enter in the generated form

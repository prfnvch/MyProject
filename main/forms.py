from django import forms
from .models import Manga, MangaComment, ChapterComment


class MangaCommentForm(forms.ModelForm):
    class Meta:
        model = MangaComment
        fields = ('content',)


class ChapterCommentForm(forms.ModelForm):
    class Meta:
        model = ChapterComment
        fields = ('content',)

import uuid

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

    def clean(self, ):
        data = super().clean()
        today_comment = timezone.now().date()
        comments_today = Comment.objects.filter(created__date=today_comment)

        if comments_today.count() >= 15:
            # raise ValidationError(
            #     "You cant send comment today"
            # )
            self.add_error("content", "You cant send comment today")

        # if 'spam' in content_spam_free:
        #     self.add_error("content", "You cant input spam keyword")

        # if comment:
        #     today = timezone.localdate().today()
        #     comment_count = Comment.objects.filter(created__date=today).count()
        #     if comment_count >= 5:
        #         self.add_error('comment', 'Maxmimum number comment for today is 5')

        return data

    def clean_content(self):
        data = self.cleaned_data['content']
        if 'spam' in data:
            raise ValidationError('dont include spam word')
        return data

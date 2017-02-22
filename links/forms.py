from django import forms

from .models import Link


class LinkForm(forms.ModelForm):

    class Meta:
        model = Link
        fields = ('url', 'tags',)

    def save(self, author, commit=True):
        instance = super(LinkForm, self).save(commit=False)
        instance.author = author

        if commit:
            instance.save()
        return instance

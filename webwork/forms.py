# -*- coding: utf-8 -*-
from django import forms

class PostForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, max_length=1000, label="How geeky is your life?")
    
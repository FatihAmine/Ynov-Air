from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'min': 1,
                'max': 5,
                'class': 'form-control form-control-lg rounded-pill text-center',
                'placeholder': '1–5'
            }),
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control rounded-3',
                'placeholder': 'Write your review here...'
            }),
        }

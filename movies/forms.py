from django import forms

from .models import UserRating


class RatingForm(forms.ModelForm):
    rating = forms.FloatField(
        min_value=0.5,
        max_value=5.0,
        widget=forms.NumberInput(attrs={"step": "0.5"}),
    )

    class Meta:
        model = UserRating
        fields = ["rating", "comment"]
        widgets = {
            "comment": forms.Textarea(attrs={"rows": 3, "placeholder": "Leave a quick note (optional)"}),
        }

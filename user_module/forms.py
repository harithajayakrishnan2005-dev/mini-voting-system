from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Feedback
from .models import UserProfile

User = get_user_model()

class CustomerSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = "user"  
        if commit:
            user.save()
        return user


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['poll', 'rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }


User = get_user_model()

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['contact', 'address', 'place', 'age', 'image']

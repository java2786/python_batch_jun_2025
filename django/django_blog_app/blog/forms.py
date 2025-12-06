from django import forms
from .models import Profile, BlogPost
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture', 'location']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about yourself...'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Mumbai, Maharashtra'
            })
        }

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            # Validate file size (max 2MB)
            if picture.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Image file size should not exceed 2MB")
            
            # Validate file extension
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            import os
            ext = os.path.splitext(picture.name)[1].lower()
            if ext not in valid_extensions:
                raise forms.ValidationError("Only JPG, JPEG, PNG, and GIF files are allowed")
        
        return picture
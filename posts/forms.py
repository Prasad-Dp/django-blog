from django import forms
from . import models

class BlogForm(forms.ModelForm):
    GEEKS_CHOICES =(
    ("News", "News"),
    ("Entertainment", "Entertainment"),
    ("Sports", "Sports"),
    ("Science", "Science"),
    ("Arts", "Arts"),
)
    tittle=forms.CharField(max_length=100,
    widget=forms.TextInput(attrs={'class':' form-control','placeholder':'tittle',}))

    post_img=forms.ImageField()

    post_disc=forms.CharField(widget=forms.Textarea( attrs={'class':'form-control'}))

    category=forms.ChoiceField( choices=GEEKS_CHOICES)

    class Meta:
        model=models.Post
        fields =(
            'tittle',
            'post_disc',
            'category',
            'post_img',
        )

class UserProfileForm(forms.ModelForm):
    
    name=forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'form-control'  }))
    about=forms.CharField(max_length=30,widget=forms.Textarea(attrs={'class':'form-control'}))
    location=forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'form-control'}))
    pfg_img=forms.ImageField()
    pbg_img=forms.ImageField()
    class Meta:
        model=models.UserProfile
        fields=(
            'name',
            'about',
            'location',
            'pfg_img',
            'pbg_img',
            
        )

    

    
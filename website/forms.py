from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class ContentSectionForm(forms.ModelForm):
    class Meta:
        model = ContentSection  # Assuming you have a ContentSection model
        fields = ['content']  # Adjust fields as needed

class PageForm(forms.ModelForm):
    # Use formsets for dynamic section handling
    content_sections = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Page
        fields = ['title', 'content_sections']  # Exclude 'slug' since it will be auto-generated

    def save(self, commit=True):
        page = super().save(commit)
        # Here, handle the saving of dynamic content sections
        # You can use self.cleaned_data['content_sections'] to handle multiple sections
        return page

class GalleryImageForm(forms.ModelForm):
    # New field for marking an image as featured
    featured = forms.BooleanField(required=False)

    class Meta:
        model = GalleryImage
        fields = ['title', 'image', 'featured']  # Add the 'featured' field

    def save(self, commit=True):
        gallery_image = super().save(commit)
        # You can add custom save logic if needed
        return gallery_image

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'is_superuser']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
class MarkImagesForDeletionForm(forms.Form):
    delete_images = forms.ModelMultipleChoiceField(
        queryset=GalleryImage.objects.none(),  # This will be populated in the view
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def __init__(self, *args, **kwargs):
        # Allow dynamic queryset population
        super().__init__(*args, **kwargs)
        self.fields['delete_images'].queryset = GalleryImage.objects.filter(marked_for_deletion=False)

class ImportDatabaseForm(forms.Form):
    sql_file = forms.FileField()

    class Meta:
        fields = ['sql_file']

        labels = {
            'sql_file': 'Select SQL File to Import'
        }
        
        widgets = {
            'sql_file': forms.ClearableFileInput(attrs={'class': 'form-control-file'})
        }
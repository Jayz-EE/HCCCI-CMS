from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.utils.text import slugify  # For auto-generating slug
from django.db.models.signals import pre_save
from django.dispatch import receiver
from io import BytesIO
from django.core.files.base import ContentFile
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from PIL import Image, ExifTags

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True, null=True)
    password = models.CharField(max_length=128, verbose_name='password')
    date_joined = models.DateTimeField(default=now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username
    
class RegisterPassword(models.Model):
    RegisterPass = models.CharField(max_length=150)

    def __str__(self):
        return self.RegisterPass

class Page(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    created_at = models.DateTimeField(null=True, blank=True)  # Manually handled
    updated_at = models.DateTimeField(null=True, blank=True)  # Manually handled

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/{self.slug}/'  

class ContentSection(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)  # HTML content for the section
    order = models.PositiveIntegerField(default=0, null=True, blank=True)  # Field to order the sections

    class Meta:
        ordering = ['order']  # Order sections by the 'order' field

    def __str__(self):
        return f'Section {self.content}'

class GalleryImage(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery_images/')
    thumbnail = models.ImageField(upload_to='gallery_images/thumbnails/', editable=False, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True)
    is_featured = models.BooleanField(default=False)
    marked_for_deletion = models.BooleanField(default=False)  # New field to track deletion

    def __str__(self):
        return self.title or f'Image for {self.page.title}'

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Check if this is a new instance
        super().save(*args, **kwargs)

        # Generate and save thumbnail if it's a new instance or if the image has changed
        if self.image and (not self.thumbnail or self.image_changed() or is_new):
            thumbnail_content = self.make_thumbnail(self.image, size=(400, 400))  # Set max size to 400px
            thumbnail_name = self.generate_thumbnail_name()
            self.thumbnail.save(thumbnail_name, thumbnail_content, save=False)
            super().save(update_fields=['thumbnail'])  # Only save the thumbnail field

    def image_changed(self):
        try:
            old_instance = GalleryImage.objects.get(pk=self.pk)
            return old_instance.image != self.image
        except GalleryImage.DoesNotExist:
            return True

    def make_thumbnail(self, image, size=(400, 400)):
        """
        Generate a high-quality, compressed thumbnail with max dimensions of 400x400.
        Corrects orientation based on EXIF data before resizing.
        """
        # Open the image and correct orientation based on EXIF data
        img = Image.open(image)
        
        # Handle EXIF orientation data
        try:
            exif = img._getexif()
            if exif is not None:
                for tag, value in exif.items():
                    if ExifTags.TAGS.get(tag, tag) == 'Orientation':
                        if value == 3:
                            img = img.rotate(180, expand=True)
                        elif value == 6:
                            img = img.rotate(270, expand=True)
                        elif value == 8:
                            img = img.rotate(90, expand=True)
        except (AttributeError, KeyError, IndexError):
            pass  # EXIF data is not present or could not be processed

        # Convert the image to RGB if it's in RGBA or other formats
        img = img.convert("RGB")

        # Resize the image while maintaining aspect ratio
        img.thumbnail(size, Image.LANCZOS)

        # Save the thumbnail to a BytesIO object with optimized quality
        thumb_io = BytesIO()
        img.save(thumb_io, format='JPEG', quality=100, optimize=True)

        return ContentFile(thumb_io.getvalue())

    def generate_thumbnail_name(self):
        """
        Generate a name for the thumbnail.
        """
        base_name = self.image.name.split('/')[-1]
        thumb_name = f"thumb_{base_name}"
        return thumb_name
    
# Signal to auto-generate unique slug if not provided
@receiver(pre_save, sender=Page)
def auto_generate_slug(sender, instance, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.title)
        slug = base_slug
        count = 1
        
        # Ensure the slug is unique by appending a number if needed
        while Page.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{count}"
            count += 1
            
        instance.slug = slug

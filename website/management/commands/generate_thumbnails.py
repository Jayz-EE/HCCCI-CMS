from django.core.management.base import BaseCommand
from django.conf import settings
from website.models import GalleryImage
from PIL import Image, ExifTags
from django.core.files.base import ContentFile
import os
import io
from django.db.models import Q

class Command(BaseCommand):
    help = 'Generate thumbnails for existing images in the gallery.'

    def handle(self, *args, **kwargs):
        # Define the desired height for the thumbnail
        thumbnail_height = 400
        quality = 85  # Adjust quality as needed for balance of file size and visual quality

        # Query all images that don't have a thumbnail
        images_without_thumbnails = GalleryImage.objects.filter(Q(thumbnail="") | Q(thumbnail__isnull=True))

        # Check if any images are found
        if not images_without_thumbnails.exists():
            self.stdout.write(self.style.WARNING("No images found without thumbnails."))
            return

        for image_obj in images_without_thumbnails:
            # Get the image path
            image_path = image_obj.image.path
            self.stdout.write(f"Processing image: {image_path} (ID: {image_obj.id})")

            # Open the original image
            try:
                with Image.open(image_path) as img:
                    # Check for EXIF orientation and apply it
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
                        pass  # EXIF not present or couldn't be processed

                    # Ensure thumbnail directory exists
                    thumbnail_dir = os.path.join(settings.MEDIA_ROOT, 'gallery_images/thumbnails')
                    if not os.path.exists(thumbnail_dir):
                        os.makedirs(thumbnail_dir)
                        self.stdout.write(f"Created thumbnail directory: {thumbnail_dir}")

                    # Convert image to RGB if it's in a different mode (e.g., PNG with transparency)
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    
                    # Calculate the width to maintain aspect ratio while setting the height to 400
                    width_percent = (thumbnail_height / float(img.size[1]))  # Calculate the ratio
                    thumbnail_width = int((float(img.size[0]) * float(width_percent)))

                    # Resize the image to the new dimensions while maintaining aspect ratio
                    img = img.resize((thumbnail_width, thumbnail_height), Image.LANCZOS)

                    # Save the thumbnail to a BytesIO object
                    thumbnail_io = io.BytesIO()
                    img.save(thumbnail_io, format='JPEG', quality=quality, optimize=True)

                    # Create a ContentFile from the BytesIO object for Django to save
                    thumbnail_filename = f"thumb_{os.path.basename(image_path)}"
                    thumbnail_content = ContentFile(thumbnail_io.getvalue(), name=thumbnail_filename)

                    # Save thumbnail to the model instance and save the instance
                    image_obj.thumbnail.save(thumbnail_filename, thumbnail_content)
                    image_obj.save()

                    self.stdout.write(self.style.SUCCESS(f'Thumbnail created and saved for {image_obj.id}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to create thumbnail for {image_obj.id}: {e}'))

        self.stdout.write(self.style.SUCCESS("Thumbnail generation completed."))

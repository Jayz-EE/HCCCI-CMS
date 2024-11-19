from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import *
from .forms import *
import csv
import json
from django.http import JsonResponse
from django.template.loader import render_to_string 
from django.views.decorators.csrf import csrf_exempt
import sqlite3
from django.http import HttpResponse
import os
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils.text import slugify
from django.db import connection
from django.utils.timezone import make_aware
from datetime import datetime
from django.utils.timezone import make_aware, is_aware
from django.utils import timezone

# Home page view
def Home(request):
    return render(request, 'website/Home.html', {})

# About page view
def aboutHCCCI(request):
    return render(request, 'website/aboutHCCCI.html', {})

def enrollment(request):
    return render(request, 'website/enrollment.html', {})

def paymentprocess(request):
    return render(request, 'website/paymentprocess.html', {})

def programsofferred(request):
    return render(request, 'website/programsofferred.html', {})

def faq(request):
    return render(request, 'website/faq.html', {})

def Elibrary(request):
    return render(request, 'website/Elibrary.html', {})

@login_required
def cms_dashboard(request):
    # Fetch all pages and order by creation date
    pages_list = Page.objects.all().order_by('-created_at')

    # Check if the user is a superuser
    is_superuser = request.user.is_superuser

    # Render the template with all pages, no pagination needed, and superuser status
    return render(request, 'cms_plugins/cms_dashboard.html', {
        'pages': pages_list,
        'is_superuser': is_superuser,
    })

@login_required
def create_page(request):
    if request.method == 'POST':
        page_form = PageForm(request.POST)
        content_sections_data = request.POST.getlist('content[]')
        
        if page_form.is_valid():
            # Create the page instance without saving it immediately
            page = page_form.save(commit=False)

            # Manually set the created_at and updated_at fields
            page.created_at = timezone.now()  # Set created_at manually
            page.updated_at = timezone.now()  # Set updated_at manually

            # Save the page
            page.save()

            # Save content sections
            for content in content_sections_data:
                if content.strip():
                    ContentSection.objects.create(page=page, content=content)

            # Handle multiple gallery images upload
            files = request.FILES.getlist('gallery_images')
            image_ids = request.POST.get('image_ids', '').split(',')
            featured_image_id = request.POST.get('featured_image')

            if len(files) != len(image_ids):
                messages.error(request, 'Number of uploaded files does not match the number of image IDs.')
                return render(request, 'cms_plugins/create_page.html', {'form': page_form})

            # Validate that the featured_image_id exists in image_ids
            if featured_image_id and featured_image_id not in image_ids:
                messages.error(request, 'Selected featured image does not exist.')
                return render(request, 'cms_plugins/create_page.html', {'form': page_form})

            # Create gallery images and set the featured image
            for file, image_id in zip(files, image_ids):
                gallery_image = GalleryImage.objects.create(page=page, image=file)

                # Set the selected image as featured based on the user selection
                if image_id == featured_image_id:
                    gallery_image.is_featured = True
                    gallery_image.save()

            messages.success(request, 'Page and images created successfully with featured image!')
            return redirect('cms_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        page_form = PageForm()

    return render(request, 'cms_plugins/create_page.html', {'form': page_form})

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify
from .models import Page, ContentSection, GalleryImage
from .forms import PageForm


@login_required
def edit_page(request, slug):
    # Retrieve the page based on the slug without filtering by user
    page = get_object_or_404(Page, slug=slug)
    page_contentsection = ContentSection.objects.filter(page=page)
    active_gallery_images = page.galleryimage_set.filter(marked_for_deletion=False)
    marked_as_gallery_images = page.galleryimage_set.filter(marked_for_deletion=True)

    if request.method == 'POST':
        form = PageForm(request.POST, instance=page)
        content_sections_data = request.POST.getlist('content[]')

        if form.is_valid():
            # Get the new title and slugify it
            new_title = form.cleaned_data['title']

            # Update slug only if the title has changed
            if new_title != page.title:
                new_slug = slugify(new_title)  # Create a new slug from the title

                # Check for slug duplication and resolve it
                original_slug = new_slug
                counter = 1
                while Page.objects.filter(slug=new_slug).exclude(id=page.id).exists():
                    new_slug = f"{original_slug}-{counter}"
                    counter += 1

                # Update the page slug with the unique slug
                page.slug = new_slug

            # Save the page with the updated title (and slug if changed)
            page.title = new_title
            page.save()

            # Clear existing sections and save new ones
            page.contentsection_set.all().delete()
            for content in content_sections_data:
                if content.strip():
                    ContentSection.objects.create(page=page, content=content)

            # Handle gallery image uploads
            files = request.FILES.getlist('gallery_images')
            featured_image_index = request.POST.get('featured_image', -1)  # Get the index of the featured image

            # Ensure the index is an integer or set it to -1 if it's empty
            try:
                featured_image_index = int(featured_image_index) if featured_image_index else -1
            except ValueError:
                featured_image_index = -1  # Default to -1 on error
            
            # Debugging: Log the featured image index and files
            print("Featured Image Index: ", featured_image_index)
            print("Files Uploaded: ", files)

            # Check if a new featured image is selected
            if featured_image_index != -1 and len(files) > featured_image_index:
                # Remove all featured images for the page before setting the new one
                page.galleryimage_set.update(is_featured=False)

                # Create new gallery images
                for index, file in enumerate(files):
                    gallery_image = GalleryImage.objects.create(page=page, image=file)

                    # Set the selected image as featured based on the user selection
                    if index == featured_image_index:
                        gallery_image.is_featured = True
                        gallery_image.save()
                        # Debugging: Confirm which image is marked as featured
                        print(f"Image {gallery_image.id} marked as featured.")
            else:
                # If no new featured image is set, just upload images without changing featured status
                for file in files:
                    GalleryImage.objects.create(page=page, image=file)

            messages.success(request, 'Page updated successfully!')
            return redirect('cms_dashboard')  # Redirect to the cms_dashboard

    else:
        form = PageForm(instance=page)

    return render(request, 'cms_plugins/edit_page.html', {
        'form': form,
        'page': page,
        'active_gallery_images': active_gallery_images,
        'marked_as_gallery_images': marked_as_gallery_images,
    })

@login_required
def delete_page(request, slug):
    page = get_object_or_404(Page, slug=slug)  # No user filter applied

    if request.method == 'POST':
        # Delete associated gallery images and their thumbnails
        gallery_images = GalleryImage.objects.filter(page=page)

        for image in gallery_images:
            # Delete the thumbnail if it exists
            if image.thumbnail:
                # Remove the thumbnail from the media storage
                thumbnail_path = image.thumbnail.path
                if os.path.exists(thumbnail_path):
                    os.remove(thumbnail_path)
            
            # Delete the image file itself
            if image.image:
                image_path = image.image.path
                if os.path.exists(image_path):
                    os.remove(image_path)

            # Delete the image record from the database
            image.delete()

        # Now delete the page itself
        page.delete()

        messages.success(request, 'Page and associated gallery images deleted successfully!')
        return redirect('cms_dashboard')

    return render(request, 'cms_plugins/delete_page.html', {'page': page})

# Add images to a page's gallery
@login_required
def add_gallery_image(request, slug):
    page = get_object_or_404(Page, slug=slug)  # No user filter applied
    if request.method == 'POST':
        form = GalleryImageForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('image')
            for file in files:
                GalleryImage.objects.create(page=page, image=file)
            messages.success(request, 'Image added to gallery successfully!')
            return redirect('edit_page', slug=page.slug)
    else:
        form = GalleryImageForm()
    return render(request, 'cms_plugins/add_gallery_image.html', {'form': form, 'page': page})

# Logout view
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required
def delete_selected_images(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        image_ids = data.get('image_ids', [])

        # Permanently delete images with the given IDs
        GalleryImage.objects.filter(id__in=image_ids).delete()

        return JsonResponse({'success': True, 'message': 'Selected images have been permanently deleted.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

# Mark as Deleted an Image from Gallery
@login_required
def mark_as_delete_image(request, image_id):
    image = get_object_or_404(GalleryImage, id=image_id)  # No user filter applied
    if request.method == 'POST':
        image.marked_for_deletion = True
        image.save()
        messages.success(request, 'Image marked for deletion.')
        return JsonResponse({'success': True, 'message': 'Image was Marked as Deleted.'})
    return JsonResponse({'success': False, 'message': 'Invalid request.'})

# Set as Featured Image
@login_required
def set_featured_image(request, image_id):
    image = get_object_or_404(GalleryImage, id=image_id)  # No user filter applied
    # Set all other images in the gallery to not featured
    GalleryImage.objects.filter(page=image.page).update(is_featured=False)
    # Set the selected image as featured
    image.is_featured = True
    image.save()
    messages.success(request, 'Featured image updated successfully!')
    return JsonResponse({'success': True, 'message': 'Featured image updated successfully!'})

# Page detail view with Previous and Next Article functionality in latest-first order
def page_detail(request, slug):
    # Get the current page based on the slug
    page = get_object_or_404(Page, slug=slug)

    # Retrieve gallery images and content sections
    gallery_images = page.galleryimage_set.filter(marked_for_deletion=False)
    content_sections = page.contentsection_set.all()
    
    # Find the next page (created before the current page in descending order)
    next_page = Page.objects.filter(
        created_at__lt=page.created_at
    ).order_by('-created_at').first()

    # Find the previous page (created after the current page in descending order)
    previous_page = Page.objects.filter(
        created_at__gt=page.created_at
    ).order_by('created_at').first()
    
    # Pass these pages to the template
    return render(request, 'cms_plugins/page_details.html', {
        'page': page,
        'gallery_images': gallery_images,
        'content_sections': content_sections,
        'previous_page': previous_page,
        'next_page': next_page
    })

# Restores Marked as Deleted Image from Gallery
@login_required
def restore_gallery_image(request, image_id):
    image = get_object_or_404(GalleryImage, id=image_id)  # No user filter applied

    if request.method == 'POST':
        # Restore the image by updating its marked_for_deletion field
        image.marked_for_deletion = False
        image.save()
        
        # Return a success response
        messages.success(request, 'Image restored successfully!')
        return JsonResponse({'success': True, 'message': 'Image has been restored.'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request.'})

@login_required
def update_gallery_and_trash(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Safely parse JSON data
            slug = data.get('slug')  # Extract the slug

            # Get the page based on the slug
            page = get_object_or_404(Page, slug=slug)

            # Fetch active and deleted gallery images
            active_gallery_images = page.galleryimage_set.filter(marked_for_deletion=False)
            marked_as_gallery_images = page.galleryimage_set.filter(marked_for_deletion=True)

            # Render the updated HTML for both containers
            gallery = render_to_string('cms_plugins/manage_gallery.html', {'active_gallery_images': active_gallery_images, 'marked_as_gallery_images': marked_as_gallery_images})

            return JsonResponse({
                'gallery': gallery,
                'success': True
            })
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON format.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def news_card_view(request):
    pages = Page.objects.all().order_by('-created_at')   # Fetch all pages

    # Prepare a list of pages with their featured images
    pages_with_images = []
    for page in pages:
        # Get featured images
        featured_images = page.galleryimage_set.filter(is_featured=True)

        # Select the first featured image if it exists
        if featured_images.exists():
            featured_image = featured_images.first().thumbnail.url
        else:
            # If no featured image, select the first image in the gallery that is not marked as deleted
            first_image = page.galleryimage_set.filter(marked_for_deletion=False).first()
            featured_image = first_image.thumbnail.url if first_image else None

        # Append the page details along with the featured image URL
        pages_with_images.append({
            'title': page.title,
            'slug': page.slug,
            'content': page.contentsection_set.first().content if page.contentsection_set.exists() else '',
            'featured_image': featured_image,
        })

    # Return a JSON response
    return JsonResponse({'pages_with_images': pages_with_images})

def news_updates(request):
    # Fetch all pages sorted by created_at in descending order
    pages = Page.objects.all().order_by('-created_at') 

    # Prepare a list of pages with their featured images
    pages_with_images = []
    for page in pages:
        # Get featured images
        featured_images = page.galleryimage_set.filter(is_featured=True)
        
        # Select the first featured image if it exists
        if featured_images.exists():
            featured_image = featured_images.first().thumbnail.url
        else:
            # If no featured image, select the first image in the gallery if available
            first_image = page.galleryimage_set.first()
            featured_image = first_image.thumbnail.url if first_image else None
        
        # Append the page details along with the featured image URL
        pages_with_images.append({
            'title': page.title,
            'slug': page.slug,
            'content': page.contentsection_set.first().content if page.contentsection_set.exists() else '',
            'featured_image': featured_image,
        })

    # Render the template with the list of pages and their images
    return render(request, 'website/news_update.html', {'pages_with_images': pages_with_images})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Welcome back, {}!'.format(user.username))
            
            # Get the next parameter from the request or fallback to the cms_dashboard
            next_url = request.GET.get('next', 'cms_dashboard')
            return redirect(next_url)  # Redirect to 'next' or 'cms_dashboard' if 'next' is not provided
    else:
        form = CustomLoginForm()

    return render(request, 'cms_plugins/login.html', {'form': form})

def logout_user(request):
    logout(request)

    return redirect('login')

def session_timeout(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login if session has expired
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def news_ticker(request):
    try:
        # Fetch the latest Page object based on `created_at`
        latest_page = Page.objects.latest('created_at')
        page_title = latest_page.title
        page_slug = latest_page.slug  # Get the slug to create a link
    except Page.DoesNotExist:
        # If no pages exist, set default values
        page_title = "No pages available"
        page_slug = None

    # Return the title and slug as JSON response
    return JsonResponse({'page_title': page_title, 'page_slug': page_slug})

@csrf_exempt
def check_register_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            entered_password = data.get("password")
            
            # Fetch the stored security password (assuming there's only one)
            stored_password = RegisterPassword.objects.first()
            
            # Ensure exact match by comparing the entered password with the stored password
            if stored_password and entered_password == stored_password.RegisterPass:
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False, "error": "Incorrect security password."})
                
        except RegisterPassword.DoesNotExist:
            return JsonResponse({"success": False, "error": "No register password found."})
    return JsonResponse({"success": False, "error": "Invalid request method."})

def register_view(request):
    # Check if the user has already verified the security password
    if not request.session.get('is_verified', False):
        if request.method == "POST":
            # Verify the entered security password
            password = request.POST.get("security_password", "")
            try:
                correct_password = RegisterPassword.objects.get(id=1).RegisterPass
                if password == correct_password:
                    # Set session variable to indicate successful verification
                    request.session['is_verified'] = True
                    return redirect('register_view')  # Redirect to the same view to load the registration form
                else:
                    # Incorrect password, show security form with error message
                    return render(request, 'cms_plugins/register_password.html', {'error': 'Incorrect security password.'})
            except RegisterPassword.DoesNotExist:
                return JsonResponse({'error': 'Security password not set up.'})
        
        # If GET request or not verified, show the security password form
        return render(request, 'cms_plugins/register_password.html')

    # If already verified, show the registration form
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email')

            # Check if is_superuser is True, set is_staff to True as well
            if user.is_superuser:
                user.is_staff = True

            user.save()
            # Clear the session verification after successful registration
            request.session.pop('is_verified', None)
            return redirect('cms_dashboard')
    else:
        form = CustomUserCreationForm()

    return render(request, 'cms_plugins/register.html', {'form': form})

def clear_session_and_redirect(request):
    logout(request)  # This clears the session, including sessionid
    return redirect('/cms/register/') 

# def update_created_at(request):
#     return render(request, 'cms_plugins/updated_page_created_at.html', {})

# def update_pages(request):
#     # Set the timezone to Philippine Time (UTC+8)
#     philippine_timezone = pytz.timezone('Asia/Manila')
    
#     # Get the current time in Philippine timezone
#     current_time = timezone.now().astimezone(philippine_timezone)

#     # Get all pages ordered by created_at in descending order
#     pages = Page.objects.all().order_by('-id')

#     # Iterate through each page and update the created_at with a 10-second difference
#     for page in pages:
#         # Set created_at to the current time in Philippine timezone
#         page.created_at = current_time
#         page.save()

#         # Increment the time by 10 seconds for the next page
#         current_time += timezone.timedelta(seconds=10)

#     # Redirect to the 'page_list' view after updating all pages
#     return redirect('/cms/')

@login_required
def manage_account(request):
    password = RegisterPassword.objects.first()  # Modify to fetch the correct password if needed
    users = CustomUser.objects.all()
    return render(request, 'cms_plugins/accounts.html', {'users': users, 'RegisterPassword': password})

@login_required
def update_register_password(request):
    if request.method == 'POST':
        try:
            # Parse the request body (JSON)
            data = json.loads(request.body)
            new_password = data.get('password')

            if new_password:
                # Assuming there is only one record, you can fetch it as shown
                password = RegisterPassword.objects.first()
                password.RegisterPass = new_password
                password.save()

                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Password is required.'})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    # If it's a GET request or other method, return the password management form
    password = RegisterPassword.objects.first()
    return render(request, 'cms_plugins/accounts.html', {})

@login_required
def delete_user_account(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    # Prevent deletion if the user is a superuser
    if user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Cannot delete a superuser account.'}, status=403)

    if request.method == 'POST':
        try:
            user.delete()  
            return JsonResponse({'success': True})
        except Exception as e:  
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
def get_users(request):
    # Fetch all users or apply any filters you need
    users = CustomUser.objects.all()
    user_list = [
        {
            'id': user.id,
            'fname': user.first_name,
            'lname': user.last_name,
            'username': user.username,
        }
        for user in users
    ]
    return JsonResponse({'users': user_list})

@login_required
def backup_database(request):
    # Create a response with the appropriate content type for JSON files
    response = HttpResponse(content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename=db_backup.json'

    # Create a dictionary to hold all the models' data
    all_data = {}

    # Loop through models only in the 'website' app
    for model in apps.get_models():
        if model._meta.app_label != 'website':
            continue

        # Create a queryset for the model
        queryset = model.objects.all()

        if queryset.exists():
            # Create a list to store the model's data
            data = []

            # Iterate over each object in the queryset
            for obj in queryset:
                # Create a dictionary of values for each field in the object
                row = {}

                # Loop through all fields and check if they should be included
                for field in model._meta.get_fields():
                    field_name = field.name

                    # Skip fields that are not editable or hidden
                    if not field.editable:
                        continue

                    value = getattr(obj, field_name, None)  # Get the value of the field from the object
                    
                    # Handle ForeignKey relationships (one-to-many or one-to-one)
                    if isinstance(field, models.ForeignKey) and value:
                        related_obj = value
                        value = related_obj.id  # Store the ID of the related object
                    
                    # Add the value to the row dictionary
                    row[field_name] = value

                # Ensure that created_at and updated_at are included
                if hasattr(obj, 'created_at'):
                    row['created_at'] = obj.created_at
                if hasattr(obj, 'updated_at'):
                    row['updated_at'] = obj.updated_at

                # Add this row to the data list
                data.append(row)

            # Add this model's data to the all_data dictionary
            model_name = model._meta.model_name
            all_data[model_name] = data

    # Convert the all_data dictionary to JSON and write it to the response with indentation
    json_data = json.dumps(all_data, default=str, ensure_ascii=False, indent=4)
    response.write(json_data)

    return response

def reset_all_sequences():
    # Get the list of all table names in the 'website' app
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name LIKE 'website_%'
        """)

        tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            try:
                # Get the sequence name for the table's primary key
                cursor.execute(f"SELECT pg_get_serial_sequence('{table_name}', 'id')")
                sequence_name = cursor.fetchone()[0]
                
                if sequence_name:
                    # Reset the sequence based on the max id value in the table
                    cursor.execute(f"""
                        SELECT setval('{sequence_name}', (SELECT MAX(id) FROM {table_name}) + 1)
                    """)
                    print(f"Sequence for {table_name} has been reset.")
                else:
                    print(f"No sequence found for {table_name}. Skipping.")
            except Exception as e:
                print(f"Error resetting sequence for {table_name}: {str(e)}")

@login_required
def import_database(request):
    if request.method == 'POST' and request.FILES.get('json_file'):
        # Get the uploaded file
        json_file = request.FILES.get('json_file')

        try:
            # Read and decode the JSON file
            decoded_file = json_file.read().decode('utf-8')
            data = json.loads(decoded_file)  # Load JSON data into Python dict

            # Loop through the data for each model
            with transaction.atomic():  # Use atomic transaction to ensure rollback on error
                for table_name, records in data.items():
                    try:
                        # Get the model class dynamically using the correct app label and model name
                        model = apps.get_model('website', table_name)  # Using 'website' app

                        # Loop through each record for the model
                        for record in records:
                            pk = record.get('id')
                            fields = {key: value for key, value in record.items() if key != 'id'}

                            # Handle created_at and updated_at fields
                            created_at = record.get('created_at', None)
                            updated_at = record.get('updated_at', None)
                            
                            # Handle created_at and updated_at manually
                            if created_at:
                                if isinstance(created_at, str):
                                    try:
                                        created_at = datetime.fromisoformat(created_at)
                                    except ValueError as e:
                                        return JsonResponse({
                                            'status': 'error',
                                            'message': f"Error parsing 'created_at' value: {str(e)}"
                                        }, status=400)
                                if not is_aware(created_at):
                                    created_at = make_aware(created_at)
                                fields['created_at'] = created_at

                            if updated_at:
                                if isinstance(updated_at, str):
                                    try:
                                        updated_at = datetime.fromisoformat(updated_at)
                                    except ValueError as e:
                                        return JsonResponse({
                                            'status': 'error',
                                            'message': f"Error parsing 'updated_at' value: {str(e)}"
                                        }, status=400)
                                if not is_aware(updated_at):
                                    updated_at = make_aware(updated_at)
                                fields['updated_at'] = updated_at

                            # Handle ForeignKey relationships
                            for field, value in fields.items():
                                field_obj = model._meta.get_field(field)
                                if isinstance(field_obj, models.ForeignKey):
                                    try:
                                        # If the field is a ForeignKey, we fetch the related object by ID
                                        related_model = field_obj.related_model
                                        related_obj = related_model.objects.get(id=value)

                                        fields[field] = related_obj  # Assign the related object

                                    except ObjectDoesNotExist:
                                        return JsonResponse({
                                            'status': 'error',
                                            'message': f"Related object for field '{field}' with ID {value} does not exist in {related_model.__name__}."
                                        }, status=400)
                                    except Exception as ex:
                                        return JsonResponse({
                                            'status': 'error',
                                            'message': f"Error fetching related object for '{field}' with ID {value}: {str(ex)}"
                                        }, status=400)

                            # Check if the object already exists by primary key
                            obj = model.objects.filter(pk=pk).first()

                            if obj:  # If object exists, update it
                                print(f"Updating existing {table_name} with ID {pk} and fields {fields}")
                                for field, value in fields.items():
                                    setattr(obj, field, value)
                                obj.save()
                            else:  # If the object does not exist, create a new one
                                print(f"Creating new fields {fields}")
                                obj = model.objects.create(pk=pk, **fields)

                            # Save the object (if created or updated)
                            obj.save()

                    except Exception as e:
                        return JsonResponse({
                            'status': 'error',
                            'message': f"Error processing table {table_name}: {str(e)}"
                        }, status=400)
                    
            reset_all_sequences()

            return JsonResponse({
                'status': 'success',
                'message': 'Database import successful.'
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Error importing JSON: {str(e)}'
            }, status=400)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'No file uploaded.'
        }, status=400)
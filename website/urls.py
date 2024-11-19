from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', Home, name='Home'),
    path('aboutHCCCI/', aboutHCCCI, name='aboutHCCCI'),
    path('enrollment/', enrollment, name='enrollment'),
    path('news-updates/', news_updates, name='news_updates'),
    path('paymentprocess/', paymentprocess, name='paymentprocess'),
    path('programsofferred/', programsofferred, name='programsofferred'),
    path('Elibrary/', Elibrary, name='Elibrary'),
    path('faq/', faq, name='faq'),
    
    path('cms/', cms_dashboard, name='cms_dashboard'),
    path('cms/create/', create_page, name='create_page'),
    path('logout/', logout_user, name='logout_user'),
    path('cms/login/', login_view, name='login'),
    path('cms/logout/', logout_view, name='logout'),

    path('cms/register/', register_view, name='register_view'),
    path('check-register-password/', check_register_password, name='check_register_password'),

    # Display and Edit Content_Page or Add Images to Gallery
    path('cms/edit/<slug:slug>/', edit_page, name='edit_page'),
    
    path('cms/delete/<slug:slug>/', delete_page, name='delete_page'),
    path('page/<slug:slug>/', page_detail, name='page_detail'), 

    path('news_ticker/', news_ticker, name='news_ticker'),

    # Separate Fetch for Adding an Image to Gallery
    path('cms/gallery/add/<slug:slug>/', add_gallery_image, name='add_gallery_image'), 

    # Permanently Delete an Image rather than Marking it for Deletion
    path('cms/gallery/delete-selected/', delete_selected_images, name='delete_selected_images'),

    # Sets the Image as Mark for Deletion
    path('cms/gallery/mark_as_delete_image/<int:image_id>/', mark_as_delete_image, name='mark_as_delete_image'),

    # Restore an Image that is Marked for Deletion
    path('cms/gallery/restore/<int:image_id>/', restore_gallery_image, name='restore_gallery_image'),

    #Updates Gallery
    path('cms/gallery/update/', update_gallery_and_trash, name='update_gallery_and_trash'),

    # Feature an Image
    path('cms/gallery/feature/<int:image_id>/', set_featured_image, name='set_featured_image'),

    # News Cards
    path('news/', news_card_view, name='news_card_view'),

    # Session Clear
    path('clear-session/', clear_session_and_redirect, name='clear_session'),

    # Arrange the Order of News Update Display
    # path('update_created_at/', update_created_at, name='update_created_at'),

    # path('update-pages/', update_pages, name='update_pages')

    # Manage Account
    path('cms/manage_account/', manage_account, name="manage_account"),

    # Update Security Password
    path('update-password/', update_register_password, name='update-password'),

    # Delete User Account 
    path('delete_user_account/<int:user_id>/', delete_user_account, name='delete_user_account'),

    # Fetch Users Data
    path('cms/get_users/', get_users, name='get_users'),

    # Backup Database
    path('cms/backup/', backup_database, name='backup_database'),

    # # Import Database
    path('cms/import/', import_database, name='import_database'),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

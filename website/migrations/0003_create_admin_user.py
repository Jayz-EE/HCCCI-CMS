from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_admin_user(apps, schema_editor):  # No need for schema_editor
    CustomUser = apps.get_model('website', 'CustomUser')  # Your app's model

    # Check if the admin user already exists
    if not CustomUser.objects.filter(username="admin").exists():
        # If the admin user does not exist, create it
        admin_user = CustomUser(
            username="admin",
            first_name="admin",
            last_name="admin",
            email="",  # Can be left blank
            password=make_password("@Classify24#"),  # Hash the password
            is_superuser=True,
            is_staff=True
        )
        admin_user.save()

class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_create_registerpassword'),  # Modify as needed to your last migration
    ]

    operations = [
        migrations.RunPython(create_admin_user),
    ]
from django.db import migrations

def create_register_password(apps, _):  # Remove schema_editor as it's not needed
    RegisterPassword = apps.get_model('website', 'RegisterPassword')
    
    # Check if the table is empty
    if RegisterPassword.objects.count() == 0:
        # Insert the default value if no records exist
        RegisterPassword.objects.create(RegisterPass="@Classify_2024")

class Migration(migrations.Migration):

    # Corrected dependencies: this ensures the migration is the first one
    dependencies = [
        ('website', '0001_initial'),  # Ensure this is the correct initial migration of the 'website' app
    ]

    operations = [
        migrations.RunPython(create_register_password),
    ]

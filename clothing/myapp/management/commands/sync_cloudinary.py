import os
from django.core.management.base import BaseCommand
from django.conf import settings
from myapp.models import Clothes

class Command(BaseCommand):
    help = 'Upload local product images to Cloudinary if Cloudinary credentials are set'

    def handle(self, *args, **kwargs):
        cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME')
        api_key = os.environ.get('CLOUDINARY_API_KEY')
        api_secret = os.environ.get('CLOUDINARY_API_SECRET')

        if not (cloud_name and api_key and api_secret):
            self.stdout.write(self.style.WARNING("Cloudinary environment variables not configured. Skipping sync."))
            return

        try:
            import cloudinary
            import cloudinary.uploader

            cloudinary.config(
                cloud_name=cloud_name,
                api_key=api_key,
                api_secret=api_secret
            )

            self.stdout.write("Checking product images for Cloudinary upload...")
            for item in Clothes.objects.all():
                if item.image:
                    file_name = str(item.image.name)
                    local_path = os.path.join(settings.MEDIA_ROOT, file_name)
                    if os.path.exists(local_path):
                        self.stdout.write(f"Uploading {file_name} to Cloudinary...")
                        res = cloudinary.uploader.upload(
                            local_path,
                            public_id=file_name,
                            overwrite=True
                        )
                        self.stdout.write(self.style.SUCCESS(f"Successfully uploaded {file_name}: {res.get('secure_url')}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error during Cloudinary sync: {e}"))

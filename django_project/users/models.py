from PIL import Image
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """
    User`s Profile Model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        """
        Resizes profile image if its too bog
        """
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 255 or img.width > 255:
            output_size = (255, 255)
            img.thumbnail(output_size)
            img.save(self.image.path)

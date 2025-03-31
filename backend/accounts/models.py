from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True) 
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    area_of_interest = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=50, blank=False, null=False)  # ✅ Required First Name
    last_name = models.CharField(max_length=50, blank=False, null=False)  # ✅ Required Last Name

    USERNAME_FIELD = 'email'  # ✅ Use email for authentication
    REQUIRED_FIELDS = ['first_name', 'last_name']  # ✅ Required during registration

    def save(self, *args, **kwargs):
        """ Auto-generate a unique username based on first_name and last_name """
        if not self.username:
            base_username = slugify(f"{self.first_name}_{self.last_name}")  # Convert to URL-friendly format
            new_username = base_username
            counter = 1
            
            # Ensure the username is unique by appending a number if needed
            while CustomUser.objects.filter(username=new_username).exists():
                new_username = f"{base_username}{counter}"
                counter += 1
            
            self.username = new_username  # Set final username

        super().save(*args, **kwargs)  # Call parent save method

    def __str__(self):
        return self.email  # ✅ Use email as the string representation

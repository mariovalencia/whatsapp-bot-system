from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.email or self.username
    
    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True
        return self.userrole_set.filter(role__rolepermission__permission__code=perm).exists()
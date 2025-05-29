from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm_code):
        return self.userrole_set.filter(role__rolepermission__permission__code=perm_code).exists()
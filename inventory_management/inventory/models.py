# inventory/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'user'
        unique_together = ('email',)
        permissions = (("can_view_inventory", "Can View Inventory"),)

    # Change related_name to avoid clashes with Django's default User
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='inventory_user_set',  # Custom related name
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='inventory_user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='inventory_user_set',  # Custom related name
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='inventory_user'
    )

    def __str__(self):
        return self.email

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'item'
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_item_name')
        ]

    def __str__(self):
        return self.name

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Max

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    dob = models.DateField()
    mobile_number = models.CharField(max_length=15, blank=True,)
    is_admin = models.BooleanField(default=False)
    is_customized_by_admin = models.BooleanField(default=False)


    # Feature-based permissions
    can_add_category = models.BooleanField(default=True)
    can_edit_category = models.BooleanField(default=True)
    can_delete_category = models.BooleanField(default=True)

    can_add_item = models.BooleanField(default=True)
    can_edit_item = models.BooleanField(default=True)
    can_delete_item = models.BooleanField(default=True)

    can_add_sale = models.BooleanField(default=True)
    can_edit_sale = models.BooleanField(default=True)
    can_delete_sale = models.BooleanField(default=True)

    can_access_category_page = models.BooleanField(default=True)
    can_access_item_page = models.BooleanField(default=True)
    can_access_sales_page = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    STATUS_CHOICES = [(1, 'Active'), (0, 'Inactive')]
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Item(models.Model):
    STATUS_CHOICES = [(1, 'Active'), (0, 'Inactive')]
    name = models.CharField(max_length=100) 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(default=0)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        self.status = 1 if self.quantity > 0 and self.price > 0 else 0
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Sales(models.Model):
    PAYMENT_MODE_CHOICES = [('Cash', 'Cash'), ('Online', 'Online')]
    STATUS_CHOICES = [(1, 'Active'), (0, 'Inactive')]

    bill_number = models.CharField(max_length=50, unique=True, blank=True)
    date = models.DateField(default=timezone.now)
    customer_name = models.CharField(max_length=100)
    payment_mode = models.CharField(max_length=10, choices=PAYMENT_MODE_CHOICES, default='Cash')
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        if not self.bill_number:
            super().save(*args, **kwargs)  # First save to get ID
            self.bill_number = f'BILL-{self.id:04d}'
            super().save(update_fields=['bill_number'])
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.bill_number} - {self.customer_name}"





class SaleItem(models.Model):
    sales = models.ForeignKey(Sales, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
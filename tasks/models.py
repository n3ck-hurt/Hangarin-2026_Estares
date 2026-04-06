from django.db import models
from django.utils import timezone

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class ArmoryCategory(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Armory Categories"

class Supplier(BaseModel):
    name = models.CharField(max_length=200, unique=True)
    country = models.CharField(max_length=100)
    reliability_score = models.IntegerField(default=100) # 0-100
    
    def __str__(self):
        return f"{self.name} ({self.country})"

class Weapon(BaseModel):
    name = models.CharField(max_length=200)
    model_number = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(ArmoryCategory, on_delete=models.CASCADE, related_name='weapons')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='weapons')
    caliber = models.CharField(max_length=50, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {self.model_number}"

class Client(BaseModel):
    name = models.CharField(max_length=200)
    region = models.CharField(max_length=100)
    clearance_level = models.IntegerField(default=1) # 1-5
    total_spent = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.name} [{self.region}]"

class Transaction(BaseModel):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='transactions')
    weapon = models.ForeignKey(Weapon, on_delete=models.CASCADE, related_name='transactions')
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")
    deal_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Deal #{self.id} - {self.client.name}"

class IntelligenceNote(BaseModel):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='intel_notes')
    content = models.TextField()
    
    def __str__(self):
        return f"Intel for Deal #{self.transaction.id}"
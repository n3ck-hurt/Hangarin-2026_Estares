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
    reliability_score = models.IntegerField(default=100, help_text="Reliability score from 1-100")
    
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
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {self.model_number}"
    
    class Meta:
        ordering = ['-created_at']

class Client(BaseModel):
    name = models.CharField(max_length=200)
    region = models.CharField(max_length=100)
    clearance_level = models.IntegerField(default=1, help_text="Security clearance level 1-5")
    total_spent = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"{self.name} (Region: {self.region})"

class Transaction(BaseModel):
    STATUS_CHOICES = [
        ("Pending", "Pending Approval"),
        ("Processing", "In Transit"),
        ("Completed", "Delivered"),
        ("Cancelled", "Intercepted/Cancelled"),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='transactions')
    weapon = models.ForeignKey(Weapon, on_delete=models.CASCADE, related_name='transactions')
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")
    deal_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Deal #{self.id} - {self.client.name} ({self.status})"
    
    def save(self, *args, **kwargs):
        # Auto-calculate total price if not provided
        if not self.total_price:
            self.total_price = self.weapon.unit_price * self.quantity
        
        # Update client total spent on completion
        if self.status == "Completed" and self.id:
            old_status = Transaction.objects.get(id=self.id).status
            if old_status != "Completed":
                self.client.total_spent += self.total_price
                self.client.save()
                # Reduce stock
                self.weapon.stock_quantity -= self.quantity
                self.weapon.save()
        
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-deal_date']

class IntelligenceNote(BaseModel):
    content = models.TextField()
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='intel_notes')
    
    def __str__(self):
        return f"Intel for Deal #{self.transaction.id}"

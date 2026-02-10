from django.db import models
from django.utils import timezone

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Priority(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    level = models.IntegerField(help_text="Higher number = higher priority")
    color = models.CharField(max_length=7, default="#000000", help_text="Hex color code")
    
    def __str__(self):
        return f"{self.name} (Level: {self.level})"
    
    class Meta:
        verbose_name_plural = "Priorities"
        ordering = ['-level']

class Task(BaseModel):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="Pending"
    )
    due_date = models.DateTimeField(blank=True, null=True)
    completed_date = models.DateTimeField(blank=True, null=True)
    
    # Foreign Keys
    priority = models.ForeignKey(
        Priority, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    def __str__(self):
        return f"{self.title} - {self.status}"
    
    def save(self, *args, **kwargs):
        if self.status == "Completed" and not self.completed_date:
            self.completed_date = timezone.now()
        elif self.status != "Completed" and self.completed_date:
            self.completed_date = None
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-created_at']


class SubTask(BaseModel):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="Pending"
    )
    task = models.ForeignKey(
        Task, 
        on_delete=models.CASCADE, 
        related_name='subtasks'
    )
    order = models.IntegerField(default=0, help_text="Order of subtask in the list")
    
    def __str__(self):
        return f"{self.title} - {self.status}"
    
    class Meta:
        ordering = ['order', 'created_at']


class Note(BaseModel):
    content = models.TextField()
    task = models.ForeignKey(
        Task, 
        on_delete=models.CASCADE, 
        related_name='notes'
    )
    
    def __str__(self):
        return f"Note for {self.task.title} - {self.created_at.strftime('%Y-%m-%d')}"
    
    class Meta:
        ordering = ['-created_at']
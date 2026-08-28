from django.db import models
class MLModel(models.Model):
    name = models.CharField(max_length=100)
    model_type = models.CharField(max_length=50)
    version = models.CharField(max_length=20, default='1.0')
    file_path = models.CharField(max_length=500, blank=True)
    metrics = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    trained_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-trained_at']
    def __str__(self):
        return f'{self.name} v{self.version}'

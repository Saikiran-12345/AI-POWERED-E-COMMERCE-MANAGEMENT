from django.db import models
from django.conf import settings

class Recommendation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recommendations')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    score = models.FloatField(default=0.0)
    reason = models.CharField(max_length=100, default='popularity')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-score']
    def __str__(self):
        return f'Rec: {self.product.name} for {self.user.email}'

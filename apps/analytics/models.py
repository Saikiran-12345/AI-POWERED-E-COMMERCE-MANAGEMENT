from django.db import models

class SalesRecord(models.Model):
    date = models.DateField(db_index=True)
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey('products.Category', on_delete=models.SET_NULL, null=True)
    seller = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=0)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-date']
        indexes = [models.Index(fields=['date', 'seller']), models.Index(fields=['date', 'category'])]
    def __str__(self):
        return f'SalesRecord {self.date}: {self.revenue}'

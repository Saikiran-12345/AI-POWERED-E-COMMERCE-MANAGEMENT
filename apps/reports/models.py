from django.db import models
class Report(models.Model):
    REPORT_TYPES = [
        ('SALES', 'Sales'), ('PRODUCTS', 'Products'), ('INVENTORY', 'Inventory'),
        ('CUSTOMERS', 'Customers'), ('ORDERS', 'Orders'), ('ML', 'ML Predictions'),
    ]
    name = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    parameters = models.JSONField(default=dict)
    generated_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return f'{self.report_type}: {self.name}'

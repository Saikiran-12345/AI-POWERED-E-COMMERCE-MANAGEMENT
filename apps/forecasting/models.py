from django.db import models
class DemandForecast(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey('products.Category', on_delete=models.CASCADE, null=True, blank=True)
    forecast_date = models.DateField()
    predicted_quantity = models.IntegerField(default=0)
    confidence = models.FloatField(default=0.0)
    model_version = models.CharField(max_length=20, default='1.0')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['forecast_date']
    def __str__(self):
        return f'Forecast for {self.forecast_date}: {self.predicted_quantity}'

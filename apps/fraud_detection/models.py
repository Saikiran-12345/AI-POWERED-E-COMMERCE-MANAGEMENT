from django.db import models
from django.conf import settings

class FraudAnalysis(models.Model):
    RISK_LEVELS = [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')]
    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, null=True, blank=True, related_name='fraud_analysis')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    anomaly_score = models.FloatField(default=0.0)
    risk_level = models.CharField(max_length=10, choices=RISK_LEVELS, default='LOW')
    flags = models.JSONField(default=list)
    is_flagged = models.BooleanField(default=False)
    reviewed = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-anomaly_score']
        verbose_name = 'Fraud Analysis'
        verbose_name_plural = 'Fraud Analyses'
    def __str__(self):
        return f'FraudAnalysis: {self.risk_level} score={self.anomaly_score:.2f}'

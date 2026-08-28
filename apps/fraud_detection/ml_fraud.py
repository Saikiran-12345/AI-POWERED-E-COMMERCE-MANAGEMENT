import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from apps.orders.models import Order
from apps.fraud_detection.models import FraudAnalysis

def detect_fraud():
    """Detect anomalous orders using Isolation Forest."""
    orders = Order.objects.all()
    if orders.count() < 50:
        return
        
    data = []
    for o in orders:
        data.append({
            'id': o.id,
            'amount': float(o.total_amount),
            'item_count': o.item_count,
            'hour': o.created_at.hour
        })
        
    df = pd.DataFrame(data)
    
    # Train Isolation Forest
    clf = IsolationForest(contamination=0.05, random_state=42)
    df['anomaly'] = clf.fit_predict(df[['amount', 'item_count', 'hour']])
    df['score'] = clf.decision_function(df[['amount', 'item_count', 'hour']])
    
    # -1 means anomaly in IsolationForest
    anomalies = df[df['anomaly'] == -1]
    
    for _, row in anomalies.iterrows():
        order = Order.objects.get(id=row['id'])
        flags = []
        if row['amount'] > df['amount'].mean() * 3:
            flags.append("Unusually high amount")
        if row['item_count'] > df['item_count'].mean() * 3:
            flags.append("Unusually high item count")
        if row['hour'] < 5:
            flags.append("Order placed at unusual hour")
            
        FraudAnalysis.objects.update_or_create(
            order=order,
            defaults={
                'user': order.customer.user if order.customer else None,
                'anomaly_score': float(abs(row['score'])),
                'risk_level': 'HIGH' if row['score'] < -0.1 else 'MEDIUM',
                'flags': flags,
                'is_flagged': True
            }
        )

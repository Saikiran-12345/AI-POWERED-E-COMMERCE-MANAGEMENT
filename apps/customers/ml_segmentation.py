import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from apps.customers.models import Customer
from apps.orders.models import Order

def segment_customers():
    """Segment customers using K-Means clustering (RFM Analysis)."""
    customers = Customer.objects.all()
    if customers.count() < 10:
        return
        
    data = []
    for c in customers:
        data.append({
            'id': c.id,
            'recency': (pd.Timestamp.now(tz='UTC') - c.updated_at).days,
            'frequency': c.order_count,
            'monetary': float(c.total_spent)
        })
        
    df = pd.DataFrame(data)
    
    # Scale features
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df[['recency', 'frequency', 'monetary']])
    
    # K-Means clustering
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df['cluster'] = kmeans.fit_predict(scaled_features)
    
    # Map clusters to business segments
    cluster_centers = pd.DataFrame(kmeans.cluster_centers_, columns=['recency', 'frequency', 'monetary'])
    cluster_centers['cluster'] = cluster_centers.index
    
    # Identify segments based on monetary value (highest = VIP)
    vip_cluster = cluster_centers.loc[cluster_centers['monetary'].idxmax(), 'cluster']
    churn_cluster = cluster_centers.loc[cluster_centers['recency'].idxmax(), 'cluster']
    
    for _, row in df.iterrows():
        customer = Customer.objects.get(id=row['id'])
        if row['cluster'] == vip_cluster:
            customer.segment = 'VIP'
        elif row['cluster'] == churn_cluster:
            customer.segment = 'At Risk'
        else:
            customer.segment = 'Regular'
        customer.save(update_fields=['segment'])

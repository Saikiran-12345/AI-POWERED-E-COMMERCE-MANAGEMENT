import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from apps.products.models import Product
from apps.orders.models import OrderItem
from apps.recommendations.models import Recommendation
from apps.accounts.models import User

def build_content_based_recommendations():
    """Build content-based recommendations using product descriptions and tags."""
    products = Product.objects.filter(status='ACTIVE')
    if products.count() < 2:
        return

    df = pd.DataFrame(list(products.values('id', 'name', 'description', 'category__name', 'tags')))
    df['combined_features'] = df['name'] + ' ' + df['description'] + ' ' + df['category__name'] + ' ' + df['tags']
    
    # TF-IDF Vectorization
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['combined_features'].fillna(''))
    
    # Compute Cosine Similarity
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    # Generate recommendations for users based on past purchases
    users = User.objects.filter(role='CUSTOMER')
    for user in users:
        past_orders = OrderItem.objects.filter(order__customer__user=user).values_list('product_id', flat=True)
        if not past_orders:
            continue
            
        user_scores = np.zeros(len(df))
        for product_id in past_orders:
            try:
                idx = df.index[df['id'] == product_id].tolist()[0]
                user_scores += cosine_sim[idx]
            except IndexError:
                continue
                
        # Get top 10 recommended product indices
        top_indices = user_scores.argsort()[-11:][::-1]
        
        for idx in top_indices:
            rec_product_id = df.iloc[idx]['id']
            if rec_product_id not in past_orders:
                Recommendation.objects.update_or_create(
                    user=user,
                    product_id=rec_product_id,
                    defaults={'score': user_scores[idx], 'reason': 'content_similarity'}
                )

def generate_popular_recommendations():
    """Fallback recommendations based on popularity (sales + views)."""
    top_products = Product.objects.filter(status='ACTIVE').order_by('-purchase_count', '-view_count')[:10]
    users = User.objects.filter(role='CUSTOMER')
    
    for user in users:
        for i, product in enumerate(top_products):
            Recommendation.objects.get_or_create(
                user=user,
                product=product,
                defaults={'score': 10.0 - i, 'reason': 'popularity'}
            )

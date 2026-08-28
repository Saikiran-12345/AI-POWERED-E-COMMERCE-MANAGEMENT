from django.core.management.base import BaseCommand
import logging

class Command(BaseCommand):
    help = 'Run all Machine Learning pipelines (Recommendations, Segmentation, Fraud Detection)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting ML Pipelines...'))
        
        try:
            self.stdout.write('1. Running Customer Segmentation (K-Means)...')
            from apps.customers.ml_segmentation import segment_customers
            segment_customers()
            self.stdout.write(self.style.SUCCESS('   Segmentation complete.'))
            
            self.stdout.write('2. Running Product Recommendations (TF-IDF & Cosine Similarity)...')
            from apps.recommendations.ml_pipeline import build_content_based_recommendations, generate_popular_recommendations
            build_content_based_recommendations()
            generate_popular_recommendations()
            self.stdout.write(self.style.SUCCESS('   Recommendations complete.'))
            
            self.stdout.write('3. Running Fraud Detection (Isolation Forest)...')
            from apps.fraud_detection.ml_fraud import detect_fraud
            detect_fraud()
            self.stdout.write(self.style.SUCCESS('   Fraud detection complete.'))
            
            self.stdout.write(self.style.SUCCESS('\nAll ML Pipelines executed successfully!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'ML Pipeline failed: {e}'))
            logging.exception("ML Pipeline Error")

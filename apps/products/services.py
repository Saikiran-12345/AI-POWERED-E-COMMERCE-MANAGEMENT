import logging
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from .models import Category, Product, ProductImage, ProductAttribute

logger = logging.getLogger(__name__)

class CategoryService:
    """Service layer for Category to abstract business logic from views and serializers."""

    @classmethod
    def get_by_id(cls, obj_id: int) -> Category:
        try:
            return Category.objects.get(id=obj_id)
        except Category.DoesNotExist:
            logger.error(f'Category with id {obj_id} not found.')
            raise ObjectDoesNotExist(f'Category not found')

    @classmethod
    @transaction.atomic
    def create(cls, **kwargs) -> Category:
        """Create a new Category instance securely."""
        logger.info(f'Creating Category with data: {kwargs}')
        instance = Category(**kwargs)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def update(cls, instance: Category, **kwargs) -> Category:
        """Update an existing Category instance."""
        logger.info(f'Updating Category {instance.id} with data: {kwargs}')
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def delete(cls, instance: Category) -> bool:
        """Delete a Category instance."""
        logger.warning(f'Deleting Category {instance.id}')
        instance.delete()
        return True

    @classmethod
    def get_all_active(cls):
        """Retrieve all active Category instances if applicable."""
        if hasattr(Category, 'is_active'):
            return Category.objects.filter(is_active=True)
        elif hasattr(Category, 'status'):
            return Category.objects.filter(status='ACTIVE')
        return Category.objects.all()

class ProductService:
    """Service layer for Product to abstract business logic from views and serializers."""

    @classmethod
    def get_by_id(cls, obj_id: int) -> Product:
        try:
            return Product.objects.get(id=obj_id)
        except Product.DoesNotExist:
            logger.error(f'Product with id {obj_id} not found.')
            raise ObjectDoesNotExist(f'Product not found')

    @classmethod
    @transaction.atomic
    def create(cls, **kwargs) -> Product:
        """Create a new Product instance securely."""
        logger.info(f'Creating Product with data: {kwargs}')
        instance = Product(**kwargs)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def update(cls, instance: Product, **kwargs) -> Product:
        """Update an existing Product instance."""
        logger.info(f'Updating Product {instance.id} with data: {kwargs}')
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def delete(cls, instance: Product) -> bool:
        """Delete a Product instance."""
        logger.warning(f'Deleting Product {instance.id}')
        instance.delete()
        return True

    @classmethod
    def get_all_active(cls):
        """Retrieve all active Product instances if applicable."""
        if hasattr(Product, 'is_active'):
            return Product.objects.filter(is_active=True)
        elif hasattr(Product, 'status'):
            return Product.objects.filter(status='ACTIVE')
        return Product.objects.all()

class ProductImageService:
    """Service layer for ProductImage to abstract business logic from views and serializers."""

    @classmethod
    def get_by_id(cls, obj_id: int) -> ProductImage:
        try:
            return ProductImage.objects.get(id=obj_id)
        except ProductImage.DoesNotExist:
            logger.error(f'ProductImage with id {obj_id} not found.')
            raise ObjectDoesNotExist(f'ProductImage not found')

    @classmethod
    @transaction.atomic
    def create(cls, **kwargs) -> ProductImage:
        """Create a new ProductImage instance securely."""
        logger.info(f'Creating ProductImage with data: {kwargs}')
        instance = ProductImage(**kwargs)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def update(cls, instance: ProductImage, **kwargs) -> ProductImage:
        """Update an existing ProductImage instance."""
        logger.info(f'Updating ProductImage {instance.id} with data: {kwargs}')
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def delete(cls, instance: ProductImage) -> bool:
        """Delete a ProductImage instance."""
        logger.warning(f'Deleting ProductImage {instance.id}')
        instance.delete()
        return True

    @classmethod
    def get_all_active(cls):
        """Retrieve all active ProductImage instances if applicable."""
        if hasattr(ProductImage, 'is_active'):
            return ProductImage.objects.filter(is_active=True)
        elif hasattr(ProductImage, 'status'):
            return ProductImage.objects.filter(status='ACTIVE')
        return ProductImage.objects.all()

class ProductAttributeService:
    """Service layer for ProductAttribute to abstract business logic from views and serializers."""

    @classmethod
    def get_by_id(cls, obj_id: int) -> ProductAttribute:
        try:
            return ProductAttribute.objects.get(id=obj_id)
        except ProductAttribute.DoesNotExist:
            logger.error(f'ProductAttribute with id {obj_id} not found.')
            raise ObjectDoesNotExist(f'ProductAttribute not found')

    @classmethod
    @transaction.atomic
    def create(cls, **kwargs) -> ProductAttribute:
        """Create a new ProductAttribute instance securely."""
        logger.info(f'Creating ProductAttribute with data: {kwargs}')
        instance = ProductAttribute(**kwargs)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def update(cls, instance: ProductAttribute, **kwargs) -> ProductAttribute:
        """Update an existing ProductAttribute instance."""
        logger.info(f'Updating ProductAttribute {instance.id} with data: {kwargs}')
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def delete(cls, instance: ProductAttribute) -> bool:
        """Delete a ProductAttribute instance."""
        logger.warning(f'Deleting ProductAttribute {instance.id}')
        instance.delete()
        return True

    @classmethod
    def get_all_active(cls):
        """Retrieve all active ProductAttribute instances if applicable."""
        if hasattr(ProductAttribute, 'is_active'):
            return ProductAttribute.objects.filter(is_active=True)
        elif hasattr(ProductAttribute, 'status'):
            return ProductAttribute.objects.filter(status='ACTIVE')
        return ProductAttribute.objects.all()


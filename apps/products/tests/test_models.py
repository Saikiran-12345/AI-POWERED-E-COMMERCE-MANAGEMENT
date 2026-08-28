import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.products.models import Category, Product, ProductImage, ProductAttribute
from apps.products.factories import CategoryFactory, ProductFactory, ProductImageFactory, ProductAttributeFactory

@pytest.mark.django_db
class TestCategoryModel(TestCase):
    def setUp(self):
        self.instance = CategoryFactory()

    def test_category_creation(self):
        """Test that Category instance can be created and saved successfully."""
        self.assertIsNotNone(self.instance.pk)
        self.assertTrue(isinstance(self.instance, Category))

    def test_category_str_representation(self):
        """Test the string representation of Category."""
        self.assertIsInstance(str(self.instance), str)

    def test_category_name_field(self):
        """Ensure name field behaves correctly in Category."""
        field = Category._meta.get_field('name')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'name'))

    def test_category_slug_field(self):
        """Ensure slug field behaves correctly in Category."""
        field = Category._meta.get_field('slug')
        self.assertTrue(hasattr(self.instance, 'slug'))

    def test_category_description_field(self):
        """Ensure description field behaves correctly in Category."""
        field = Category._meta.get_field('description')
        self.assertTrue(hasattr(self.instance, 'description'))

    def test_category_image_field(self):
        """Ensure image field behaves correctly in Category."""
        field = Category._meta.get_field('image')
        self.assertTrue(hasattr(self.instance, 'image'))

    def test_category_parent_field(self):
        """Ensure parent field behaves correctly in Category."""
        field = Category._meta.get_field('parent')
        self.assertEqual(field.get_internal_type(), 'ForeignKey')
        self.assertTrue(hasattr(self.instance, 'parent'))

    def test_category_is_active_field(self):
        """Ensure is_active field behaves correctly in Category."""
        field = Category._meta.get_field('is_active')
        self.assertTrue(hasattr(self.instance, 'is_active'))

    def test_category_sort_order_field(self):
        """Ensure sort_order field behaves correctly in Category."""
        field = Category._meta.get_field('sort_order')
        self.assertEqual(field.get_internal_type(), 'IntegerField')
        self.assertTrue(hasattr(self.instance, 'sort_order'))

    def test_category_created_at_field(self):
        """Ensure created_at field behaves correctly in Category."""
        field = Category._meta.get_field('created_at')
        self.assertTrue(hasattr(self.instance, 'created_at'))

    def test_category_updated_at_field(self):
        """Ensure updated_at field behaves correctly in Category."""
        field = Category._meta.get_field('updated_at')
        self.assertTrue(hasattr(self.instance, 'updated_at'))

class TestProductModel(TestCase):
    def setUp(self):
        self.instance = ProductFactory()

    def test_product_creation(self):
        """Test that Product instance can be created and saved successfully."""
        self.assertIsNotNone(self.instance.pk)
        self.assertTrue(isinstance(self.instance, Product))

    def test_product_str_representation(self):
        """Test the string representation of Product."""
        self.assertIsInstance(str(self.instance), str)

    def test_product_product_id_field(self):
        """Ensure product_id field behaves correctly in Product."""
        field = Product._meta.get_field('product_id')
        self.assertTrue(hasattr(self.instance, 'product_id'))

    def test_product_name_field(self):
        """Ensure name field behaves correctly in Product."""
        field = Product._meta.get_field('name')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'name'))

    def test_product_slug_field(self):
        """Ensure slug field behaves correctly in Product."""
        field = Product._meta.get_field('slug')
        self.assertTrue(hasattr(self.instance, 'slug'))

    def test_product_description_field(self):
        """Ensure description field behaves correctly in Product."""
        field = Product._meta.get_field('description')
        self.assertTrue(hasattr(self.instance, 'description'))

    def test_product_short_description_field(self):
        """Ensure short_description field behaves correctly in Product."""
        field = Product._meta.get_field('short_description')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'short_description'))

    def test_product_category_field(self):
        """Ensure category field behaves correctly in Product."""
        field = Product._meta.get_field('category')
        self.assertEqual(field.get_internal_type(), 'ForeignKey')
        self.assertTrue(hasattr(self.instance, 'category'))

    def test_product_seller_field(self):
        """Ensure seller field behaves correctly in Product."""
        field = Product._meta.get_field('seller')
        self.assertEqual(field.get_internal_type(), 'ForeignKey')
        self.assertTrue(hasattr(self.instance, 'seller'))

    def test_product_brand_field(self):
        """Ensure brand field behaves correctly in Product."""
        field = Product._meta.get_field('brand')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'brand'))

    def test_product_sku_field(self):
        """Ensure sku field behaves correctly in Product."""
        field = Product._meta.get_field('sku')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'sku'))

    def test_product_price_field(self):
        """Ensure price field behaves correctly in Product."""
        field = Product._meta.get_field('price')
        self.assertTrue(hasattr(self.instance, 'price'))

    def test_product_discount_percent_field(self):
        """Ensure discount_percent field behaves correctly in Product."""
        field = Product._meta.get_field('discount_percent')
        self.assertTrue(hasattr(self.instance, 'discount_percent'))

    def test_product_cost_price_field(self):
        """Ensure cost_price field behaves correctly in Product."""
        field = Product._meta.get_field('cost_price')
        self.assertTrue(hasattr(self.instance, 'cost_price'))

    def test_product_main_image_field(self):
        """Ensure main_image field behaves correctly in Product."""
        field = Product._meta.get_field('main_image')
        self.assertTrue(hasattr(self.instance, 'main_image'))

    def test_product_status_field(self):
        """Ensure status field behaves correctly in Product."""
        field = Product._meta.get_field('status')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'status'))

    def test_product_is_featured_field(self):
        """Ensure is_featured field behaves correctly in Product."""
        field = Product._meta.get_field('is_featured')
        self.assertTrue(hasattr(self.instance, 'is_featured'))

    def test_product_is_digital_field(self):
        """Ensure is_digital field behaves correctly in Product."""
        field = Product._meta.get_field('is_digital')
        self.assertTrue(hasattr(self.instance, 'is_digital'))

    def test_product_average_rating_field(self):
        """Ensure average_rating field behaves correctly in Product."""
        field = Product._meta.get_field('average_rating')
        self.assertTrue(hasattr(self.instance, 'average_rating'))

    def test_product_review_count_field(self):
        """Ensure review_count field behaves correctly in Product."""
        field = Product._meta.get_field('review_count')
        self.assertEqual(field.get_internal_type(), 'IntegerField')
        self.assertTrue(hasattr(self.instance, 'review_count'))

    def test_product_meta_title_field(self):
        """Ensure meta_title field behaves correctly in Product."""
        field = Product._meta.get_field('meta_title')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'meta_title'))

    def test_product_meta_description_field(self):
        """Ensure meta_description field behaves correctly in Product."""
        field = Product._meta.get_field('meta_description')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'meta_description'))

    def test_product_tags_field(self):
        """Ensure tags field behaves correctly in Product."""
        field = Product._meta.get_field('tags')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'tags'))

    def test_product_view_count_field(self):
        """Ensure view_count field behaves correctly in Product."""
        field = Product._meta.get_field('view_count')
        self.assertEqual(field.get_internal_type(), 'IntegerField')
        self.assertTrue(hasattr(self.instance, 'view_count'))

    def test_product_purchase_count_field(self):
        """Ensure purchase_count field behaves correctly in Product."""
        field = Product._meta.get_field('purchase_count')
        self.assertEqual(field.get_internal_type(), 'IntegerField')
        self.assertTrue(hasattr(self.instance, 'purchase_count'))

    def test_product_created_at_field(self):
        """Ensure created_at field behaves correctly in Product."""
        field = Product._meta.get_field('created_at')
        self.assertTrue(hasattr(self.instance, 'created_at'))

    def test_product_updated_at_field(self):
        """Ensure updated_at field behaves correctly in Product."""
        field = Product._meta.get_field('updated_at')
        self.assertTrue(hasattr(self.instance, 'updated_at'))

class TestProductImageModel(TestCase):
    def setUp(self):
        self.instance = ProductImageFactory()

    def test_productimage_creation(self):
        """Test that ProductImage instance can be created and saved successfully."""
        self.assertIsNotNone(self.instance.pk)
        self.assertTrue(isinstance(self.instance, ProductImage))

    def test_productimage_str_representation(self):
        """Test the string representation of ProductImage."""
        self.assertIsInstance(str(self.instance), str)

    def test_productimage_product_field(self):
        """Ensure product field behaves correctly in ProductImage."""
        field = ProductImage._meta.get_field('product')
        self.assertEqual(field.get_internal_type(), 'ForeignKey')
        self.assertTrue(hasattr(self.instance, 'product'))

    def test_productimage_image_field(self):
        """Ensure image field behaves correctly in ProductImage."""
        field = ProductImage._meta.get_field('image')
        self.assertTrue(hasattr(self.instance, 'image'))

    def test_productimage_alt_text_field(self):
        """Ensure alt_text field behaves correctly in ProductImage."""
        field = ProductImage._meta.get_field('alt_text')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'alt_text'))

    def test_productimage_sort_order_field(self):
        """Ensure sort_order field behaves correctly in ProductImage."""
        field = ProductImage._meta.get_field('sort_order')
        self.assertEqual(field.get_internal_type(), 'IntegerField')
        self.assertTrue(hasattr(self.instance, 'sort_order'))

    def test_productimage_created_at_field(self):
        """Ensure created_at field behaves correctly in ProductImage."""
        field = ProductImage._meta.get_field('created_at')
        self.assertTrue(hasattr(self.instance, 'created_at'))

class TestProductAttributeModel(TestCase):
    def setUp(self):
        self.instance = ProductAttributeFactory()

    def test_productattribute_creation(self):
        """Test that ProductAttribute instance can be created and saved successfully."""
        self.assertIsNotNone(self.instance.pk)
        self.assertTrue(isinstance(self.instance, ProductAttribute))

    def test_productattribute_str_representation(self):
        """Test the string representation of ProductAttribute."""
        self.assertIsInstance(str(self.instance), str)

    def test_productattribute_product_field(self):
        """Ensure product field behaves correctly in ProductAttribute."""
        field = ProductAttribute._meta.get_field('product')
        self.assertEqual(field.get_internal_type(), 'ForeignKey')
        self.assertTrue(hasattr(self.instance, 'product'))

    def test_productattribute_name_field(self):
        """Ensure name field behaves correctly in ProductAttribute."""
        field = ProductAttribute._meta.get_field('name')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'name'))

    def test_productattribute_value_field(self):
        """Ensure value field behaves correctly in ProductAttribute."""
        field = ProductAttribute._meta.get_field('value')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'value'))


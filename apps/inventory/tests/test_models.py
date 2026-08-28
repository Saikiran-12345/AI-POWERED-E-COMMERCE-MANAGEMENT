import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.inventory.models import Inventory, InventoryHistory
from apps.inventory.factories import InventoryFactory, InventoryHistoryFactory

@pytest.mark.django_db
class TestInventoryModel(TestCase):
    def setUp(self):
        self.instance = InventoryFactory()

    def test_inventory_creation(self):
        """Test that Inventory instance can be created and saved successfully."""
        self.assertIsNotNone(self.instance.pk)
        self.assertTrue(isinstance(self.instance, Inventory))

    def test_inventory_str_representation(self):
        """Test the string representation of Inventory."""
        self.assertIsInstance(str(self.instance), str)

    def test_inventory_product_field(self):
        """Ensure product field behaves correctly in Inventory."""
        field = Inventory._meta.get_field('product')
        self.assertTrue(hasattr(self.instance, 'product'))

    def test_inventory_quantity_field(self):
        """Ensure quantity field behaves correctly in Inventory."""
        field = Inventory._meta.get_field('quantity')
        self.assertEqual(field.get_internal_type(), 'IntegerField')
        self.assertTrue(hasattr(self.instance, 'quantity'))

    def test_inventory_reserved_quantity_field(self):
        """Ensure reserved_quantity field behaves correctly in Inventory."""
        field = Inventory._meta.get_field('reserved_quantity')
        self.assertEqual(field.get_internal_type(), 'IntegerField')
        self.assertTrue(hasattr(self.instance, 'reserved_quantity'))

    def test_inventory_reorder_point_field(self):
        """Ensure reorder_point field behaves correctly in Inventory."""
        field = Inventory._meta.get_field('reorder_point')
        self.assertEqual(field.get_internal_type(), 'IntegerField')
        self.assertTrue(hasattr(self.instance, 'reorder_point'))

    def test_inventory_reorder_quantity_field(self):
        """Ensure reorder_quantity field behaves correctly in Inventory."""
        field = Inventory._meta.get_field('reorder_quantity')
        self.assertEqual(field.get_internal_type(), 'IntegerField')
        self.assertTrue(hasattr(self.instance, 'reorder_quantity'))

    def test_inventory_warehouse_location_field(self):
        """Ensure warehouse_location field behaves correctly in Inventory."""
        field = Inventory._meta.get_field('warehouse_location')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'warehouse_location'))

    def test_inventory_last_restocked_at_field(self):
        """Ensure last_restocked_at field behaves correctly in Inventory."""
        field = Inventory._meta.get_field('last_restocked_at')
        self.assertTrue(hasattr(self.instance, 'last_restocked_at'))

    def test_inventory_updated_at_field(self):
        """Ensure updated_at field behaves correctly in Inventory."""
        field = Inventory._meta.get_field('updated_at')
        self.assertTrue(hasattr(self.instance, 'updated_at'))

    def test_inventory_created_at_field(self):
        """Ensure created_at field behaves correctly in Inventory."""
        field = Inventory._meta.get_field('created_at')
        self.assertTrue(hasattr(self.instance, 'created_at'))

class TestInventoryHistoryModel(TestCase):
    def setUp(self):
        self.instance = InventoryHistoryFactory()

    def test_inventoryhistory_creation(self):
        """Test that InventoryHistory instance can be created and saved successfully."""
        self.assertIsNotNone(self.instance.pk)
        self.assertTrue(isinstance(self.instance, InventoryHistory))

    def test_inventoryhistory_str_representation(self):
        """Test the string representation of InventoryHistory."""
        self.assertIsInstance(str(self.instance), str)

    def test_inventoryhistory_inventory_field(self):
        """Ensure inventory field behaves correctly in InventoryHistory."""
        field = InventoryHistory._meta.get_field('inventory')
        self.assertEqual(field.get_internal_type(), 'ForeignKey')
        self.assertTrue(hasattr(self.instance, 'inventory'))

    def test_inventoryhistory_change_type_field(self):
        """Ensure change_type field behaves correctly in InventoryHistory."""
        field = InventoryHistory._meta.get_field('change_type')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'change_type'))

    def test_inventoryhistory_quantity_changed_field(self):
        """Ensure quantity_changed field behaves correctly in InventoryHistory."""
        field = InventoryHistory._meta.get_field('quantity_changed')
        self.assertEqual(field.get_internal_type(), 'IntegerField')
        self.assertTrue(hasattr(self.instance, 'quantity_changed'))

    def test_inventoryhistory_quantity_before_field(self):
        """Ensure quantity_before field behaves correctly in InventoryHistory."""
        field = InventoryHistory._meta.get_field('quantity_before')
        self.assertEqual(field.get_internal_type(), 'IntegerField')
        self.assertTrue(hasattr(self.instance, 'quantity_before'))

    def test_inventoryhistory_quantity_after_field(self):
        """Ensure quantity_after field behaves correctly in InventoryHistory."""
        field = InventoryHistory._meta.get_field('quantity_after')
        self.assertEqual(field.get_internal_type(), 'IntegerField')
        self.assertTrue(hasattr(self.instance, 'quantity_after'))

    def test_inventoryhistory_note_field(self):
        """Ensure note field behaves correctly in InventoryHistory."""
        field = InventoryHistory._meta.get_field('note')
        self.assertTrue(hasattr(self.instance, 'note'))

    def test_inventoryhistory_changed_by_field(self):
        """Ensure changed_by field behaves correctly in InventoryHistory."""
        field = InventoryHistory._meta.get_field('changed_by')
        self.assertEqual(field.get_internal_type(), 'ForeignKey')
        self.assertTrue(hasattr(self.instance, 'changed_by'))

    def test_inventoryhistory_created_at_field(self):
        """Ensure created_at field behaves correctly in InventoryHistory."""
        field = InventoryHistory._meta.get_field('created_at')
        self.assertTrue(hasattr(self.instance, 'created_at'))


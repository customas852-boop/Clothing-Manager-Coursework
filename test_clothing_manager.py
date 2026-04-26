"""
Unit Tests for Clothing Wardrobe Management System
Tests core functionality using Python's unittest framework
"""

import unittest
import os
import json
from datetime import datetime
from clothing_manager_complete import (
    Location, ClothingItem, Shoes, Clothing, Accessories, 
    Outfit, Wardrobe, ClothingItemFactory
)


class TestLocation(unittest.TestCase):
    """Test Location class functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Reset Wardrobe singleton before each test
        Wardrobe._instance = None
        self.wardrobe = Wardrobe()
        self.location = self.wardrobe.add_location("Bedroom", "Main closet")
    
    def tearDown(self):
        """Clean up after tests."""
        Wardrobe._instance = None
        if os.path.exists("wardrobe_data.json"):
            os.remove("wardrobe_data.json")
    
    def test_location_creation(self):
        """Test creating a location."""
        self.assertEqual(self.location.name, "Bedroom")
        self.assertEqual(self.location.description, "Main closet")
        self.assertIsNotNone(self.location.location_id)
    
    def test_location_id_unique(self):
        """Test that location IDs are unique."""
        loc1 = self.wardrobe.add_location("Drawer 1")
        loc2 = self.wardrobe.add_location("Drawer 2")
        self.assertNotEqual(loc1.location_id, loc2.location_id)
    
    def test_location_string_representation(self):
        """Test location string representation."""
        location_str = str(self.location)
        self.assertIn("Location", location_str)


class TestClothingItems(unittest.TestCase):
    """Test clothing item classes (Shoes, Clothing, Accessories)."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Reset Wardrobe singleton and create fresh wardrobe
        Wardrobe._instance = None
        ClothingItem._id_counter = 0
        self.wardrobe = Wardrobe()
        self.location = self.wardrobe.add_location("Closet")
        self.shoes = Shoes("Nike", "White", "10", "sneakers", self.location)
        self.clothing = Clothing("T-Shirt", "Blue", "M", "shirt", self.location)
        self.accessories = Accessories("Belt", "Brown", "M", "belt", self.location)
    
    def tearDown(self):
        """Clean up after tests."""
        Wardrobe._instance = None
        ClothingItem._id_counter = 0
        if os.path.exists("wardrobe_data.json"):
            os.remove("wardrobe_data.json")
    
    def test_shoes_creation(self):
        """Test creating shoes."""
        self.assertEqual(self.shoes.name, "Nike")
        self.assertEqual(self.shoes.color, "White")
        self.assertEqual(self.shoes.size, "10")
        self.assertEqual(self.shoes.shoe_type, "sneakers")
        self.assertEqual(self.shoes.get_type(), "Shoes")
    
    def test_clothing_creation(self):
        """Test creating clothing."""
        self.assertEqual(self.clothing.name, "T-Shirt")
        self.assertEqual(self.clothing.color, "Blue")
        self.assertEqual(self.clothing.clothing_type, "shirt")
        self.assertEqual(self.clothing.get_type(), "Clothing")
    
    def test_accessories_creation(self):
        """Test creating accessories."""
        self.assertEqual(self.accessories.name, "Belt")
        self.assertEqual(self.accessories.accessory_type, "belt")
        self.assertEqual(self.accessories.get_type(), "Accessories")
    
    def test_item_id_unique(self):
        """Test that item IDs are unique."""
        item1 = Shoes("Shoe 1", "Black", "9")
        item2 = Shoes("Shoe 2", "White", "10")
        self.assertNotEqual(item1.item_id, item2.item_id)
    
    def test_assign_location(self):
        """Test assigning location to item."""
        item = Shoes("Test", "Black", "10")
        self.assertIsNone(item.location)
        
        item.assign_location(self.location)
        self.assertEqual(item.location, self.location)
    
    def test_remove_location(self):
        """Test removing location from item."""
        self.assertEqual(self.shoes.location, self.location)
        self.shoes.remove_location()
        self.assertIsNone(self.shoes.location)
    
    def test_item_has_date_added(self):
        """Test that items have date_added timestamp."""
        self.assertIsNotNone(self.shoes.date_added)
        self.assertIsInstance(self.shoes.date_added, str)  # ISO format
    
    def test_polymorphism_get_type(self):
        """Test polymorphism - different items return different types."""
        self.assertEqual(self.shoes.get_type(), "Shoes")
        self.assertEqual(self.clothing.get_type(), "Clothing")
        self.assertEqual(self.accessories.get_type(), "Accessories")


class TestClothingItemFactory(unittest.TestCase):
    """Test Factory Pattern for creating items."""
    
    def setUp(self):
        """Set up test fixtures."""
        Wardrobe._instance = None
        ClothingItem._id_counter = 0
        self.wardrobe = Wardrobe()
    
    def tearDown(self):
        """Clean up after tests."""
        Wardrobe._instance = None
        ClothingItem._id_counter = 0
        if os.path.exists("wardrobe_data.json"):
            os.remove("wardrobe_data.json")
    
    def test_factory_create_shoes(self):
        """Test factory creating shoes."""
        shoes = ClothingItemFactory.create_item("Shoes", "Nike", "Black", "11")
        self.assertIsInstance(shoes, Shoes)
        self.assertEqual(shoes.get_type(), "Shoes")
    
    def test_factory_create_clothing(self):
        """Test factory creating clothing."""
        clothing = ClothingItemFactory.create_item("Clothing", "Jeans", "Blue", "32")
        self.assertIsInstance(clothing, Clothing)
        self.assertEqual(clothing.get_type(), "Clothing")
    
    def test_factory_create_accessories(self):
        """Test factory creating accessories."""
        accessory = ClothingItemFactory.create_item("Accessories", "Scarf", "Red", "One Size")
        self.assertIsInstance(accessory, Accessories)
        self.assertEqual(accessory.get_type(), "Accessories")
    
    def test_factory_invalid_type(self):
        """Test factory with invalid type."""
        with self.assertRaises(ValueError):
            ClothingItemFactory.create_item("InvalidType", "Test", "Black", "M")


class TestOutfit(unittest.TestCase):
    """Test Outfit class (Composition pattern)."""
    
    def setUp(self):
        """Set up test fixtures."""
        Wardrobe._instance = None
        ClothingItem._id_counter = 0
        self.wardrobe = Wardrobe()
        self.location = self.wardrobe.add_location("Closet")
        self.shoes = self.wardrobe.add_shoes("Nike", "White", "10")
        self.clothing = self.wardrobe.add_clothing("T-Shirt", "Blue", "M")
        self.outfit = Outfit("Casual Outfit")
    
    def tearDown(self):
        """Clean up after tests."""
        Wardrobe._instance = None
        ClothingItem._id_counter = 0
        if os.path.exists("wardrobe_data.json"):
            os.remove("wardrobe_data.json")
    
    def test_outfit_creation(self):
        """Test creating an outfit."""
        self.assertEqual(self.outfit.name, "Casual Outfit")
        self.assertIsNotNone(self.outfit.outfit_id)
        self.assertEqual(len(self.outfit.get_items()), 0)
    
    def test_add_item_to_outfit(self):
        """Test adding items to outfit (composition)."""
        self.outfit.add_item(self.shoes)
        self.assertIn(self.shoes, self.outfit.get_items())
    
    def test_add_multiple_items(self):
        """Test adding multiple items to outfit."""
        self.outfit.add_item(self.shoes)
        self.outfit.add_item(self.clothing)
        self.assertEqual(len(self.outfit.get_items()), 2)
    
    def test_remove_item_from_outfit(self):
        """Test removing items from outfit."""
        self.outfit.add_item(self.shoes)
        self.outfit.add_item(self.clothing)
        self.outfit.remove_item(self.shoes.item_id)
        self.assertNotIn(self.shoes, self.outfit.get_items())
        self.assertIn(self.clothing, self.outfit.get_items())
    
    def test_add_duplicate_item(self):
        """Test that adding duplicate items is prevented."""
        self.outfit.add_item(self.shoes)
        self.outfit.add_item(self.shoes)  # Try to add same item again
        self.assertEqual(len(self.outfit.get_items()), 1)  # Should still be 1
    
    def test_outfit_completeness(self):
        """Test outfit completeness (needs at least 2 types)."""
        self.assertFalse(self.outfit.is_complete())  # Empty outfit
        self.outfit.add_item(self.shoes)
        self.assertFalse(self.outfit.is_complete())  # Only 1 item
        self.outfit.add_item(self.clothing)
        self.assertTrue(self.outfit.is_complete())  # 2 items = complete
    
    def test_outfit_color_scheme(self):
        """Test getting outfit color scheme."""
        self.outfit.add_item(self.shoes)
        self.outfit.add_item(self.clothing)
        colors = self.outfit.get_color_scheme()
        self.assertIn("White", colors)
        self.assertIn("Blue", colors)
    
    def test_outfit_id_unique(self):
        """Test that outfit IDs are unique."""
        outfit2 = Outfit("Formal Outfit")
        self.assertNotEqual(self.outfit.outfit_id, outfit2.outfit_id)
    
    def test_composition_independence(self):
        """Test that items in outfit remain independent (composition)."""
        self.outfit.add_item(self.shoes)
        original_color = self.shoes.color
        self.shoes.color = "Red"  # Change item outside outfit
        # Item in outfit should reflect change (composition allows access)
        self.assertEqual(self.outfit.get_items()[0].color, "Red")
        self.shoes.color = original_color  # Restore


class TestWardrobe(unittest.TestCase):
    """Test Wardrobe class (Singleton and Aggregation)."""
    
    def setUp(self):
        """Set up test fixtures."""
        Wardrobe._instance = None
        ClothingItem._id_counter = 0
        self.wardrobe = Wardrobe()
    
    def tearDown(self):
        """Clean up after tests."""
        Wardrobe._instance = None
        ClothingItem._id_counter = 0
        if os.path.exists("wardrobe_data.json"):
            os.remove("wardrobe_data.json")
    
    def test_wardrobe_creation(self):
        """Test creating a wardrobe."""
        self.assertIsNotNone(self.wardrobe)
        self.assertEqual(len(self.wardrobe.list_items()), 0)
        self.assertEqual(len(self.wardrobe.list_locations()), 0)
    
    def test_singleton_pattern(self):
        """Test Singleton pattern - same instance."""
        wardrobe1 = Wardrobe()
        wardrobe2 = Wardrobe()
        self.assertIs(wardrobe1, wardrobe2)
    
    def test_add_location(self):
        """Test adding locations to wardrobe (aggregation)."""
        location = self.wardrobe.add_location("Closet", "Main")
        self.assertEqual(len(self.wardrobe.list_locations()), 1)
        self.assertEqual(location.name, "Closet")
    
    def test_add_shoes(self):
        """Test adding shoes to wardrobe."""
        shoes = self.wardrobe.add_shoes("Nike", "White", "10")
        self.assertEqual(len(self.wardrobe.list_items()), 1)
        self.assertEqual(shoes.name, "Nike")
    
    def test_add_clothing(self):
        """Test adding clothing to wardrobe."""
        clothing = self.wardrobe.add_clothing("Jeans", "Blue", "32")
        self.assertEqual(len(self.wardrobe.list_items()), 1)
        self.assertEqual(clothing.get_type(), "Clothing")
    
    def test_add_accessories(self):
        """Test adding accessories to wardrobe."""
        accessory = self.wardrobe.add_accessories("Watch", "Silver", "One Size")
        self.assertEqual(len(self.wardrobe.list_items()), 1)
        self.assertEqual(accessory.get_type(), "Accessories")
    
    def test_get_item_by_id(self):
        """Test retrieving item by ID."""
        shoes = self.wardrobe.add_shoes("Nike", "Black", "11")
        item = self.wardrobe.get_item(shoes.item_id)
        self.assertEqual(item, shoes)
    
    def test_get_nonexistent_item(self):
        """Test retrieving non-existent item."""
        item = self.wardrobe.get_item(999)
        self.assertIsNone(item)
    
    def test_create_outfit(self):
        """Test creating outfit in wardrobe."""
        shoes = self.wardrobe.add_shoes("Nike", "White", "10")
        clothing = self.wardrobe.add_clothing("T-Shirt", "Blue", "M")
        outfit = self.wardrobe.create_outfit("Casual")
        outfit.add_item(shoes)
        outfit.add_item(clothing)
        self.assertEqual(len(self.wardrobe.list_outfits()), 1)
    
    def test_add_item_to_outfit(self):
        """Test adding item to outfit through wardrobe."""
        shoes = self.wardrobe.add_shoes("Nike", "White", "10")
        outfit = self.wardrobe.create_outfit("Empty Outfit")
        self.wardrobe.add_item_to_outfit(outfit.outfit_id, shoes.item_id)
        self.assertIn(shoes, outfit.get_items())
    
    def test_remove_item_from_outfit(self):
        """Test removing item from outfit through wardrobe."""
        shoes = self.wardrobe.add_shoes("Nike", "White", "10")
        outfit = self.wardrobe.create_outfit("With Shoes")
        outfit.add_item(shoes)
        self.wardrobe.remove_item_from_outfit(outfit.outfit_id, shoes.item_id)
        self.assertNotIn(shoes, outfit.get_items())
    
    def test_list_complete_outfits(self):
        """Test listing complete outfits."""
        shoes = self.wardrobe.add_shoes("Nike", "White", "10")
        clothing = self.wardrobe.add_clothing("T-Shirt", "Blue", "M")
        outfit1 = self.wardrobe.create_outfit("Complete")
        outfit1.add_item(shoes)
        outfit1.add_item(clothing)
        
        incomplete = self.wardrobe.create_outfit("Incomplete")
        incomplete.add_item(shoes)
        
        complete_outfits = self.wardrobe.list_complete_outfits()
        self.assertEqual(len(complete_outfits), 1)
        self.assertTrue(outfit1.is_complete())
        self.assertFalse(incomplete.is_complete())
    
    def test_aggregation_independence(self):
        """Test that items in wardrobe can exist independently (aggregation)."""
        shoes = self.wardrobe.add_shoes("Nike", "White", "10")
        location = self.wardrobe.add_location("Bedroom")
        
        # Item exists independently
        self.assertIn(shoes, self.wardrobe.list_items())
        self.assertIn(location, self.wardrobe.list_locations())
        # Items and locations have independent lifespans


class TestPersistence(unittest.TestCase):
    """Test file I/O and persistence."""
    
    def setUp(self):
        """Set up test fixtures."""
        Wardrobe._instance = None
        ClothingItem._id_counter = 0
        self.test_file = "test_wardrobe.json"
    
    def tearDown(self):
        """Clean up after tests."""
        Wardrobe._instance = None
        ClothingItem._id_counter = 0
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists("wardrobe_data.json"):
            os.remove("wardrobe_data.json")
    
    def test_save_data(self):
        """Test saving wardrobe data."""
        wardrobe = Wardrobe(self.test_file)
        wardrobe.add_location("Closet")
        wardrobe.add_shoes("Nike", "White", "10")
        wardrobe.save_data()
        self.assertTrue(os.path.exists(self.test_file))
    
    def test_load_data(self):
        """Test loading wardrobe data."""
        # Create wardrobe and add data
        wardrobe1 = Wardrobe(self.test_file)
        wardrobe1.add_location("Bedroom")
        wardrobe1.add_shoes("Nike", "White", "10")
        wardrobe1.save_data()
        
        # Verify save
        self.assertTrue(os.path.exists(self.test_file))
        
        # Reset and load
        Wardrobe._instance = None
        ClothingItem._id_counter = 0
        wardrobe2 = Wardrobe(self.test_file)
        self.assertGreater(len(wardrobe2.list_locations()), 0)
    
    def test_persistence_data_integrity(self):
        """Test that persisted data maintains integrity."""
        # Create and save
        wardrobe1 = Wardrobe(self.test_file)
        wardrobe1.add_location("Closet")
        wardrobe1.add_shoes("Nike", "White", "10")
        wardrobe1.save_data()
        
        # Load and verify
        Wardrobe._instance = None
        ClothingItem._id_counter = 0
        wardrobe2 = Wardrobe(self.test_file)
        items = wardrobe2.list_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].name, "Nike")


class TestEncapsulation(unittest.TestCase):
    """Test encapsulation of private attributes."""
    
    def setUp(self):
        """Set up test fixtures."""
        Wardrobe._instance = None
        ClothingItem._id_counter = 0
    
    def tearDown(self):
        """Clean up after tests."""
        Wardrobe._instance = None
        ClothingItem._id_counter = 0
        if os.path.exists("wardrobe_data.json"):
            os.remove("wardrobe_data.json")
    
    def test_id_counter_private(self):
        """Test that ID counters are private."""
        item1 = Shoes("Nike", "White", "10")
        self.assertEqual(item1.item_id, 1)
        # Check that _id_counter exists but is private (leading underscore)
        self.assertTrue(hasattr(Shoes.__bases__[0], '_id_counter'))
    
    def test_item_id_property(self):
        """Test item_id is accessible."""
        item = Shoes("Nike", "White", "10")
        self.assertEqual(item.item_id, 1)
        self.assertIsNotNone(item.item_id)


class TestIntegration(unittest.TestCase):
    """Integration tests combining multiple features."""
    
    def setUp(self):
        """Set up test fixtures."""
        Wardrobe._instance = None
        ClothingItem._id_counter = 0
        self.wardrobe = Wardrobe()
    
    def tearDown(self):
        """Clean up after tests."""
        Wardrobe._instance = None
        ClothingItem._id_counter = 0
        if os.path.exists("wardrobe_data.json"):
            os.remove("wardrobe_data.json")
    
    def test_complete_workflow(self):
        """Test complete workflow: create locations, add items, create outfits."""
        # Add locations (aggregation)
        bedroom = self.wardrobe.add_location("Bedroom")
        closet = self.wardrobe.add_location("Closet")
        
        # Add items
        shoes = self.wardrobe.add_shoes("Nike", "White", "10")
        clothing = self.wardrobe.add_clothing("T-Shirt", "Blue", "M")
        
        # Assign locations to items
        self.wardrobe.assign_location_to_item(shoes.item_id, bedroom.location_id)
        self.wardrobe.assign_location_to_item(clothing.item_id, closet.location_id)
        
        # Create outfit (composition)
        outfit = self.wardrobe.create_outfit("Weekend Casual")
        outfit.add_item(shoes)
        outfit.add_item(clothing)
        
        # Verify
        self.assertEqual(len(self.wardrobe.list_locations()), 2)
        self.assertEqual(len(self.wardrobe.list_items()), 2)
        self.assertEqual(len(self.wardrobe.list_outfits()), 1)
        self.assertTrue(outfit.is_complete())
    
    def test_factory_pattern_workflow(self):
        """Test workflow using factory pattern."""
        # Use factory to create items
        shoes = ClothingItemFactory.create_item("Shoes", "Adidas", "Black", "9")
        clothing = ClothingItemFactory.create_item("Clothing", "Pants", "Brown", "32")
        accessory = ClothingItemFactory.create_item("Accessories", "Hat", "White", "One Size")
        
        # Add to wardrobe
        self.wardrobe.add_item(shoes)
        self.wardrobe.add_item(clothing)
        self.wardrobe.add_item(accessory)
        
        # Create outfit
        outfit = self.wardrobe.create_outfit("Factory Made")
        # Add items to outfit
        outfit.add_item(shoes)
        outfit.add_item(clothing)
        outfit.add_item(accessory)
        
        # Verify all types present
        types = set(item.get_type() for item in outfit.get_items())
        self.assertEqual(len(types), 3)


def create_test_suite():
    """Create and return test suite."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestLocation))
    suite.addTests(loader.loadTestsFromTestCase(TestClothingItems))
    suite.addTests(loader.loadTestsFromTestCase(TestClothingItemFactory))
    suite.addTests(loader.loadTestsFromTestCase(TestOutfit))
    suite.addTests(loader.loadTestsFromTestCase(TestWardrobe))
    suite.addTests(loader.loadTestsFromTestCase(TestPersistence))
    suite.addTests(loader.loadTestsFromTestCase(TestEncapsulation))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    return suite


if __name__ == "__main__":
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    suite = create_test_suite()
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)

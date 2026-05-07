"""
File I/O Practical Examples
Demonstrates how to use the file I/O functionality in real-world scenarios
"""

from clothing_manager import Wardrobe
from file_manager import FileManager


def example_1_basic_export():
    """Example 1: Basic CSV Export"""
    print("="*70)
    print("EXAMPLE 1: Basic CSV Export")
    print("="*70)
    
    # Create wardrobe with items
    wardrobe = Wardrobe("example1.json")
    
    # Add some locations
    bedroom = wardrobe.add_location("Bedroom", "Main closet")
    drawer = wardrobe.add_location("Drawer 1", "Sock drawer")
    
    # Add items
    wardrobe.add_shoes("Nike Sneakers", "White", "10", location=bedroom)
    wardrobe.add_shoes("Black Heels", "Black", "8", "heels", location=drawer)
    wardrobe.add_clothing("Blue T-Shirt", "Blue", "M", "shirt", location=bedroom)
    wardrobe.add_clothing("Denim Jeans", "Blue", "32", "pants", location=drawer)
    wardrobe.add_accessories("Leather Belt", "Brown", "M", "belt", location=bedroom)
    
    # Export to CSV
    FileManager.export_items_to_csv(wardrobe, "example1_items.csv")
    FileManager.export_locations_to_csv(wardrobe, "example1_locations.csv")
    
    print("\n✓ Files created:")
    print("  - example1_items.csv")
    print("  - example1_locations.csv")
    print("\nOpen these files in Excel or a text editor to view!")


def example_2_bulk_import():
    """Example 2: Bulk Import from CSV"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Bulk Import from CSV")
    print("="*70)
    
    # First, create a sample CSV file
    csv_content = """Type,Name,Color,Size,Location,Specific Type
Shoes,Running Shoes,Gray,9,Gym Locker,sneakers
Shoes,Formal Shoes,Black,10,Closet,formal
Clothing,Gym T-Shirt,Red,M,Gym Locker,shirt
Clothing,Business Shirt,White,L,Closet,shirt
Clothing,Casual Pants,Beige,32,Closet,pants
Accessories,Sports Watch,Silver,One Size,Gym Locker,watch
Accessories,Business Watch,Gold,One Size,Closet,watch
Accessories,Scarf,Grey,One Size,Closet,scarf
"""
    
    # Write sample CSV
    with open("example2_import.csv", "w") as f:
        f.write(csv_content)
    
    print("Created sample CSV file: example2_import.csv")
    
    # Now import it
    wardrobe = Wardrobe("example2.json")
    imported, failed = FileManager.import_items_from_csv(wardrobe, "example2_import.csv")
    
    print(f"\nImport Results:")
    print(f"  ✓ Successfully imported: {imported} items")
    print(f"  ✗ Failed: {failed} items")
    
    print(f"\nWardrobe now contains {len(wardrobe.list_items())} items")
    print(f"Locations created: {', '.join([loc.name for loc in wardrobe.list_locations()])}")


def example_3_outfit_export():
    """Example 3: Export Outfits to CSV"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Export Outfits to CSV")
    print("="*70)
    
    wardrobe = Wardrobe("example3.json")
    
    # Add items
    drawer = wardrobe.add_location("Drawer", "Main drawer")
    shoes = wardrobe.add_shoes("Nike", "White", "10", location=drawer)
    shirt = wardrobe.add_clothing("Polo", "Blue", "M", "shirt", location=drawer)
    pants = wardrobe.add_clothing("Khakis", "Beige", "32", "pants", location=drawer)
    belt = wardrobe.add_accessories("Belt", "Brown", "M", "belt", location=drawer)
    
    # Create outfits
    casual = wardrobe.create_outfit("Casual Friday", "Comfortable work outfit")
    casual.add_item(shoes)
    casual.add_item(shirt)
    casual.add_item(pants)
    casual.add_item(belt)
    
    gym = wardrobe.create_outfit("Gym", "Workout clothes")
    gym.add_item(shoes)
    gym.add_item(shirt)
    
    # Export outfits
    FileManager.export_outfits_to_csv(wardrobe, "example3_outfits.csv")
    
    print(f"\n✓ Exported {len(wardrobe.list_outfits())} outfits to example3_outfits.csv")
    print("\nOutfits:")
    for outfit in wardrobe.list_outfits():
        status = "✓ Complete" if outfit.is_complete() else "✗ Incomplete"
        print(f"  - {outfit.name} ({len(outfit.get_items())} items) {status}")


def example_4_generate_reports():
    """Example 4: Generate Comprehensive Reports"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Generate Comprehensive Reports")
    print("="*70)
    
    wardrobe = Wardrobe("example4.json")
    
    # Build wardrobe
    bedroom = wardrobe.add_location("Bedroom", "Main closet")
    closet = wardrobe.add_location("Office Closet", "Work clothes")
    
    # Add various items
    items_data = [
        ("Shoes", "Nike Sneakers", "White", "10", "Bedroom", "sneakers"),
        ("Shoes", "Black Heels", "Black", "8", "Office Closet", "heels"),
        ("Clothing", "Blue T-Shirt", "Blue", "M", "Bedroom", "shirt"),
        ("Clothing", "White Blouse", "White", "M", "Office Closet", "shirt"),
        ("Clothing", "Black Pants", "Black", "32", "Office Closet", "pants"),
        ("Clothing", "Denim Jeans", "Blue", "32", "Bedroom", "pants"),
        ("Accessories", "Brown Belt", "Brown", "M", "Bedroom", "belt"),
        ("Accessories", "Black Belt", "Black", "M", "Office Closet", "belt"),
        ("Accessories", "Silver Watch", "Silver", "One Size", "Office Closet", "watch"),
        ("Accessories", "Scarf", "Grey", "One Size", "Bedroom", "scarf"),
    ]
    
    for item_type, name, color, size, location_name, specific_type in items_data:
        location = wardrobe.get_location(1) if location_name == "Bedroom" else wardrobe.get_location(2)
        if item_type == "Shoes":
            wardrobe.add_shoes(name, color, size, specific_type, location)
        elif item_type == "Clothing":
            wardrobe.add_clothing(name, color, size, specific_type, location)
        else:
            wardrobe.add_accessories(name, color, size, specific_type, location)
    
    # Create outfits
    work_outfit = wardrobe.create_outfit("Business Casual", "For office")
    work_outfit.add_item(wardrobe.get_item(2))  # Black heels
    work_outfit.add_item(wardrobe.get_item(4))  # White blouse
    work_outfit.add_item(wardrobe.get_item(5))  # Black pants
    work_outfit.add_item(wardrobe.get_item(8))  # Black belt
    
    casual_outfit = wardrobe.create_outfit("Weekend Casual", "Relaxed look")
    casual_outfit.add_item(wardrobe.get_item(1))  # Nike sneakers
    casual_outfit.add_item(wardrobe.get_item(3))  # Blue T-shirt
    casual_outfit.add_item(wardrobe.get_item(6))  # Denim jeans
    
    # Generate reports
    FileManager.generate_wardrobe_report(wardrobe, "example4_inventory.txt")
    FileManager.generate_outfit_details_report(wardrobe, "example4_outfits.txt")
    
    print("✓ Reports generated:")
    print("  - example4_inventory.txt (comprehensive inventory)")
    print("  - example4_outfits.txt (outfit details)")
    
    print("\nWardrobe Summary:")
    print(f"  Total Items: {len(wardrobe.list_items())}")
    print(f"  Locations: {len(wardrobe.list_locations())}")
    print(f"  Outfits: {len(wardrobe.list_outfits())}")
    print(f"  Complete Outfits: {len(wardrobe.list_complete_outfits())}")


def example_5_bulk_export():
    """Example 5: Export All Data at Once"""
    print("\n" + "="*70)
    print("EXAMPLE 5: Bulk Export - All Data in Multiple Formats")
    print("="*70)
    
    wardrobe = Wardrobe("example5.json")
    
    # Build wardrobe
    closet = wardrobe.add_location("Closet", "Main closet")
    drawer = wardrobe.add_location("Drawer", "Accessories drawer")
    
    # Add items
    shoes = wardrobe.add_shoes("Adidas", "Black", "9", location=closet)
    shirt = wardrobe.add_clothing("Casual Shirt", "Red", "M", location=drawer)
    accessory = wardrobe.add_accessories("Watch", "Silver", "One Size", location=drawer)
    
    # Create outfit
    outfit = wardrobe.create_outfit("Casual Weekend")
    outfit.add_item(shoes)
    outfit.add_item(shirt)
    outfit.add_item(accessory)
    
    # Export everything at once
    print("\nExporting all data to 'example5_export' folder...")
    FileManager.export_all_data(wardrobe, "example5_export")
    
    print("\nGenerated files:")
    import os
    if os.path.exists("example5_export"):
        files = os.listdir("example5_export")
        for file in sorted(files):
            file_path = os.path.join("example5_export", file)
            file_size = os.path.getsize(file_path)
            print(f"  ✓ {file} ({file_size} bytes)")


def example_6_color_analysis():
    """Example 6: Analyze Wardrobe Colors"""
    print("\n" + "="*70)
    print("EXAMPLE 6: Color Analysis from Generated Report")
    print("="*70)
    
    wardrobe = Wardrobe("example6.json")
    
    # Add items with various colors
    colors = ["Blue", "Black", "White", "Blue", "Red", "Black", "Grey", "White", "Blue"]
    for i, color in enumerate(colors, 1):
        if i % 3 == 0:
            wardrobe.add_clothing(f"Item {i}", color, "M")
        elif i % 3 == 1:
            wardrobe.add_shoes(f"Shoes {i}", color, "10")
        else:
            wardrobe.add_accessories(f"Accessory {i}", color, "One Size")
    
    # Generate report
    FileManager.generate_wardrobe_report(wardrobe, "example6_analysis.txt")
    
    # Also print color statistics here
    print("\nColor Statistics in Wardrobe:")
    color_counts = {}
    for item in wardrobe.list_items():
        color_counts[item.color] = color_counts.get(item.color, 0) + 1
    
    for color, count in sorted(color_counts.items(), key=lambda x: -x[1]):
        percentage = (count / len(wardrobe.list_items())) * 100
        bar = "█" * int(percentage / 5)
        print(f"  {color:12} {count:2} items ({percentage:5.1f}%) {bar}")
    
    print(f"\nDetailed analysis saved to: example6_analysis.txt")


def example_7_data_migration():
    """Example 7: Data Migration Between Wardrobes"""
    print("\n" + "="*70)
    print("EXAMPLE 7: Data Migration - Export from One, Import to Another")
    print("="*70)
    
    # Create first wardrobe and add items
    print("Step 1: Creating source wardrobe...")
    wardrobe1 = Wardrobe("source.json")
    wardrobe1.add_location("Bedroom")
    wardrobe1.add_shoes("Nike", "White", "10")
    wardrobe1.add_clothing("Shirt", "Blue", "M")
    wardrobe1.add_accessories("Belt", "Brown", "M")
    
    # Export from first wardrobe
    print("Step 2: Exporting from source wardrobe...")
    FileManager.export_items_to_csv(wardrobe1, "migration_data.csv")
    
    # Create second wardrobe and import
    print("Step 3: Importing into destination wardrobe...")
    wardrobe2 = Wardrobe("destination.json")
    imported, failed = FileManager.import_items_from_csv(wardrobe2, "migration_data.csv")
    
    print(f"\nMigration Complete:")
    print(f"  Source items: {len(wardrobe1.list_items())}")
    print(f"  Destination items: {len(wardrobe2.list_items())}")
    print(f"  Successfully migrated: {imported} items")
    print(f"  Failed: {failed} items")
    
    print("\nSource wardrobe items:")
    for item in wardrobe1.list_items():
        print(f"  - {item.name}")
    
    print("\nDestination wardrobe items:")
    for item in wardrobe2.list_items():
        print(f"  - {item.name}")


def main():
    """Run all examples"""
    print("\n" + "="*70)
    print("FILE I/O OPERATIONS - PRACTICAL EXAMPLES")
    print("="*70)
    
    try:
        example_1_basic_export()
        example_2_bulk_import()
        example_3_outfit_export()
        example_4_generate_reports()
        example_5_bulk_export()
        example_6_color_analysis()
        example_7_data_migration()
        
        print("\n" + "="*70)
        print("ALL EXAMPLES COMPLETED!")
        print("="*70)
        print("\nGenerated Files:")
        import os
        files = [f for f in os.listdir(".") if any(
            f.startswith(prefix) for prefix in ["example", "migration"]
        ) and f.endswith((".csv", ".txt", ".json")) or os.path.isdir(f) and f.startswith("example")]
        
        for file in sorted(files):
            if os.path.isfile(file):
                size = os.path.getsize(file)
                print(f"  - {file} ({size} bytes)")
            elif os.path.isdir(file):
                print(f"  - {file}/ (folder)")
        
        print("\nOpen these files to see the results!")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

"""
CLI Interface with File I/O Operations
Supports importing/exporting data in multiple formats (CSV, TXT, JSON)
"""

from clothing_manager_complete import Wardrobe
from file_manager import FileManager


class WardrobeCLI:
    """Command-line interface with file I/O capabilities."""
    
    def __init__(self):
        self.wardrobe = Wardrobe()
        self.file_manager = FileManager()
    
    def print_main_menu(self):
        """Display the main menu."""
        print("\n" + "="*50)
        print("        CLOTHING WARDROBE MANAGER")
        print("        (With File I/O Operations)")
        print("="*50)
        print("\n[CORE OPERATIONS]")
        print("1. Add Location")
        print("2. Add Clothing Item")
        print("3. Create Outfit")
        print("4. Assign Location to Item")
        print("5. List Items")
        print("6. List Outfits")
        print("\n[FILE I/O OPERATIONS]")
        print("7. Export Items to CSV")
        print("8. Export Outfits to CSV")
        print("9. Export Locations to CSV")
        print("10. Import Items from CSV")
        print("11. Generate Wardrobe Report (TXT)")
        print("12. Generate Outfit Details Report (TXT)")
        print("13. Export All Data (Multiple Formats)")
        print("\n[DATA MANAGEMENT]")
        print("14. View Item Details")
        print("15. View Outfit Details")
        print("16. Save Wardrobe Data (JSON)")
        print("17. Exit")
        print("="*50)
    
    # ===== CORE OPERATIONS =====
    
    def add_location(self):
        """Add a new location."""
        print("\n--- Add Location ---")
        name = input("Enter location name (e.g., 'Drawer 1'): ").strip()
        if not name:
            print("Location name cannot be empty!")
            return
        
        description = input("Enter description (optional): ").strip()
        location = self.wardrobe.add_location(name, description)
        print(f"✓ Location added: {location}")
    
    def add_clothing_item(self):
        """Add a clothing item to the wardrobe."""
        print("\n--- Add Clothing Item ---")
        print("1. Shoes")
        print("2. Clothing")
        print("3. Accessories")
        
        choice = input("Select type (1-3): ").strip()
        
        name = input("Enter item name: ").strip()
        color = input("Enter color: ").strip()
        size = input("Enter size: ").strip()
        
        if choice == "1":
            shoe_type = input("Enter shoe type [default: shoes]: ").strip() or "shoes"
            item = self.wardrobe.add_shoes(name, color, size, shoe_type)
            print(f"✓ Shoes added: {item}")
        elif choice == "2":
            clothing_type = input("Enter clothing type [default: shirt]: ").strip() or "shirt"
            item = self.wardrobe.add_clothing(name, color, size, clothing_type)
            print(f"✓ Clothing added: {item}")
        elif choice == "3":
            accessory_type = input("Enter accessory type [default: general]: ").strip() or "general"
            item = self.wardrobe.add_accessories(name, color, size, accessory_type)
            print(f"✓ Accessories added: {item}")
        else:
            print("Invalid choice!")
    
    def assign_location_to_item(self):
        """Assign a location to a clothing item."""
        print("\n--- Assign Location to Item ---")
        
        items = self.wardrobe.list_items()
        if not items:
            print("No items available!")
            return
        
        locations = self.wardrobe.list_locations()
        if not locations:
            print("No locations available! Please add locations first.")
            return
        
        print("\nAvailable items:")
        for item in items:
            print(f"  {item.item_id}. {item.name} ({item.get_type()})")
        
        try:
            item_id = int(input("\nEnter item ID: ").strip())
            item = self.wardrobe.get_item(item_id)
            if not item:
                print("Invalid item ID!")
                return
            
            print("\nAvailable locations:")
            for location in locations:
                print(f"  {location.location_id}. {location.name}")
            
            location_id = int(input("\nEnter location ID: ").strip())
            location = self.wardrobe.get_location(location_id)
            if not location:
                print("Invalid location ID!")
                return
            
            item.assign_location(location)
            print(f"✓ Assigned '{location.name}' to '{item.name}'")
        except ValueError:
            print("Invalid input!")
    
    def create_outfit(self):
        """Create a new outfit."""
        print("\n--- Create Outfit ---")
        name = input("Enter outfit name: ").strip()
        if not name:
            print("Outfit name cannot be empty!")
            return
        
        description = input("Enter description (optional): ").strip()
        outfit = self.wardrobe.create_outfit(name, description)
        print(f"✓ Outfit created: {outfit}")
        
        # Ask if user wants to add items to the outfit
        add_items = input("Add items to outfit? (y/n): ").strip().lower()
        if add_items == 'y':
            self.add_items_to_outfit(outfit.outfit_id)
    
    def add_items_to_outfit(self, outfit_id: int):
        """Add items to an outfit."""
        items = self.wardrobe.list_items()
        if not items:
            print("No items available!")
            return
        
        print(f"\n--- Add Items to Outfit {outfit_id} ---")
        while True:
            print("Available items:")
            for item in items:
                in_outfit = "✓" if item in self.wardrobe.get_outfit(outfit_id).get_items() else " "
                print(f"  [{in_outfit}] {item.item_id}. {item.name} ({item.get_type()})")
            
            item_id = input("\nEnter item ID (0 to finish): ").strip()
            if item_id == "0":
                break
            
            try:
                item_id = int(item_id)
                if self.wardrobe.add_item_to_outfit(outfit_id, item_id):
                    item = self.wardrobe.get_item(item_id)
                    print(f"✓ Added {item.name}")
                else:
                    print("Could not add item!")
            except ValueError:
                print("Invalid item ID!")
    
    def list_items(self):
        """List all items."""
        items = self.wardrobe.list_items()
        if not items:
            print("\n--- No items in wardrobe ---")
            return
        
        print("\n--- All Items ---")
        for item in items:
            print(f"  {item}")
    
    def list_outfits(self):
        """List all outfits."""
        outfits = self.wardrobe.list_outfits()
        if not outfits:
            print("\n--- No outfits ---")
            return
        
        print("\n--- All Outfits ---")
        for outfit in outfits:
            print(f"  {outfit}")
    
    # ===== FILE I/O OPERATIONS =====
    
    def export_items_csv(self):
        """Export items to CSV."""
        print("\n--- Export Items to CSV ---")
        filename = input("Enter filename [default: wardrobe_items.csv]: ").strip() or "wardrobe_items.csv"
        
        self.file_manager.export_items_to_csv(self.wardrobe, filename)
    
    def export_outfits_csv(self):
        """Export outfits to CSV."""
        print("\n--- Export Outfits to CSV ---")
        filename = input("Enter filename [default: wardrobe_outfits.csv]: ").strip() or "wardrobe_outfits.csv"
        
        self.file_manager.export_outfits_to_csv(self.wardrobe, filename)
    
    def export_locations_csv(self):
        """Export locations to CSV."""
        print("\n--- Export Locations to CSV ---")
        filename = input("Enter filename [default: wardrobe_locations.csv]: ").strip() or "wardrobe_locations.csv"
        
        self.file_manager.export_locations_to_csv(self.wardrobe, filename)
    
    def import_items_csv(self):
        """Import items from CSV."""
        print("\n--- Import Items from CSV ---")
        
        # List available CSV files
        csv_files = self.file_manager.list_available_imports()
        if csv_files:
            print("Available CSV files:")
            for i, file in enumerate(csv_files, 1):
                print(f"  {i}. {file}")
        
        filename = input("Enter filename to import from: ").strip()
        if filename:
            imported, failed = self.file_manager.import_items_from_csv(self.wardrobe, filename)
            print(f"Result: {imported} imported, {failed} failed")
    
    def generate_wardrobe_report(self):
        """Generate comprehensive wardrobe report."""
        print("\n--- Generate Wardrobe Report ---")
        filename = input("Enter filename [default: wardrobe_report.txt]: ").strip() or "wardrobe_report.txt"
        
        self.file_manager.generate_wardrobe_report(self.wardrobe, filename)
    
    def generate_outfit_report(self):
        """Generate outfit details report."""
        print("\n--- Generate Outfit Details Report ---")
        filename = input("Enter filename [default: outfit_details.txt]: ").strip() or "outfit_details.txt"
        
        self.file_manager.generate_outfit_details_report(self.wardrobe, filename)
    
    def export_all_data(self):
        """Export all data in multiple formats."""
        print("\n--- Export All Data ---")
        folder = input("Enter folder name [default: exports]: ").strip() or "exports"
        
        self.file_manager.export_all_data(self.wardrobe, folder)
    
    # ===== DETAIL VIEWS =====
    
    def view_item_details(self):
        """View details of a specific item."""
        items = self.wardrobe.list_items()
        if not items:
            print("\n--- No items available ---")
            return
        
        print("\n--- Select Item ---")
        for item in items:
            print(f"  {item.item_id}. {item.name}")
        
        try:
            item_id = int(input("Enter item ID: ").strip())
            item = self.wardrobe.get_item(item_id)
            if not item:
                print("Invalid item ID!")
                return
            
            print(f"\n--- Item Details ---")
            print(f"ID: {item.item_id}")
            print(f"Type: {item.get_type()}")
            print(f"Name: {item.name}")
            print(f"Color: {item.color}")
            print(f"Size: {item.size}")
            
            # Display specific subtype if available
            if hasattr(item, 'shoe_type'):
                print(f"Shoe Type: {item.shoe_type}")
            elif hasattr(item, 'clothing_type'):
                print(f"Clothing Type: {item.clothing_type}")
            elif hasattr(item, 'accessory_type'):
                print(f"Accessory Type: {item.accessory_type}")
            
            print(f"Location: {item.location.name if item.location else 'Not assigned'}")
            print(f"Date Added: {item.date_added}")
            
            # Check if in outfits
            outfits_with_item = [o for o in self.wardrobe.list_outfits() 
                                 if item in o.get_items()]
            if outfits_with_item:
                print(f"In Outfits: {', '.join([o.name for o in outfits_with_item])}")
        except ValueError:
            print("Invalid item ID!")
    
    def view_outfit_details(self):
        """View details of a specific outfit."""
        outfits = self.wardrobe.list_outfits()
        if not outfits:
            print("\n--- No outfits available ---")
            return
        
        print("\n--- Select Outfit ---")
        for outfit in outfits:
            print(f"  {outfit.outfit_id}. {outfit.name}")
        
        try:
            outfit_id = int(input("Enter outfit ID: ").strip())
            outfit = self.wardrobe.get_outfit(outfit_id)
            if not outfit:
                print("Invalid outfit ID!")
                return
            
            print(f"\n--- Outfit Details ---")
            print(f"Name: {outfit.name}")
            print(f"Description: {outfit.description if outfit.description else 'N/A'}")
            print(f"Status: {'✓ Complete' if outfit.is_complete() else '✗ Incomplete'}")
            
            items = outfit.get_items()
            print(f"Items ({len(items)}):")
            if items:
                for item in items:
                    print(f"  - {item.name} ({item.get_type()}, {item.color})")
            else:
                print("  (empty)")
            
            if items:
                print(f"Color Scheme: {', '.join(outfit.get_color_scheme())}")
        except ValueError:
            print("Invalid outfit ID!")
    
    def save_data(self):
        """Save wardrobe data to JSON."""
        self.wardrobe.save_data()
        print("✓ Wardrobe data saved!")
    
    def run(self):
        """Run the CLI application."""
        print("\n" + "="*50)
        print("  Wardrobe Manager with File I/O")
        print("="*50)
        
        while True:
            self.print_main_menu()
            choice = input("Enter your choice (1-17): ").strip()
            
            if choice == "1":
                self.add_location()
            elif choice == "2":
                self.add_clothing_item()
            elif choice == "3":
                self.create_outfit()
            elif choice == "4":
                self.assign_location_to_item()
            elif choice == "5":
                self.list_items()
            elif choice == "6":
                self.list_outfits()
            elif choice == "7":
                self.export_items_csv()
            elif choice == "8":
                self.export_outfits_csv()
            elif choice == "9":
                self.export_locations_csv()
            elif choice == "10":
                self.import_items_csv()
            elif choice == "11":
                self.generate_wardrobe_report()
            elif choice == "12":
                self.generate_outfit_report()
            elif choice == "13":
                self.export_all_data()
            elif choice == "14":
                self.view_item_details()
            elif choice == "15":
                self.view_outfit_details()
            elif choice == "16":
                self.save_data()
            elif choice == "17":
                confirm = input("Save data before exiting? (y/n): ").strip().lower()
                if confirm == 'y':
                    self.save_data()
                print("Goodbye!")
                break
            else:
                print("Invalid choice! Please try again.")


if __name__ == "__main__":
    cli = WardrobeCLI()
    cli.run()

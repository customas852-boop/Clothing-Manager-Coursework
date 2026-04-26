"""
File I/O Manager for Clothing Wardrobe Manager
Implements reading from and writing to files in multiple formats:
- CSV: For importing/exporting items and outfits
- TXT: For generating reports and summaries
- JSON: For data persistence (already implemented in main module)
"""

import csv
import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from clothing_manager import Wardrobe, ClothingItem, Location, Outfit


class FileManager:
    """
    Handles all file I/O operations for the Wardrobe Manager.
    
    Supported Formats:
    - CSV: Comma-separated values for easy spreadsheet import/export
    - TXT: Human-readable text reports
    - JSON: Data persistence (handled by Wardrobe class)
    """
    
    # ========== CSV EXPORT ==========
    
    @staticmethod
    def export_items_to_csv(wardrobe: Wardrobe, filename: str = "wardrobe_items.csv") -> bool:
        """
        Export all clothing items to CSV file.
        
        CSV Format:
        ID,Type,Name,Color,Size,Location,Date Added,Specific Type
        
        Args:
            wardrobe: Wardrobe instance
            filename: Output CSV filename
        
        Returns:
            True if successful, False otherwise
        """
        try:
            items = wardrobe.list_items()
            if not items:
                print("No items to export!")
                return False
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['ID', 'Type', 'Name', 'Color', 'Size', 'Location', 'Date Added', 'Specific Type']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                
                for item in items:
                    specific_type = ""
                    if hasattr(item, 'shoe_type'):
                        specific_type = item.shoe_type
                    elif hasattr(item, 'clothing_type'):
                        specific_type = item.clothing_type
                    elif hasattr(item, 'accessory_type'):
                        specific_type = item.accessory_type
                    
                    writer.writerow({
                        'ID': item.item_id,
                        'Type': item.get_type(),
                        'Name': item.name,
                        'Color': item.color,
                        'Size': item.size,
                        'Location': item.location.name if item.location else 'Not assigned',
                        'Date Added': item.date_added,
                        'Specific Type': specific_type
                    })
            
            print(f"✓ Exported {len(items)} items to {filename}")
            return True
        
        except Exception as e:
            print(f"✗ Error exporting items: {e}")
            return False
    
    @staticmethod
    def export_outfits_to_csv(wardrobe: Wardrobe, filename: str = "wardrobe_outfits.csv") -> bool:
        """
        Export all outfits to CSV file.
        
        CSV Format:
        ID,Name,Description,Status,Item Count,Items,Color Scheme,Created
        
        Args:
            wardrobe: Wardrobe instance
            filename: Output CSV filename
        
        Returns:
            True if successful, False otherwise
        """
        try:
            outfits = wardrobe.list_outfits()
            if not outfits:
                print("No outfits to export!")
                return False
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['ID', 'Name', 'Description', 'Status', 'Item Count', 'Items', 'Color Scheme', 'Created']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                
                for outfit in outfits:
                    items = outfit.get_items()
                    item_names = "; ".join([f"{i.name}({i.get_type()})" for i in items])
                    colors = ", ".join(outfit.get_color_scheme())
                    
                    writer.writerow({
                        'ID': outfit.outfit_id,
                        'Name': outfit.name,
                        'Description': outfit.description,
                        'Status': '✓ Complete' if outfit.is_complete() else '✗ Incomplete',
                        'Item Count': len(items),
                        'Items': item_names,
                        'Color Scheme': colors,
                        'Created': outfit.created_at
                    })
            
            print(f"✓ Exported {len(outfits)} outfits to {filename}")
            return True
        
        except Exception as e:
            print(f"✗ Error exporting outfits: {e}")
            return False
    
    @staticmethod
    def export_locations_to_csv(wardrobe: Wardrobe, filename: str = "wardrobe_locations.csv") -> bool:
        """
        Export all locations to CSV file.
        
        CSV Format:
        ID,Name,Description,Item Count
        
        Args:
            wardrobe: Wardrobe instance
            filename: Output CSV filename
        
        Returns:
            True if successful, False otherwise
        """
        try:
            locations = wardrobe.list_locations()
            if not locations:
                print("No locations to export!")
                return False
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['ID', 'Name', 'Description', 'Item Count']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                
                for location in locations:
                    items_in_location = wardrobe.list_items_by_location(location.location_id)
                    
                    writer.writerow({
                        'ID': location.location_id,
                        'Name': location.name,
                        'Description': location.description,
                        'Item Count': len(items_in_location)
                    })
            
            print(f"✓ Exported {len(locations)} locations to {filename}")
            return True
        
        except Exception as e:
            print(f"✗ Error exporting locations: {e}")
            return False
    
    # ========== CSV IMPORT ==========
    
    @staticmethod
    def import_items_from_csv(wardrobe: Wardrobe, filename: str) -> Tuple[int, int]:
        """
        Import items from CSV file.
        
        CSV Format Expected:
        Type,Name,Color,Size,Location,Specific Type
        Shoes,Nike Sneakers,White,10,Drawer 1,sneakers
        Clothing,Blue T-Shirt,Blue,M,Shelf,shirt
        
        Args:
            wardrobe: Wardrobe instance
            filename: Input CSV filename
        
        Returns:
            Tuple of (items_imported, items_failed)
        """
        if not os.path.exists(filename):
            print(f"✗ File not found: {filename}")
            return (0, 0)
        
        imported = 0
        failed = 0
        
        try:
            with open(filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row_num, row in enumerate(reader, start=2):  # Start at 2 (after header)
                    try:
                        item_type = row.get('Type', '').strip()
                        name = row.get('Name', '').strip()
                        color = row.get('Color', '').strip()
                        size = row.get('Size', '').strip()
                        location_name = row.get('Location', '').strip()
                        specific_type = row.get('Specific Type', '').strip()
                        
                        # Validate required fields
                        if not all([item_type, name, color, size]):
                            print(f"  Row {row_num}: Missing required fields - skipped")
                            failed += 1
                            continue
                        
                        # Get location if specified
                        location = None
                        if location_name:
                            # Check if location exists
                            locations = wardrobe.list_locations()
                            location = next((loc for loc in locations if loc.name == location_name), None)
                            
                            if not location:
                                # Create new location if doesn't exist
                                location = wardrobe.add_location(location_name)
                        
                        # Create item based on type
                        if item_type == "Shoes":
                            wardrobe.add_shoes(name, color, size, specific_type or "shoes", location)
                            imported += 1
                        elif item_type == "Clothing":
                            wardrobe.add_clothing(name, color, size, specific_type or "shirt", location)
                            imported += 1
                        elif item_type == "Accessories":
                            wardrobe.add_accessories(name, color, size, specific_type or "general", location)
                            imported += 1
                        else:
                            print(f"  Row {row_num}: Unknown item type '{item_type}' - skipped")
                            failed += 1
                    
                    except Exception as e:
                        print(f"  Row {row_num}: Error - {e}")
                        failed += 1
            
            print(f"✓ Imported {imported} items ({failed} failed)")
            return (imported, failed)
        
        except Exception as e:
            print(f"✗ Error importing items: {e}")
            return (0, 0)
    
    # ========== TXT REPORTS ==========
    
    @staticmethod
    def generate_wardrobe_report(wardrobe: Wardrobe, filename: str = "wardrobe_report.txt") -> bool:
        """
        Generate a comprehensive text report of the wardrobe.
        
        Report includes:
        - Summary statistics
        - All locations with item counts
        - Items organized by type
        - All outfits with details
        - Color statistics
        
        Args:
            wardrobe: Wardrobe instance
            filename: Output TXT filename
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                # Header
                f.write("="*70 + "\n")
                f.write("WARDROBE INVENTORY REPORT\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*70 + "\n\n")
                
                # Summary
                all_items = wardrobe.list_items()
                all_outfits = wardrobe.list_outfits()
                all_locations = wardrobe.list_locations()
                
                f.write("SUMMARY\n")
                f.write("-" * 70 + "\n")
                f.write(f"Total Items: {len(all_items)}\n")
                f.write(f"Total Locations: {len(all_locations)}\n")
                f.write(f"Total Outfits: {len(all_outfits)}\n")
                f.write(f"Complete Outfits: {len(wardrobe.list_complete_outfits())}\n")
                f.write(f"Shoes: {len(wardrobe.list_items_by_type('Shoes'))}\n")
                f.write(f"Clothing: {len(wardrobe.list_items_by_type('Clothing'))}\n")
                f.write(f"Accessories: {len(wardrobe.list_items_by_type('Accessories'))}\n")
                f.write("\n")
                
                # Locations
                f.write("LOCATIONS\n")
                f.write("-" * 70 + "\n")
                if all_locations:
                    for location in all_locations:
                        items_in_loc = wardrobe.list_items_by_location(location.location_id)
                        f.write(f"\n[{location.location_id}] {location.name}\n")
                        if location.description:
                            f.write(f"    Description: {location.description}\n")
                        f.write(f"    Items: {len(items_in_loc)}\n")
                        if items_in_loc:
                            for item in items_in_loc:
                                f.write(f"      - {item.name} ({item.get_type()}, {item.color})\n")
                else:
                    f.write("No locations defined.\n")
                f.write("\n")
                
                # Items by Type
                f.write("ITEMS BY TYPE\n")
                f.write("-" * 70 + "\n")
                
                for item_type in ["Shoes", "Clothing", "Accessories"]:
                    items = wardrobe.list_items_by_type(item_type)
                    f.write(f"\n{item_type.upper()} ({len(items)})\n")
                    if items:
                        for item in sorted(items, key=lambda x: x.name):
                            location = item.location.name if item.location else "Not assigned"
                            f.write(f"  [ID: {item.item_id}] {item.name}\n")
                            f.write(f"      Color: {item.color}, Size: {item.size}, Location: {location}\n")
                    else:
                        f.write(f"  (none)\n")
                f.write("\n")
                
                # Outfits
                f.write("OUTFITS\n")
                f.write("-" * 70 + "\n")
                if all_outfits:
                    for outfit in all_outfits:
                        status = "✓ COMPLETE" if outfit.is_complete() else "✗ INCOMPLETE"
                        f.write(f"\n[ID: {outfit.outfit_id}] {outfit.name} - {status}\n")
                        if outfit.description:
                            f.write(f"    Description: {outfit.description}\n")
                        
                        items = outfit.get_items()
                        f.write(f"    Items ({len(items)}):\n")
                        if items:
                            for item in items:
                                f.write(f"      - {item.name} ({item.get_type()}, {item.color})\n")
                        else:
                            f.write(f"      (empty)\n")
                        
                        if items:
                            colors = outfit.get_color_scheme()
                            f.write(f"    Color Scheme: {', '.join(colors)}\n")
                else:
                    f.write("No outfits defined.\n")
                f.write("\n")
                
                # Color Statistics
                if all_items:
                    f.write("COLOR STATISTICS\n")
                    f.write("-" * 70 + "\n")
                    color_counts = {}
                    for item in all_items:
                        color_counts[item.color] = color_counts.get(item.color, 0) + 1
                    
                    for color, count in sorted(color_counts.items(), key=lambda x: -x[1]):
                        f.write(f"  {color}: {count} items\n")
                    f.write("\n")
                
                # Footer
                f.write("="*70 + "\n")
                f.write("END OF REPORT\n")
                f.write("="*70 + "\n")
            
            print(f"✓ Report generated: {filename}")
            return True
        
        except Exception as e:
            print(f"✗ Error generating report: {e}")
            return False
    
    @staticmethod
    def generate_outfit_details_report(wardrobe: Wardrobe, filename: str = "outfit_details.txt") -> bool:
        """
        Generate detailed report for each outfit.
        
        Args:
            wardrobe: Wardrobe instance
            filename: Output TXT filename
        
        Returns:
            True if successful, False otherwise
        """
        try:
            outfits = wardrobe.list_outfits()
            if not outfits:
                print("No outfits to report on!")
                return False
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("="*70 + "\n")
                f.write("OUTFIT DETAILS REPORT\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*70 + "\n\n")
                
                for i, outfit in enumerate(outfits, 1):
                    f.write(f"OUTFIT {i}: {outfit.name}\n")
                    f.write("-" * 70 + "\n")
                    f.write(f"ID: {outfit.outfit_id}\n")
                    f.write(f"Description: {outfit.description if outfit.description else 'N/A'}\n")
                    f.write(f"Status: {'✓ Complete' if outfit.is_complete() else '✗ Incomplete'}\n")
                    f.write(f"Created: {outfit.created_at}\n")
                    
                    items = outfit.get_items()
                    f.write(f"\nItems ({len(items)}):\n")
                    
                    # Group by type
                    by_type = {}
                    for item in items:
                        item_type = item.get_type()
                        if item_type not in by_type:
                            by_type[item_type] = []
                        by_type[item_type].append(item)
                    
                    for item_type in ["Shoes", "Clothing", "Accessories"]:
                        if item_type in by_type:
                            f.write(f"\n  {item_type}:\n")
                            for item in by_type[item_type]:
                                f.write(f"    • {item.name}\n")
                                f.write(f"      Color: {item.color}, Size: {item.size}\n")
                                if item.location:
                                    f.write(f"      Location: {item.location.name}\n")
                    
                    # Requirements check
                    f.write(f"\nRequirements Check:\n")
                    requirements = outfit.has_required_items()
                    f.write(f"  Has Shoes: {'✓' if requirements['has_shoes'] else '✗'}\n")
                    f.write(f"  Has Clothing: {'✓' if requirements['has_clothing'] else '✗'}\n")
                    f.write(f"  Has Accessories: {'✓' if requirements['has_accessories'] else '✗'}\n")
                    
                    # Color scheme
                    colors = outfit.get_color_scheme()
                    f.write(f"\nColor Scheme: {', '.join(colors) if colors else 'N/A'}\n")
                    
                    f.write("\n" + "="*70 + "\n\n")
            
            print(f"✓ Outfit details report generated: {filename}")
            return True
        
        except Exception as e:
            print(f"✗ Error generating outfit details: {e}")
            return False
    
    # ========== UTILITY FUNCTIONS ==========
    
    @staticmethod
    def export_all_data(wardrobe: Wardrobe, folder: str = "exports") -> bool:
        """
        Export all data to multiple file formats in a folder.
        
        Creates folder with:
        - wardrobe_items.csv
        - wardrobe_outfits.csv
        - wardrobe_locations.csv
        - wardrobe_report.txt
        - outfit_details.txt
        
        Args:
            wardrobe: Wardrobe instance
            folder: Output folder name
        
        Returns:
            True if all exports successful
        """
        try:
            # Create folder if doesn't exist
            if not os.path.exists(folder):
                os.makedirs(folder)
            
            # Export all formats
            results = []
            results.append(FileManager.export_items_to_csv(wardrobe, os.path.join(folder, "wardrobe_items.csv")))
            results.append(FileManager.export_outfits_to_csv(wardrobe, os.path.join(folder, "wardrobe_outfits.csv")))
            results.append(FileManager.export_locations_to_csv(wardrobe, os.path.join(folder, "wardrobe_locations.csv")))
            results.append(FileManager.generate_wardrobe_report(wardrobe, os.path.join(folder, "wardrobe_report.txt")))
            results.append(FileManager.generate_outfit_details_report(wardrobe, os.path.join(folder, "outfit_details.txt")))
            
            if all(results):
                print(f"\n✓ All data exported to '{folder}' folder!")
                return True
            else:
                print(f"\n⚠ Some exports may have failed. Check messages above.")
                return False
        
        except Exception as e:
            print(f"✗ Error exporting all data: {e}")
            return False
    
    @staticmethod
    def list_available_imports(folder: str = ".") -> List[str]:
        """
        List all CSV files available for import in a folder.
        
        Args:
            folder: Folder to search
        
        Returns:
            List of CSV filenames
        """
        csv_files = []
        try:
            for file in os.listdir(folder):
                if file.endswith('.csv'):
                    csv_files.append(file)
            return sorted(csv_files)
        except Exception as e:
            print(f"Error listing files: {e}")
            return []

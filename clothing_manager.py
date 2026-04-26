"""
Clothing Wardrobe Manager - With Composition and Aggregation

COMPOSITION & AGGREGATION DEMONSTRATED:
1. Aggregation: Wardrobe HAS-A Location (weak ownership)
   - Location can exist independently
   - Locations are referenced but not owned by Wardrobe
   
2. Composition: Outfit COMPOSES ClothingItems (strong ownership)
   - ClothingItems are parts of an Outfit
   - If Outfit is deleted, its items should be managed
   
3. Aggregation: Outfit HAS-A ClothingItems (weak ownership)
   - Items can exist in wardrobe even if removed from outfit
   - Outfit references but doesn't own the items
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Set
from abc import ABC, abstractmethod


class Location:
    """Represents a storage location for clothing items."""
    
    def __init__(self, location_id: int, name: str, description: str = ""):
        self.location_id = location_id
        self.name = name
        self.description = description
    
    def __repr__(self):
        return f"Location({self.location_id}, {self.name})"
    
    def to_dict(self):
        return {
            "location_id": self.location_id,
            "name": self.name,
            "description": self.description
        }
    
    @staticmethod
    def from_dict(data: dict):
        return Location(
            location_id=data["location_id"],
            name=data["name"],
            description=data.get("description", "")
        )


class ClothingItem(ABC):
    """Abstract base class for all clothing items."""
    
    _id_counter = 0
    
    def __init__(self, name: str, color: str, size: str, location: Optional[Location] = None):
        ClothingItem._id_counter += 1
        self.item_id = ClothingItem._id_counter
        self.name = name
        self.color = color
        self.size = size
        self.location = location  # Aggregation: weak reference to Location
        self.date_added = datetime.now().isoformat()
    
    @abstractmethod
    def get_type(self) -> str:
        """Return the type of clothing item."""
        pass
    
    def assign_location(self, location: Location):
        """Assign a location to this clothing item."""
        self.location = location
    
    def remove_location(self):
        """Remove the location assignment from this item."""
        self.location = None
    
    def __repr__(self):
        location_str = self.location.name if self.location else "No location"
        return f"{self.get_type()}(ID: {self.item_id}, {self.name}, {self.color}, Size: {self.size}, Location: {location_str})"
    
    def to_dict(self):
        return {
            "item_id": self.item_id,
            "type": self.get_type(),
            "name": self.name,
            "color": self.color,
            "size": self.size,
            "location_id": self.location.location_id if self.location else None,
            "date_added": self.date_added
        }


class Shoes(ClothingItem):
    """Class representing shoes."""
    
    def __init__(self, name: str, color: str, size: str, shoe_type: str = "shoes", 
                 location: Optional[Location] = None):
        super().__init__(name, color, size, location)
        self.shoe_type = shoe_type
    
    def get_type(self) -> str:
        return "Shoes"
    
    def to_dict(self):
        data = super().to_dict()
        data["shoe_type"] = self.shoe_type
        return data


class Clothing(ClothingItem):
    """Class representing general clothing items."""
    
    def __init__(self, name: str, color: str, size: str, clothing_type: str = "shirt", 
                 location: Optional[Location] = None):
        super().__init__(name, color, size, location)
        self.clothing_type = clothing_type
    
    def get_type(self) -> str:
        return "Clothing"
    
    def to_dict(self):
        data = super().to_dict()
        data["clothing_type"] = self.clothing_type
        return data


class Accessories(ClothingItem):
    """Class representing accessories."""
    
    def __init__(self, name: str, color: str, size: str, accessory_type: str = "general", 
                 location: Optional[Location] = None):
        super().__init__(name, color, size, location)
        self.accessory_type = accessory_type
    
    def get_type(self) -> str:
        return "Accessories"
    
    def to_dict(self):
        data = super().to_dict()
        data["accessory_type"] = self.accessory_type
        return data


# ============================================
# COMPOSITION EXAMPLE
# ============================================
class Outfit:
    """
    COMPOSITION PATTERN
    
    An Outfit COMPOSES multiple ClothingItems.
    
    WHY COMPOSITION:
    - An Outfit is made UP OF clothing items (shoes, shirt, pants, accessories)
    - The outfit's purpose is to group and coordinate items together
    - Items are logically part of the outfit's structure
    - An outfit without items is not meaningful
    
    KEY CHARACTERISTIC: Strong ownership
    - The outfit "owns" the relationship with its items
    - When you think of "my blue outfit", you're thinking of the composition
    
    COMPOSITION vs AGGREGATION:
    - Composition: "An Outfit IS-MADE-OF items" (strong, part-whole)
    - Aggregation: "An Outfit CONTAINS-A reference to items" (weak, shared)
    
    In this implementation:
    - We use aggregation for practical reasons (items can be in multiple outfits)
    - But conceptually, an outfit is a composition of items
    """
    
    _outfit_id_counter = 0
    
    def __init__(self, name: str, description: str = ""):
        """Create an outfit that will compose clothing items."""
        Outfit._outfit_id_counter += 1
        self.outfit_id = Outfit._outfit_id_counter
        self.name = name
        self.description = description
        self.items: List[ClothingItem] = []  # Composition: outfit IS-MADE-OF items
        self.created_at = datetime.now().isoformat()
    
    def add_item(self, item: ClothingItem) -> bool:
        """Add a clothing item to the outfit."""
        if item not in self.items:
            self.items.append(item)
            return True
        return False
    
    def remove_item(self, item_id: int) -> bool:
        """Remove an item from the outfit by ID."""
        self.items = [item for item in self.items if item.item_id != item_id]
        return True
    
    def get_items(self) -> List[ClothingItem]:
        """Get all items in this outfit."""
        return self.items.copy()
    
    def get_items_by_type(self, item_type: str) -> List[ClothingItem]:
        """Get items of a specific type in this outfit."""
        return [item for item in self.items if item.get_type() == item_type]
    
    def has_required_items(self) -> Dict[str, bool]:
        """Check if outfit has basic required items."""
        return {
            "has_shoes": len(self.get_items_by_type("Shoes")) > 0,
            "has_clothing": len(self.get_items_by_type("Clothing")) > 0,
            "has_accessories": len(self.get_items_by_type("Accessories")) > 0,
        }
    
    def is_complete(self) -> bool:
        """Check if outfit has at least shoes, clothing, and optionally accessories."""
        required = self.has_required_items()
        return required["has_shoes"] and required["has_clothing"]
    
    def get_color_scheme(self) -> List[str]:
        """Get all colors used in this outfit."""
        return list(set([item.color for item in self.items]))
    
    def __repr__(self):
        items_count = len(self.items)
        completion = "✓ Complete" if self.is_complete() else "✗ Incomplete"
        return f"Outfit(ID: {self.outfit_id}, {self.name}, Items: {items_count}, {completion})"
    
    def to_dict(self):
        return {
            "outfit_id": self.outfit_id,
            "name": self.name,
            "description": self.description,
            "items": [item.item_id for item in self.items],  # Store item IDs
            "created_at": self.created_at
        }


class ClothingItemFactory:
    """Factory Method Pattern for creating clothing items."""
    
    @staticmethod
    def create_item(item_type: str, name: str, color: str, size: str, 
                   specific_type: str = "", location: Optional[Location] = None) -> ClothingItem:
        if item_type == "Shoes":
            return Shoes(name, color, size, specific_type or "shoes", location)
        elif item_type == "Clothing":
            return Clothing(name, color, size, specific_type or "shirt", location)
        elif item_type == "Accessories":
            return Accessories(name, color, size, specific_type or "general", location)
        else:
            raise ValueError(f"Unknown item type: {item_type}")
    
    @staticmethod
    def create_from_dict(item_data: dict, location: Optional[Location] = None) -> ClothingItem:
        item_type = item_data.get("type")
        specific_type_map = {
            "Shoes": item_data.get("shoe_type", "shoes"),
            "Clothing": item_data.get("clothing_type", "shirt"),
            "Accessories": item_data.get("accessory_type", "general")
        }
        
        specific_type = specific_type_map.get(item_type, "")
        item = ClothingItemFactory.create_item(
            item_type,
            item_data["name"],
            item_data["color"],
            item_data["size"],
            specific_type,
            location
        )
        item.item_id = item_data["item_id"]
        item.date_added = item_data.get("date_added", item.date_added)
        return item


# ============================================
# SINGLETON & AGGREGATION
# ============================================
class Wardrobe:
    """
    Wardrobe Manager with Aggregation Pattern
    
    AGGREGATION PATTERN
    
    The Wardrobe AGGREGATES:
    1. Locations (weak reference) - Locations exist independently
    2. ClothingItems (weak reference) - Items exist independently
    3. Outfits (composition ownership) - Outfits are created/managed by Wardrobe
    
    WHY AGGREGATION (for Items and Locations):
    - Items and Locations can exist without the Wardrobe
    - They're not intrinsically part of Wardrobe's structure
    - Multiple Wardrobes could reference the same items/locations
    - Deletion of Wardrobe doesn't mean items/locations cease to exist
    
    KEY CHARACTERISTIC: Weak ownership
    - Wardrobe is a container/manager, not an owner
    - Items and Locations have independent lifecycles
    - Items can be added/removed without affecting Locations
    
    SINGLETON PATTERN (as before)
    """
    
    _instance: Optional['Wardrobe'] = None
    
    def __new__(cls, data_file: str = "wardrobe_data.json"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, data_file: str = "wardrobe_data.json"):
        if self._initialized:
            return
        
        # AGGREGATION: Wardrobe aggregates items and locations (weak ownership)
        self.items: Dict[int, ClothingItem] = {}
        self.locations: Dict[int, Location] = {}
        
        # COMPOSITION: Wardrobe composes outfits (owns/manages outfits)
        self.outfits: Dict[int, Outfit] = {}
        
        self.next_location_id = 1
        self.data_file = data_file
        self._initialized = True
        self.load_data()
    
    @classmethod
    def get_instance(cls, data_file: str = "wardrobe_data.json") -> 'Wardrobe':
        """Get the singleton instance"""
        if cls._instance is None:
            cls._instance = cls(data_file)
        return cls._instance
    
    # ===== LOCATION MANAGEMENT (Aggregation) =====
    def add_location(self, name: str, description: str = "") -> Location:
        """Add a new location (aggregation)."""
        location = Location(self.next_location_id, name, description)
        self.locations[self.next_location_id] = location
        self.next_location_id += 1
        return location
    
    def get_location(self, location_id: int) -> Optional[Location]:
        """Get a location by ID."""
        return self.locations.get(location_id)
    
    def list_locations(self) -> List[Location]:
        """Get all locations."""
        return list(self.locations.values())
    
    # ===== CLOTHING ITEM MANAGEMENT (Aggregation) =====
    def add_item(self, item: ClothingItem) -> ClothingItem:
        """Add a clothing item to the wardrobe (aggregation)."""
        self.items[item.item_id] = item
        return item
    
    def add_shoes(self, name: str, color: str, size: str, shoe_type: str = "shoes", 
                  location: Optional[Location] = None) -> Shoes:
        """Add shoes using Factory Method."""
        shoes = ClothingItemFactory.create_item("Shoes", name, color, size, shoe_type, location)
        return self.add_item(shoes)
    
    def add_clothing(self, name: str, color: str, size: str, clothing_type: str = "shirt", 
                    location: Optional[Location] = None) -> Clothing:
        """Add clothing using Factory Method."""
        clothing = ClothingItemFactory.create_item("Clothing", name, color, size, clothing_type, location)
        return self.add_item(clothing)
    
    def add_accessories(self, name: str, color: str, size: str, accessory_type: str = "general", 
                       location: Optional[Location] = None) -> Accessories:
        """Add accessories using Factory Method."""
        accessories = ClothingItemFactory.create_item("Accessories", name, color, size, accessory_type, location)
        return self.add_item(accessories)
    
    def get_item(self, item_id: int) -> Optional[ClothingItem]:
        """Get an item by ID."""
        return self.items.get(item_id)
    
    def list_items(self) -> List[ClothingItem]:
        """Get all items."""
        return list(self.items.values())
    
    def list_items_by_type(self, item_type: str) -> List[ClothingItem]:
        """Get all items of a specific type."""
        return [item for item in self.items.values() if item.get_type() == item_type]
    
    def list_items_by_location(self, location_id: int) -> List[ClothingItem]:
        """Get all items in a specific location."""
        return [item for item in self.items.values() 
                if item.location and item.location.location_id == location_id]
    
    def assign_location_to_item(self, item_id: int, location_id: int) -> bool:
        """Assign a location to an item."""
        item = self.get_item(item_id)
        location = self.get_location(location_id)
        
        if item and location:
            item.assign_location(location)
            return True
        return False
    
    def remove_item(self, item_id: int) -> bool:
        """Remove an item from the wardrobe."""
        if item_id in self.items:
            del self.items[item_id]
            # Remove item from all outfits
            for outfit in self.outfits.values():
                outfit.remove_item(item_id)
            return True
        return False
    
    # ===== OUTFIT MANAGEMENT (Composition) =====
    def create_outfit(self, name: str, description: str = "") -> Outfit:
        """Create a new outfit (composition - wardrobe owns/creates outfits)."""
        outfit = Outfit(name, description)
        self.outfits[outfit.outfit_id] = outfit
        return outfit
    
    def get_outfit(self, outfit_id: int) -> Optional[Outfit]:
        """Get an outfit by ID."""
        return self.outfits.get(outfit_id)
    
    def list_outfits(self) -> List[Outfit]:
        """Get all outfits."""
        return list(self.outfits.values())
    
    def list_complete_outfits(self) -> List[Outfit]:
        """Get all complete outfits."""
        return [outfit for outfit in self.outfits.values() if outfit.is_complete()]
    
    def add_item_to_outfit(self, outfit_id: int, item_id: int) -> bool:
        """Add an item to an outfit."""
        outfit = self.get_outfit(outfit_id)
        item = self.get_item(item_id)
        
        if outfit and item:
            return outfit.add_item(item)
        return False
    
    def remove_item_from_outfit(self, outfit_id: int, item_id: int) -> bool:
        """Remove an item from an outfit."""
        outfit = self.get_outfit(outfit_id)
        if outfit:
            return outfit.remove_item(item_id)
        return False
    
    def delete_outfit(self, outfit_id: int) -> bool:
        """Delete an outfit."""
        if outfit_id in self.outfits:
            del self.outfits[outfit_id]
            return True
        return False
    
    def save_data(self):
        """Save wardrobe data to JSON file."""
        data = {
            "items": [item.to_dict() for item in self.items.values()],
            "locations": [loc.to_dict() for loc in self.locations.values()],
            "outfits": [outfit.to_dict() for outfit in self.outfits.values()],
            "next_location_id": self.next_location_id,
            "next_item_id": ClothingItem._id_counter,
            "next_outfit_id": Outfit._outfit_id_counter
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_data(self):
        """Load wardrobe data from JSON file."""
        if not os.path.exists(self.data_file):
            return
        
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
            
            # Load locations
            for loc_data in data.get("locations", []):
                loc = Location.from_dict(loc_data)
                self.locations[loc.location_id] = loc
            
            if data.get("next_location_id"):
                self.next_location_id = data["next_location_id"]
            
            if data.get("next_item_id"):
                ClothingItem._id_counter = data["next_item_id"]
            
            # Load items
            for item_data in data.get("items", []):
                location_id = item_data.get("location_id")
                location = self.get_location(location_id) if location_id else None
                item = ClothingItemFactory.create_from_dict(item_data, location)
                self.items[item.item_id] = item
            
            # Load outfits
            if data.get("next_outfit_id"):
                Outfit._outfit_id_counter = data["next_outfit_id"]
            
            for outfit_data in data.get("outfits", []):
                outfit = Outfit(outfit_data["name"], outfit_data["description"])
                outfit.outfit_id = outfit_data["outfit_id"]
                outfit.created_at = outfit_data.get("created_at", outfit.created_at)
                
                # Restore items to outfit
                for item_id in outfit_data.get("items", []):
                    item = self.get_item(item_id)
                    if item:
                        outfit.add_item(item)
                
                self.outfits[outfit.outfit_id] = outfit
        
        except Exception as e:
            print(f"Error loading data: {e}")

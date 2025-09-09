#!/usr/bin/env python3
"""
Stock Management System

This module provides functionality for managing stock inventory including
adding, removing, updating, and reporting stock items.
"""

from datetime import datetime
from typing import Dict, List, Optional


class Stock:
    """Represents a stock item in the inventory."""
    
    def __init__(self, item_id: str, name: str, quantity: int = 0, price: float = 0.0):
        """
        Initialize a stock item.
        
        Args:
            item_id: Unique identifier for the stock item
            name: Name/description of the stock item
            quantity: Current quantity in stock (default: 0)
            price: Price per unit (default: 0.0)
        """
        self.item_id = item_id
        self.name = name
        self.quantity = quantity
        self.price = price
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def __str__(self) -> str:
        return f"Stock(id={self.item_id}, name={self.name}, qty={self.quantity}, price={self.price})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def update_quantity(self, new_quantity: int) -> None:
        """Update the stock quantity."""
        if new_quantity < 0:
            raise ValueError("Quantity cannot be negative")
        self.quantity = new_quantity
        self.updated_at = datetime.now()
    
    def update_price(self, new_price: float) -> None:
        """Update the stock item price."""
        if new_price < 0:
            raise ValueError("Price cannot be negative")
        self.price = new_price
        self.updated_at = datetime.now()


class StockManager:
    """Manages stock inventory operations."""
    
    def __init__(self):
        """Initialize the stock manager."""
        self._inventory: Dict[str, Stock] = {}
    
    def add_stock_item(self, item_id: str, name: str, quantity: int = 0, price: float = 0.0) -> Stock:
        """
        Add a new stock item to the inventory.
        
        Args:
            item_id: Unique identifier for the stock item
            name: Name/description of the stock item
            quantity: Initial quantity (default: 0)
            price: Price per unit (default: 0.0)
            
        Returns:
            The created Stock object
            
        Raises:
            ValueError: If item_id already exists or invalid values provided
        """
        if item_id in self._inventory:
            raise ValueError(f"Stock item with ID '{item_id}' already exists")
        
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        
        if price < 0:
            raise ValueError("Price cannot be negative")
        
        stock_item = Stock(item_id, name, quantity, price)
        self._inventory[item_id] = stock_item
        return stock_item
    
    def remove_stock_item(self, item_id: str) -> bool:
        """
        Remove a stock item from the inventory.
        
        Args:
            item_id: ID of the stock item to remove
            
        Returns:
            True if item was removed, False if item not found
        """
        if item_id in self._inventory:
            del self._inventory[item_id]
            return True
        return False
    
    def get_stock_item(self, item_id: str) -> Optional[Stock]:
        """
        Get a stock item by ID.
        
        Args:
            item_id: ID of the stock item to retrieve
            
        Returns:
            Stock object if found, None otherwise
        """
        return self._inventory.get(item_id)
    
    def update_stock_quantity(self, item_id: str, quantity: int) -> bool:
        """
        Update the quantity of a stock item.
        
        Args:
            item_id: ID of the stock item to update
            quantity: New quantity value
            
        Returns:
            True if updated successfully, False if item not found
            
        Raises:
            ValueError: If quantity is negative
        """
        stock_item = self.get_stock_item(item_id)
        if stock_item:
            stock_item.update_quantity(quantity)
            return True
        return False
    
    def add_to_stock(self, item_id: str, quantity: int) -> bool:
        """
        Add quantity to existing stock.
        
        Args:
            item_id: ID of the stock item
            quantity: Quantity to add
            
        Returns:
            True if updated successfully, False if item not found
            
        Raises:
            ValueError: If quantity is negative
        """
        if quantity < 0:
            raise ValueError("Quantity to add cannot be negative")
        
        stock_item = self.get_stock_item(item_id)
        if stock_item:
            stock_item.update_quantity(stock_item.quantity + quantity)
            return True
        return False
    
    def remove_from_stock(self, item_id: str, quantity: int) -> bool:
        """
        Remove quantity from existing stock.
        
        Args:
            item_id: ID of the stock item
            quantity: Quantity to remove
            
        Returns:
            True if updated successfully, False if item not found or insufficient stock
            
        Raises:
            ValueError: If quantity is negative or exceeds available stock
        """
        if quantity < 0:
            raise ValueError("Quantity to remove cannot be negative")
        
        stock_item = self.get_stock_item(item_id)
        if stock_item:
            if stock_item.quantity < quantity:
                raise ValueError(f"Insufficient stock. Available: {stock_item.quantity}, Requested: {quantity}")
            stock_item.update_quantity(stock_item.quantity - quantity)
            return True
        return False
    
    def is_in_stock(self, item_id: str, required_quantity: int = 1) -> bool:
        """
        Check if an item is in stock with required quantity.
        
        Args:
            item_id: ID of the stock item to check
            required_quantity: Minimum quantity required (default: 1)
            
        Returns:
            True if item has sufficient stock, False otherwise
        """
        stock_item = self.get_stock_item(item_id)
        return stock_item is not None and stock_item.quantity >= required_quantity
    
    def get_all_stock_items(self) -> List[Stock]:
        """
        Get all stock items in the inventory.
        
        Returns:
            List of all Stock objects
        """
        return list(self._inventory.values())
    
    def get_low_stock_items(self, threshold: int = 5) -> List[Stock]:
        """
        Get stock items with quantity below threshold.
        
        Args:
            threshold: Minimum quantity threshold (default: 5)
            
        Returns:
            List of Stock objects with low stock
        """
        return [stock for stock in self._inventory.values() if stock.quantity < threshold]
    
    def get_stock_report(self) -> Dict:
        """
        Generate a comprehensive stock report.
        
        Returns:
            Dictionary containing stock statistics and information
        """
        all_items = self.get_all_stock_items()
        total_items = len(all_items)
        total_quantity = sum(item.quantity for item in all_items)
        total_value = sum(item.quantity * item.price for item in all_items)
        out_of_stock = [item for item in all_items if item.quantity == 0]
        low_stock = self.get_low_stock_items()
        
        return {
            'total_items': total_items,
            'total_quantity': total_quantity,
            'total_value': round(total_value, 2),
            'out_of_stock_count': len(out_of_stock),
            'low_stock_count': len(low_stock),
            'out_of_stock_items': [item.item_id for item in out_of_stock],
            'low_stock_items': [item.item_id for item in low_stock]
        }
    
    def clear_inventory(self) -> None:
        """Clear all items from the inventory."""
        self._inventory.clear()


# Example usage and testing functions
def main():
    """Example usage of the stock management system."""
    # Create a stock manager
    manager = StockManager()
    
    # Add some stock items
    manager.add_stock_item("001", "Widget A", 100, 10.50)
    manager.add_stock_item("002", "Widget B", 50, 25.00)
    manager.add_stock_item("003", "Widget C", 2, 15.75)
    
    # Display initial stock
    print("Initial Stock Report:")
    report = manager.get_stock_report()
    print(f"Total items: {report['total_items']}")
    print(f"Total value: ${report['total_value']}")
    print(f"Low stock items: {report['low_stock_items']}")
    
    # Test stock operations
    print("\nTesting stock operations:")
    print(f"Widget A in stock (qty 10): {manager.is_in_stock('001', 10)}")
    
    # Remove some stock
    manager.remove_from_stock("001", 30)
    print(f"After removing 30 Widget A: {manager.get_stock_item('001')}")
    
    # Add stock
    manager.add_to_stock("002", 25)
    print(f"After adding 25 Widget B: {manager.get_stock_item('002')}")
    
    print("\nFinal Stock Report:")
    final_report = manager.get_stock_report()
    for key, value in final_report.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
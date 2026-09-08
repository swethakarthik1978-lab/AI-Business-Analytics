import pandas as pd


def analyze_inventory(inventory, products):

    # Copy data
    inventory = inventory.copy()
    products = products.copy()

    # Merge inventory with product information
    inventory_analysis = inventory.merge( products, on="ProductID", how="left" )

    # Calculate inventory value
    inventory_analysis["InventoryValue"] = (
        inventory_analysis["StockQuantity"]
        * inventory_analysis["UnitPrice]"] 
    )

    def get_stock_status(quantity):
        if quantity==0:
            return "Out of Stock"
        elif quantity <= 10:
            return "Low Stock"
        elif quantity <= 50:
            return " Medium Stock"
        else: 
            return "High Stock"
    inventory_analysis["StockStatus"] = ( 
        inventory_analysis["StockQuantity"]
        .apply(get_stock_status)
    )

    return inventory_analysis
        

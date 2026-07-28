from sqlalchemy.orm import Session
from database.models import Product, Customer, Order, Inventory, Finance
def add_product(db: Session, product: Product):
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_products(db: Session):
    return db.query(Product).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.ProductID == product_id).first()

def update_product_stock(db: Session, product_id: int, stock: int):
    product = get_product_by_id(db, product_id)
    if product:
        product.Stock = stock
        db.commit()
        db.refresh(product)
    return product

def delete_product(db: Session, product_id: int):
    product = get_product_by_id(db, product_id)
    if product:
        db.delete(product)
        db.commit()
    return product


def add_customer(db: Session, customer: Customer):
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

def get_customers(db: Session):
    return db.query(Customer).all()

def get_customer_by_id(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.CustomerID == customer_id).first()

def delete_customer(db: Session, customer_id: int):
    customer= get_customer_by_id(db, customer_id)
    if customer:
        db.delete(customer)
        db.commit()
    return customer


def add_order(db: Session, order: Order):
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def get_orders(db: Session):
    return db.query(Order).all()

def get_order_by_id(db: Session, order_id: int):
    return db.query(Order).filter(Order.OrderID == order_id).first()

def delete_order(db: Session, order_id: int):
    order= get_order_by_id(db, order_id)
    if order:
        db.delete(order)
        db.commit()
    return order


def add_inventory(db: Session, inventory: Inventory):
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    return inventory

def get_inventory(db: Session):
    return db.query(inventory).all()

def update_inventory(db: Session, inventory_id:int, current_stock:int):
    inventory = db.query(Inventory).filter(Inventory.InventoryID == inventory_id).first()
    if inventory:
        inventory.CurrentStock = current_stock
        db.commit()
        db.refresh(inventory)

    return inventory

def add_finance(db: Session, finance: Finance):
    db.add(finance)
    db.commit()
    db.refresh(finance)
    return finance 

def get_finance_records(db: Session):
    return db.query(Finance).all()

def get_finance_by_id(db: Session, finance_id: int):
    return db.query(Finance).filter(Finance.FinanceID == finance_id).first()

def delete_finance(db: Session, finance_id: int):
    customer= get_finance_by_id(db, finance_id)
    if finance:
        db.delete(finance)
        db.commit()
    return finance
from sqlalchemy.orm import Session

from .models import Product, Customer, Order, Inventory, Finance


# =========================================================
# PRODUCT CRUD
# =========================================================

def add_product(db: Session, product: Product):
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_products(db: Session):
    return db.query(Product).all()


def get_product_by_id(db: Session, product_id: int):
    return (
        db.query(Product)
        .filter(Product.ProductID == product_id)
        .first()
    )


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


# =========================================================
# CUSTOMER CRUD
# =========================================================

def add_customer(db: Session, customer: Customer):
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def get_customers(db: Session):
    return db.query(Customer).all()


def get_customer_by_id(db: Session, customer_id: int):
    return (
        db.query(Customer)
        .filter(Customer.CustomerID == customer_id)
        .first()
    )


def delete_customer(db: Session, customer_id: int):
    customer = get_customer_by_id(db, customer_id)

    if customer:
        db.delete(customer)
        db.commit()

    return customer


# =========================================================
# ORDER CRUD
# =========================================================

def add_order(db: Session, order: Order):
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def get_orders(db: Session):
    return db.query(Order).all()


def get_order_by_id(db: Session, order_id: int):
    return (
        db.query(Order)
        .filter(Order.OrderID == order_id)
        .first()
    )


def delete_order(db: Session, order_id: int):
    order = get_order_by_id(db, order_id)

    if order:
        db.delete(order)
        db.commit()

    return order


# =========================================================
# INVENTORY CRUD
# =========================================================

def get_inventory(db: Session):
    return db.query(Inventory).all()


def update_inventory(
    db: Session,
    inventory_id: int,
    current_stock: int
):
    inventory = (
        db.query(Inventory)
        .filter(Inventory.InventoryID == inventory_id)
        .first()
    )

    if inventory:
        inventory.CurrentStock = current_stock
        db.commit()
        db.refresh(inventory)

    return inventory


# =========================================================
# FINANCE CRUD
# =========================================================

def get_finance_records(db: Session):
    return db.query(Finance).all()


def get_finance_by_id(db: Session, finance_id: int):
    return (
        db.query(Finance)
        .filter(Finance.FinanceID == finance_id)
        .first()
    )


def delete_finance(db: Session, finance_id: int):
    finance = get_finance_by_id(db, finance_id)

    if finance:
        db.delete(finance)
        db.commit()

    return finance


# =========================================================
# BULK DATAFRAME IMPORT FUNCTIONS
# =========================================================

def add_customers(db: Session, df):

    for _, row in df.iterrows():

        customer = Customer(
            CustomerID=int(row["CustomerID"]),
            CustomerName=str(row["CustomerName"]),
            Email=str(row["Email"]),
            Phone=str(row["Phone"]),
            City=str(row["City"])
        )

        db.merge(customer)

    db.commit()


def add_products(db: Session, df):

    for _, row in df.iterrows():

        product = Product(
            ProductID=int(row["ProductID"]),
            ProductName=str(row["ProductName"]),
            Category=str(row["Category"]),
            Price=float(row["Price"]),
            Stock=int(row["Stock"])
        )

        db.merge(product)

    db.commit()


def add_inventory(db: Session, df):

    for _, row in df.iterrows():

        inventory = Inventory(
            InventoryID=int(row["InventoryID"]),
            ProductID=int(row["ProductID"]),
            CurrentStock=int(row["CurrentStock"]),
            ReorderLevel=int(row["ReorderLevel"])
        )

        db.merge(inventory)

    db.commit()


def add_finance(db: Session, df):

    for _, row in df.iterrows():

        finance = Finance(
            FinanceID=int(row["FinanceID"]),
            Revenue=float(row["Revenue"]),
            Expenses=float(row["Expenses"]),
            Profit=float(row["Profit"])
        )

        db.merge(finance)

    db.commit()
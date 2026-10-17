import pandas as pd


def personalized_recommendations(
    sales,
    products,
    customer_id,
    n=5
):

    """
    Recommend products based on a customer's
    previous purchases.
    """

    sales = sales.copy()
    products = products.copy()

    # ==================================================
    # CUSTOMER PURCHASE HISTORY
    # ==================================================

    customer_sales = sales[
        sales[
            "CustomerID"
        ]
        == customer_id
    ]

    if customer_sales.empty:

        return pd.DataFrame()

    # ==================================================
    # PRODUCTS ALREADY PURCHASED
    # ==================================================

    purchased_products = (
        customer_sales[
            "ProductID"
        ]
        .dropna()
        .unique()
    )

    # ==================================================
    # CATEGORIES CUSTOMER PURCHASED
    # ==================================================

    purchased_categories = (
        products[
            products[
                "ProductID"
            ].isin(
                purchased_products
            )
        ][
            "Category"
        ]
        .dropna()
        .unique()
    )

    # ==================================================
    # RECOMMENDED PRODUCTS
    # ==================================================

    recommendations = products[
        (
            products[
                "Category"
            ].isin(
                purchased_categories
            )
        )
        &
        (
            ~products[
                "ProductID"
            ].isin(
                purchased_products
            )
        )
    ].copy()

    # ==================================================
    # REMOVE DUPLICATES
    # ==================================================

    recommendations = (
        recommendations
        .drop_duplicates(
            subset="ProductID"
        )
    )

    # ==================================================
    # RETURN RESULTS
    # ==================================================

    return (
        recommendations
        .head(n)
    )
import pandas as pd


def frequently_bought_together(
    sales,
    product_id,
    n=5
):

    """
    Find products purchased in the same
    orders as the selected product.
    """

    sales = sales.copy()

    # ==================================================
    # ORDERS CONTAINING SELECTED PRODUCT
    # ==================================================

    selected_orders = (
        sales[
            sales[
                "ProductID"
            ]
            == product_id
        ][
            "OrderID"
        ]
        .unique()
    )

    if (
        len(
            selected_orders
        )
        == 0
    ):

        return pd.DataFrame(
            columns=[
                "ProductID",
                "Frequency"
            ]
        )

    # ==================================================
    # RELATED SALES
    # ==================================================

    related_sales = sales[
        sales[
            "OrderID"
        ].isin(
            selected_orders
        )
    ]

    # ==================================================
    # REMOVE ORIGINAL PRODUCT
    # ==================================================

    related_products = related_sales[
        related_sales[
            "ProductID"
        ]
        != product_id
    ]

    if related_products.empty:

        return pd.DataFrame(
            columns=[
                "ProductID",
                "Frequency"
            ]
        )

    # ==================================================
    # COUNT OCCURRENCES
    # ==================================================

    recommendations = (
        related_products
        .groupby(
            "ProductID"
        )
        .size()
        .reset_index(
            name="Frequency"
        )
        .sort_values(
            "Frequency",
            ascending=False
        )
        .head(n)
    )

    return recommendations
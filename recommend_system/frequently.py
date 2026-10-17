# ==================================================
# IMPORTS
# ==================================================

import pandas as pd


# ==================================================
# FREQUENTLY BOUGHT TOGETHER
# ==================================================

def frequently_bought_together(
    sales,
    product_id,
    n=5
):

    """
    Find products that are frequently purchased
    in the same orders as the selected product.

    Parameters
    ----------
    sales : pandas.DataFrame
        Sales transaction data.

    product_id : int
        Product selected by the user.

    n : int
        Maximum number of recommendations.

    Returns
    -------
    pandas.DataFrame
        ProductID and Frequency.
    """

    sales = sales.copy()

    # ==================================================
    # VALIDATE COLUMNS
    # ==================================================

    required_columns = {
        "OrderID",
        "ProductID"
    }

    missing_columns = (
        required_columns
        - set(
            sales.columns
        )
    )

    if missing_columns:

        raise ValueError(
            "Missing required sales columns: "
            + ", ".join(
                sorted(
                    missing_columns
                )
            )
        )

    # ==================================================
    # REMOVE DUPLICATES
    # ==================================================

    # Each product should only count once
    # inside the same order.

    order_products = (
        sales[
            [
                "OrderID",
                "ProductID"
            ]
        ]
        .drop_duplicates()
    )

    # ==================================================
    # FIND ORDERS CONTAINING SELECTED PRODUCT
    # ==================================================

    selected_orders = (
        order_products[
            order_products[
                "ProductID"
            ]
            == product_id
        ][
            "OrderID"
        ]
        .unique()
    )

    # Product was never purchased.

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
    # GET OTHER PRODUCTS FROM SAME ORDERS
    # ==================================================

    related_products = (
        order_products[
            order_products[
                "OrderID"
            ]
            .isin(
                selected_orders
            )
        ]
    )

    # ==================================================
    # REMOVE ORIGINAL PRODUCT
    # ==================================================

    related_products = (
        related_products[
            related_products[
                "ProductID"
            ]
            != product_id
        ]
    )

    if (
        related_products.empty
    ):

        return pd.DataFrame(
            columns=[
                "ProductID",
                "Frequency"
            ]
        )

    # ==================================================
    # COUNT CO-PURCHASE FREQUENCY
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
            [
                "Frequency",
                "ProductID"
            ],
            ascending=[
                False,
                True
            ]
        )
        .head(
            n
        )
        .reset_index(
            drop=True
        )
    )

    # ==================================================
    # RETURN RESULTS
    # ==================================================

    return recommendations
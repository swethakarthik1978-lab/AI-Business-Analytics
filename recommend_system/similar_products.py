import pandas as pd


def recommend_similar_products(
    products,
    product_id,
    n=5
):

    """
    Recommend products from the same category
    as the selected product.
    """

    products = products.copy()

    # ==================================================
    # FIND SELECTED PRODUCT
    # ==================================================

    selected_product = products[
        products[
            "ProductID"
        ]
        == product_id
    ]

    if selected_product.empty:

        return pd.DataFrame()

    # ==================================================
    # GET CATEGORY
    # ==================================================

    category = (
        selected_product
        .iloc[0][
            "Category"
        ]
    )

    # ==================================================
    # FIND SIMILAR PRODUCTS
    # ==================================================

    recommendations = products[
        (
            products[
                "Category"
            ]
            == category
        )
        &
        (
            products[
                "ProductID"
            ]
            != product_id
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
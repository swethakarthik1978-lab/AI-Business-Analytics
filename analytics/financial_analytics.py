
import pandas as pd

def analyze_financial(finance, sales):
    finance = finance.copy()
    sales = sales.copy()

    revenue = sales["TotalAmount"].sum()
    expenses = finance["Expenses"].sum()
    profit = revenue - expenses

    if revenue != 0:
        gross_margin = (profit / revenue) * 100
    else:
        gross_margin = 0

    net_profit = profit

    if revenue != 0:
        net_margin = (net_profit / revenue) * 100
    else:
        net_margin = 0

    # ==================================================
    # FINANCIAL SUMMARY
    # ==================================================

    financial_summary = pd.DataFrame({
        "Metric": [
            "Revenue",
            "Expenses",
            "Profit",
            "Gross Margin",
            "Net Margin"
        ],
        "Value": [
            revenue,
            expenses,
            profit,
            gross_margin,
            net_margin
        ]
    })

    # ==================================================
    # RETURN RESULTS
    # ==================================================

    return {
        "revenue": revenue,
        "expenses": expenses,
        "profit": profit,
        "gross_margin": gross_margin,
        "net_margin": net_margin,
        "financial_summary": financial_summary
    }
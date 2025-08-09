import pandas as pd
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "Sample Portfolio Dataset for Assignment.xlsx"

def load_holdings():
    df = pd.read_excel(DATA_FILE, sheet_name="Holdings")
    df = df.rename(columns={
        "Symbol": "symbol",
        "Company Name": "name",
        "Quantity": "quantity",
        "Avg Price ₹": "avgPrice",
        "Current Price (₹)": "currentPrice",
        "Sector": "sector",
        "Market Cap": "marketCap",
        "Value ₹": "value",
        "Gain/Loss (₹)": "gainLoss",
        "Gain/Loss %": "gainLossPercent"
    })

    # numeric_cols = ["avgPrice", "currentPrice", "value", "gainLoss", "gainLossPercent"]
    # df[numeric_cols] = df[numeric_cols].round(2)

    return df.to_dict(orient="records")
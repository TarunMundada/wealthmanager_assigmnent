import pandas as pd
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "Sample Portfolio Dataset for Assignment.xlsx"

def load_holdings(): #function to load portfolio holdings
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
    
    return df.to_dict(orient="records")


def load_allocation(): #function to load allocations
    sector_df = pd.read_excel(DATA_FILE, sheet_name="Sector_Allocation")
    sector_df = sector_df.rename(columns={
        "Sector": "sector",
        "Value (₹)": "value",
        "Percentage": "percentage"
    })

    by_sector = {
        row["sector"]: {
            "value": float(str(row["value"]).replace(",", "")),
            "percentage": float(str(row["percentage"]).replace("%", ""))
        }
        for _, row in sector_df.iterrows()
    }

    market_df = pd.read_excel(DATA_FILE, sheet_name="Market_Cap")
    market_df = market_df.rename(columns={
        "Market Cap": "marketCap",
        "Value (₹)": "value",
        "Percentage": "percentage"
    })

    by_market_cap = {
        row["marketCap"]: {
            "value": float(str(row["value"]).replace(",", "")),
            "percentage": float(str(row["percentage"]).replace("%", ""))
        }
        for _, row in market_df.iterrows()
    }

    return {
        "bySector": by_sector,
        "byMarketCap": by_market_cap
    }
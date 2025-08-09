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
    
def load_performance(): #function to load performance data
    df = pd.read_excel(DATA_FILE, sheet_name="Historical_Performance")
    df = df.rename(columns={
        "Date": "date",
        "Portfolio Value (₹)": "portfolio",
        "Nifty 50": "nifty50",
        "Gold (₹/10g)": "gold",
        "Portfolio Return %": "portfolioReturn",
        "Nifty 50 Return %": "nifty50Return",
        "Gold Return %": "goldReturn"
    })

    timeline = [
        {
            "date": row["date"].strftime("%Y-%m-%d"),
            "portfolio": int(row["portfolio"]),
            "nifty50": int(row["nifty50"]),
            "gold": int(row["gold"])
        }
        for _, row in df.iterrows()
    ]

    n = len(df)
    if n == 0:
        return {"timeline": [], "returns": {}}

    def compute_return(col, months_ago):
        last = df[col].iloc[-1]
        past_idx = max(0, n - 1 - months_ago)
        past = df[col].iloc[past_idx]
        if pd.isna(last) or pd.isna(past) or past == 0:
            return None
        return round((last - past) / past, 4)

    returns = {
        "portfolio": {
            "1month": compute_return('portfolio', 1),
            "3months": compute_return('portfolio', 3),
            "1year": compute_return('portfolio', n-1)
        },
        "nifty50": {
            "1month": compute_return('nifty50', 1),
            "3months": compute_return('nifty50', 3),
            "1year": compute_return('nifty50', n-1)
        },
        "gold": {
            "1month": compute_return('gold', 1),
            "3months": compute_return('gold', 3),
            "1year": compute_return('gold', n-1)
        }
    }

    return {"timeline": timeline, "returns": returns}

def load_summary():
    # Load Top Performers sheet
    top_perf_df = pd.read_excel(DATA_FILE, sheet_name="Top_Performers")
    summary_df = pd.read_excel(DATA_FILE, sheet_name="Summary")

    # Extract summary metrics
    total_value = float(str(summary_df.loc[summary_df["Metric"] == "Total Portfolio Value", "Value"].values[0]).replace(",", ""))
    total_invested = float(str(summary_df.loc[summary_df["Metric"] == "Total Invested Amount", "Value"].values[0]).replace(",", ""))
    total_gain_loss = float(str(summary_df.loc[summary_df["Metric"] == "Total Gain/Loss", "Value"].values[0]).replace(",", ""))
    total_gain_loss_percent = float(str(summary_df.loc[summary_df["Metric"] == "Total Gain/Loss (%)", "Value"].values[0]).replace("%", ""))

    diversification_score = float(str(summary_df.loc[summary_df["Metric"] == "Diversification Score", "Value"].values[0]))
    risk_level = summary_df.loc[summary_df["Metric"] == "Risk Level", "Value"].values[0]

    # Extract performers
    top_performer_row = top_perf_df.loc[top_perf_df["Metric"] == "Best Performer"].iloc[0]
    worst_performer_row = top_perf_df.loc[top_perf_df["Metric"] == "Worst Performer"].iloc[0]

    top_performer = {
        "symbol": top_performer_row["Symbol"],
        "name": top_performer_row["Company Name"],
        "gainPercent": float(str(top_performer_row["Performance"]).replace("%", ""))
    }

    worst_performer = {
        "symbol": worst_performer_row["Symbol"],
        "name": worst_performer_row["Company Name"],
        "gainPercent": float(str(worst_performer_row["Performance"]).replace("%", ""))
    }

    return {
        "totalValue": total_value,
        "totalInvested": total_invested,
        "totalGainLoss": total_gain_loss,
        "totalGainLossPercent": total_gain_loss_percent,
        "topPerformer": top_performer,
        "worstPerformer": worst_performer,
        "diversificationScore": diversification_score,
        "riskLevel": risk_level
    }


import pandas as pd
import yfinance as yf

# ==============================================================================
# 1. DATA LOADING & ROBUST COLUMN DETECTOR
# ==============================================================================
df_cash = pd.read_csv("cash_flows.csv", encoding="utf-8-sig")
df_trades = pd.read_csv("trades.csv", encoding="utf-8-sig")

# Strip whitespace and convert column headers to lowercase
df_cash.columns = df_cash.columns.str.strip().str.lower()
df_trades.columns = df_trades.columns.str.strip().str.lower()


# Dynamic column detection function
def get_col_name(df, possible_names):
    for name in possible_names:
        for col in df.columns:
            if name in col:
                return col
    return None


# Map trade column names automatically
col_date = get_col_name(df_trades, ["date"])
col_ticker = get_col_name(df_trades, ["ticker", "etf", "symbol"])
col_shares = get_col_name(df_trades, ["shares", "qty", "quantity"])
col_cost = get_col_name(
    df_trades, ["cost_eur", "cost", "total_eur", "total eur", "total"]
)

df_trades = df_trades.rename(
    columns={
        col_date: "date",
        col_ticker: "etf",
        col_shares: "shares",
        col_cost: "cost_eur",
    }
)

# Parse dates
df_cash["date"] = pd.to_datetime(df_cash["date"])
df_trades["date"] = pd.to_datetime(df_trades["date"], format="mixed")

# Ensure numeric types
df_cash["amount_eur"] = pd.to_numeric(df_cash["amount_eur"], errors="coerce")
df_trades["shares"] = pd.to_numeric(df_trades["shares"], errors="coerce")
df_trades["cost_eur"] = pd.to_numeric(df_trades["cost_eur"], errors="coerce")

# Map tickers to yfinance symbols
TICKER_MAP = {"VWRA": "VWRA.L", "VWCE": "VWCE.DE", "VAGF": "VAGF.DE"}


# ==============================================================================
# 2. DYNAMIC PORTFOLIO EVALUATION FUNCTION
# ==============================================================================
def get_portfolio_value_on_date(eval_date, df_cash_until, df_trades_until):
    """Calculates total portfolio value (Holdings Value + Unspent Cash) on eval_date."""
    trades_sub = df_trades_until[df_trades_until["date"] <= eval_date]
    cash_sub = df_cash_until[df_cash_until["date"] <= eval_date]

    total_deposited = cash_sub["amount_eur"].sum()

    if trades_sub.empty:
        return total_deposited

    holdings = trades_sub.groupby("etf")["shares"].sum().to_dict()
    spent_eur = trades_sub["cost_eur"].sum()
    unspent_cash = total_deposited - spent_eur

    market_value = 0.0
    for etf, shares in holdings.items():
        if shares > 0 and etf in TICKER_MAP:
            yf_symbol = TICKER_MAP[etf]
            hist = yf.Ticker(yf_symbol).history(
                start=eval_date - pd.Timedelta(days=5),
                end=eval_date + pd.Timedelta(days=1),
            )
            if not hist.empty:
                last_price = hist["Close"].iloc[-1]
                if etf == "VWRA":
                    last_price *= 0.92  # USD to EUR conversion
                market_value += shares * last_price

    return market_value + unspent_cash


# ==============================================================================
# 3. HISTORICAL TWR CALCULATION LOOP
# ==============================================================================
twr_rows = []
cum_twr = 0.0
prev_post_val = 0.0

for idx, row in df_cash.iterrows():
    date_dt = row["date"]
    date_str = date_dt.strftime("%Y-%m-%d")
    deposit_eur = float(row["amount_eur"])

    if idx == 0:
        pre_val = 0.0
        sub_ret = 0.0
        post_val = deposit_eur
        cum_twr = 0.0
    else:
        pre_val = get_portfolio_value_on_date(
            date_dt, df_cash.iloc[:idx], df_trades
        )
        sub_ret = (pre_val / prev_post_val) - 1.0 if prev_post_val > 0 else 0.0
        cum_twr = ((1.0 + cum_twr) * (1.0 + sub_ret)) - 1.0
        post_val = pre_val + deposit_eur

    prev_post_val = post_val

    twr_rows.append(
        {
            "Date": date_str,
            "Deposit (€)": f"€{deposit_eur:,.2f}",
            "Pre-Val (€)": f"€{pre_val:,.2f}",
            "Post-Val (€)": f"€{post_val:,.2f}",
            "Period Return": f"{sub_ret:+.2%}",
            "Cumulative TWR": f"{cum_twr:+.2%}",
        }
    )

df_twr_output = pd.DataFrame(twr_rows)

# ==============================================================================
# 4. LIVE PORTFOLIO & CASH VALUATION
# ==============================================================================
total_deposited = df_cash["amount_eur"].sum()
total_spent = df_trades["cost_eur"].sum()
unspent_cash = total_deposited - total_spent

holdings_summary = (
    df_trades.groupby("etf")
    .agg(shares=("shares", "sum"), cost_eur=("cost_eur", "sum"))
    .reset_index()
)

live_rows = []
total_market_value = 0.0

for _, row in holdings_summary.iterrows():
    etf = row["etf"]
    shares = row["shares"]
    cost = row["cost_eur"]

    # Fetch live price
    yf_symbol = TICKER_MAP.get(etf, etf)
    ticker_obj = yf.Ticker(yf_symbol)
    live_price = ticker_obj.fast_info.last_price

    if etf == "VWRA":
        live_price *= 0.92  # USD to EUR estimate

    mkt_val = shares * live_price
    total_market_value += mkt_val
    pnl = mkt_val - cost
    pnl_pct = (pnl / cost) * 100 if cost > 0 else 0.0

    live_rows.append(
        {
            "ETF": etf,
            "Shares": f"{shares:,.2f}",
            "Cost (€)": f"€{cost:,.2f}",
            "Price (€)": f"€{live_price:,.2f}",
            "Value (€)": f"€{mkt_val:,.2f}",
            "P&L (€)": f"€{pnl:+,.2f}",
            "Return (%)": f"{pnl_pct:+.2f}%",
        }
    )

df_live_output = pd.DataFrame(live_rows)
total_portfolio_value = total_market_value + unspent_cash
total_pnl = total_portfolio_value - total_deposited
total_pnl_pct = (
    (total_pnl / total_deposited) * 100 if total_deposited > 0 else 0.0
)

# ==============================================================================
# 5. TERMINAL OUTPUTS
# ==============================================================================
print("======================================================================")
print("                        HISTORICAL DEPOSITS TWR                       ")
print("======================================================================")
print(df_twr_output.to_string(index=False))

print("\n======================================================================")
print("                 LIVE PORTFOLIO & CASH VALUATION                      ")
print("======================================================================")
print(df_live_output.to_string(index=False))
print("----------------------------------------------------------------------")
print(f"Unspent Cash Balance  : €{unspent_cash:,.2f}")
print(f"Total Invested In ETFs : €{total_market_value:,.2f}")
print(f"Total Portfolio Value  : €{total_portfolio_value:,.2f}")
print(f"Total Cash Deposited   : €{total_deposited:,.2f}")
print(f"Overall Profit/Loss    : €{total_pnl:+,.2f} ({total_pnl_pct:+.2f}%)")
print("======================================================================")
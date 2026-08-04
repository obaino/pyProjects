import pandas as pd
import yfinance as yf

# ==============================================================================
# 1. DATA LOADING & PREPARATION
# ==============================================================================
df_cash = pd.read_csv("cash_flows.csv", encoding="utf-8-sig")
df_trades = pd.read_csv("trades.csv", encoding="utf-8-sig")

# Normalize column headers
df_cash.columns = df_cash.columns.str.strip().str.lower()
df_trades.columns = df_trades.columns.str.strip().str.lower()

# Map potential column name variations automatically
df_trades = df_trades.rename(
    columns={
        "ticker": "etf",
        "symbol": "etf",
        "qty": "shares",
        "quantity": "shares",
        "cost": "cost_eur",
        "total_eur": "cost_eur",
        "total eur": "cost_eur",
    }
)

df_cash["date"] = pd.to_datetime(df_cash["date"])
df_trades["date"] = pd.to_datetime(df_trades["date"], format="mixed")

df_cash["amount_eur"] = pd.to_numeric(df_cash["amount_eur"], errors="coerce")
df_trades["shares"] = pd.to_numeric(df_trades["shares"], errors="coerce")
df_trades["cost_eur"] = pd.to_numeric(df_trades["cost_eur"], errors="coerce")

TICKER_MAP = {"VWRA": "VWRA.L", "VWCE": "VWCE.DE", "VAGF": "VAGF.DE"}

# Cache FX rates to avoid repeated API network calls
fx_cache = {}


def get_usd_eur_rate(eval_date):
    """Fetches the historical USD to EUR conversion rate on or just before eval_date."""
    date_str = eval_date.strftime("%Y-%m-%d")
    if date_str in fx_cache:
        return fx_cache[date_str]

    fx = yf.Ticker("EURUSD=X").history(
        start=eval_date - pd.Timedelta(days=5),
        end=eval_date + pd.Timedelta(days=1),
    )
    if not fx.empty:
        rate = 1.0 / fx["Close"].iloc[-1]
    else:
        rate = 0.92

    fx_cache[date_str] = rate
    return rate


# ==============================================================================
# 2. DYNAMIC PORTFOLIO EVALUATION FUNCTION
# ==============================================================================
def get_portfolio_value_on_date(eval_date, df_cash_until, df_trades_until):
    """Calculates total portfolio market value (ETF holdings + Unspent Cash) in EUR on eval_date."""
    trades_sub = df_trades_until[df_trades_until["date"] <= eval_date]
    cash_sub = df_cash_until[df_cash_until["date"] <= eval_date]

    total_deposited = cash_sub["amount_eur"].sum()

    if trades_sub.empty:
        return total_deposited

    holdings = trades_sub.groupby("etf")["shares"].sum().to_dict()
    spent_eur = trades_sub["cost_eur"].sum()
    unspent_cash = total_deposited - spent_eur

    usd_eur_rate = get_usd_eur_rate(eval_date)
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
                    last_price *= usd_eur_rate
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
# 4. LIVE PORTFOLIO, CASH VALUATION & LIVE TWR
# ==============================================================================
total_deposited = df_cash["amount_eur"].sum()
total_spent = df_trades["cost_eur"].sum()
unspent_cash = total_deposited - total_spent

holdings_summary = (
    df_trades.groupby("etf")
    .agg(shares=("shares", "sum"), cost_eur=("cost_eur", "sum"))
    .reset_index()
)

# Fetch current live USD to EUR rate dynamically
fx_live = yf.Ticker("EURUSD=X").fast_info.last_price
live_usd_eur_rate = 1.0 / fx_live if fx_live else 0.92

live_rows = []
total_market_value = 0.0

for _, row in holdings_summary.iterrows():
    etf = row["etf"]
    shares = row["shares"]
    cost = row["cost_eur"]

    yf_symbol = TICKER_MAP.get(etf, etf)
    live_price = yf.Ticker(yf_symbol).fast_info.last_price

    if etf == "VWRA":
        live_price *= live_usd_eur_rate

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

# --- Compute Live TWR since the last deposit ---
last_post_val = prev_post_val  # Post-Val from the last deposit date
last_cum_twr = cum_twr        # TWR reached at the last deposit date

sub_period_return_live = (
    (total_portfolio_value / last_post_val) - 1.0 if last_post_val > 0 else 0.0
)
live_twr = ((1.0 + last_cum_twr) * (1.0 + sub_period_return_live)) - 1.0

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
print(f"Live Portfolio TWR     : {live_twr:+.2%}")
print("======================================================================")
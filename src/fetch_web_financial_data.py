import os
from datetime import datetime

import numpy as np
import pandas as pd
import yfinance as yf


RAW_DIR = "data/raw"
os.makedirs(RAW_DIR, exist_ok=True)


TICKERS = {
    "RELIANCE.NS": "Energy / Conglomerate",
    "HDFCBANK.NS": "Banking",
    "ICICIBANK.NS": "Banking",
    "SBIN.NS": "Banking",
    "INFY.NS": "Information Technology",
    "TCS.NS": "Information Technology",
    "ITC.NS": "FMCG",
    "HINDUNILVR.NS": "FMCG",
    "MARUTI.NS": "Automobile",
    "TATAMOTORS.NS": "Automobile"
}


INDEX_TICKERS = {
    "^NSEI": "NIFTY 50",
    "^BSESN": "BSE Sensex"
}


def safe_download(ticker, period="1y"):
    try:
        df = yf.download(
            ticker,
            period=period,
            interval="1d",
            progress=False,
            auto_adjust=True
        )

        if df.empty:
            return None

        df = df.dropna()
        return df

    except Exception as e:
        print(f"Error downloading {ticker}: {e}")
        return None


def calculate_metrics(df):
    """
    Calculates return and volatility metrics from downloaded yfinance data.
    This function handles both normal columns and MultiIndex columns.
    """

    # Handle MultiIndex columns returned by newer yfinance versions
    if isinstance(df.columns, pd.MultiIndex):
        if "Close" in df.columns.get_level_values(0):
            close = df["Close"]
            if isinstance(close, pd.DataFrame):
                close = close.iloc[:, 0]
        elif "Adj Close" in df.columns.get_level_values(0):
            close = df["Adj Close"]
            if isinstance(close, pd.DataFrame):
                close = close.iloc[:, 0]
        else:
            raise ValueError("No Close or Adj Close column found in MultiIndex dataframe.")
    else:
        if "Close" in df.columns:
            close = df["Close"]
        elif "Adj Close" in df.columns:
            close = df["Adj Close"]
        else:
            raise ValueError("No Close or Adj Close column found in dataframe.")

    close = close.dropna()

    if close.empty:
        raise ValueError("Close price series is empty.")

    start_price = float(close.iloc[0])
    end_price = float(close.iloc[-1])

    total_return = ((end_price - start_price) / start_price) * 100

    daily_returns = close.pct_change().dropna()

    if daily_returns.empty:
        volatility = 0.0
    else:
        volatility = float(daily_returns.std() * np.sqrt(252) * 100)

    max_price = float(close.max())
    min_price = float(close.min())

    return {
        "start_price": round(start_price, 2),
        "end_price": round(end_price, 2),
        "total_return": round(total_return, 2),
        "annualized_volatility": round(volatility, 2),
        "max_price": round(max_price, 2),
        "min_price": round(min_price, 2)
    }


def get_risk_level(volatility):
    if volatility < 18:
        return "Low"
    elif volatility < 30:
        return "Medium"
    else:
        return "High"


def write_market_reports():
    path = os.path.join(RAW_DIR, "market_reports.txt")

    lines = []
    lines.append("WEB-SOURCED MARKET REPORTS")
    lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("Source: Yahoo Finance via yfinance historical market data")
    lines.append("=" * 80)

    for ticker, index_name in INDEX_TICKERS.items():
        df = safe_download(ticker, period="1y")

        if df is None:
            lines.append(f"\nData unavailable for {index_name} ({ticker}).")
            continue

        metrics = calculate_metrics(df)

        lines.append(f"\nMarket Index: {index_name} ({ticker})")
        lines.append(f"One-year starting price: {metrics['start_price']}")
        lines.append(f"Latest price: {metrics['end_price']}")
        lines.append(f"One-year return: {metrics['total_return']}%")
        lines.append(f"Annualized volatility: {metrics['annualized_volatility']}%")
        lines.append(f"One-year high: {metrics['max_price']}")
        lines.append(f"One-year low: {metrics['min_price']}")

        if metrics["total_return"] > 10:
            sentiment = "positive"
        elif metrics["total_return"] < -5:
            sentiment = "negative"
        else:
            sentiment = "mixed or neutral"

        lines.append(
            f"Market interpretation: The {index_name} showed a {sentiment} trend "
            f"over the last one year based on price return and volatility."
        )

    with open(path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))

    print(f"Created {path}")


def write_historical_data():
    path = os.path.join(RAW_DIR, "historical_data.txt")

    lines = []
    lines.append("WEB-SOURCED HISTORICAL STOCK DATA")
    lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("Source: Yahoo Finance via yfinance")
    lines.append("=" * 80)

    for ticker, sector in TICKERS.items():
        df = safe_download(ticker, period="1y")

        if df is None:
            lines.append(f"\nData unavailable for {ticker}.")
            continue

        metrics = calculate_metrics(df)
        risk_level = get_risk_level(metrics["annualized_volatility"])

        lines.append(f"\nTicker: {ticker}")
        lines.append(f"Sector: {sector}")
        lines.append(f"One-year starting price: {metrics['start_price']}")
        lines.append(f"Latest price: {metrics['end_price']}")
        lines.append(f"One-year return: {metrics['total_return']}%")
        lines.append(f"Annualized volatility: {metrics['annualized_volatility']}%")
        lines.append(f"One-year high: {metrics['max_price']}")
        lines.append(f"One-year low: {metrics['min_price']}")
        lines.append(f"Calculated risk level based on volatility: {risk_level}")

    with open(path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))

    print(f"Created {path}")


def write_sector_outlook():
    path = os.path.join(RAW_DIR, "sector_outlook.txt")

    sector_data = {}

    for ticker, sector in TICKERS.items():
        df = safe_download(ticker, period="1y")

        if df is None:
            continue

        metrics = calculate_metrics(df)

        if sector not in sector_data:
            sector_data[sector] = []

        sector_data[sector].append(metrics)

    lines = []
    lines.append("WEB-SOURCED SECTOR OUTLOOK")
    lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("Source: Yahoo Finance via yfinance")
    lines.append("=" * 80)

    for sector, metrics_list in sector_data.items():
        avg_return = np.mean([m["total_return"] for m in metrics_list])
        avg_volatility = np.mean([m["annualized_volatility"] for m in metrics_list])

        risk_level = get_risk_level(avg_volatility)

        if avg_return > 10:
            outlook = "positive"
        elif avg_return < -5:
            outlook = "weak"
        else:
            outlook = "neutral or mixed"

        lines.append(f"\nSector: {sector}")
        lines.append(f"Average one-year return of selected stocks: {round(avg_return, 2)}%")
        lines.append(f"Average annualized volatility: {round(avg_volatility, 2)}%")
        lines.append(f"Sector risk level: {risk_level}")
        lines.append(
            f"Sector outlook: The {sector} sector appears {outlook} based on "
            f"recent one-year price performance and volatility of selected listed companies."
        )

    with open(path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))

    print(f"Created {path}")


def extract_news_items(ticker):
    try:
        stock = yf.Ticker(ticker)
        news_items = stock.news

        results = []

        if not news_items:
            return results

        for item in news_items[:5]:
            title = item.get("title", "")
            publisher = item.get("publisher", "")
            link = item.get("link", "")

            if title:
                results.append({
                    "title": title,
                    "publisher": publisher,
                    "link": link
                })

        return results

    except Exception as e:
        print(f"News unavailable for {ticker}: {e}")
        return []


def write_stock_news():
    path = os.path.join(RAW_DIR, "stock_news.txt")

    lines = []
    lines.append("WEB-SOURCED STOCK NEWS")
    lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("Source: Yahoo Finance news via yfinance")
    lines.append("=" * 80)

    for ticker, sector in TICKERS.items():
        lines.append(f"\nTicker: {ticker}")
        lines.append(f"Sector: {sector}")

        news_items = extract_news_items(ticker)

        if not news_items:
            lines.append("No recent news items available from yfinance for this ticker.")
            continue

        for idx, news in enumerate(news_items, start=1):
            lines.append(f"{idx}. Title: {news['title']}")
            lines.append(f"   Publisher: {news['publisher']}")
            lines.append(f"   Link: {news['link']}")

    with open(path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))

    print(f"Created {path}")


def write_risk_commentary():
    path = os.path.join(RAW_DIR, "risk_commentary.txt")

    lines = []
    lines.append("WEB-SOURCED RISK COMMENTARY")
    lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("Source: Yahoo Finance historical prices via yfinance")
    lines.append("=" * 80)

    stock_metrics = []

    for ticker, sector in TICKERS.items():
        df = safe_download(ticker, period="1y")

        if df is None:
            continue

        metrics = calculate_metrics(df)
        metrics["ticker"] = ticker
        metrics["sector"] = sector
        metrics["risk_level"] = get_risk_level(metrics["annualized_volatility"])

        stock_metrics.append(metrics)

    sorted_by_volatility = sorted(
        stock_metrics,
        key=lambda x: x["annualized_volatility"],
        reverse=True
    )

    lines.append("\nVolatility Ranking:")
    for item in sorted_by_volatility:
        lines.append(
            f"{item['ticker']} | Sector: {item['sector']} | "
            f"Volatility: {item['annualized_volatility']}% | "
            f"Risk Level: {item['risk_level']} | "
            f"One-year Return: {item['total_return']}%"
        )

    lines.append("\nPortfolio Risk Interpretation:")
    lines.append(
        "Stocks with higher annualized volatility may increase portfolio drawdown risk. "
        "A portfolio concentrated in one sector may face concentration risk. "
        "Diversification across banking, IT, FMCG, automobile, and energy sectors can reduce overall exposure."
    )

    lines.append("\nRisk Appetite Mapping:")
    lines.append(
        "Low-risk investors may prefer lower-volatility large-cap and defensive-sector exposure."
    )
    lines.append(
        "Medium-risk investors may combine large-cap stocks, index exposure, and selected sector allocation."
    )
    lines.append(
        "High-risk investors may accept higher volatility and larger equity exposure, but may face larger drawdowns."
    )

    lines.append(
        "\nDisclaimer: This risk commentary is generated for educational purposes only "
        "and is not financial advice."
    )

    with open(path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))

    print(f"Created {path}")


def main():
    write_market_reports()
    write_stock_news()
    write_historical_data()
    write_sector_outlook()
    write_risk_commentary()

    print("\nAll web-sourced financial text files created successfully inside data/raw/")


if __name__ == "__main__":
    main()

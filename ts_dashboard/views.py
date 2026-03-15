# ts_dashboard/views.py
from django.shortcuts import render
from django.conf import settings
import os

import matplotlib
matplotlib.use("Agg")  # important for servers (no GUI)
import matplotlib.pyplot as plt

from collections import namedtuple
from tslearn.data_loader import build_stock_uts
from tslearn.time_series import TimeSeriesFactory

def home(request):
    """
    notebook: framework_for_time_series_data/nlp_ts/paper-daily-sse_stock-ts_models.ipynb
    
    """
    start_date, end_date = "2025-11-10", "2026-11-10"
    Stock = namedtuple("Stock", ["symbol", "name"])

    stocks = [
        Stock("MSFT", "Microsoft"),
        Stock("INTC", "Intel"),
    ]

    independent_variable = "Close"

    stocks = {
        s.symbol: build_stock_uts(
            s.symbol,
            s.name,
            independent_variable,
            start_date=start_date,
            end_date=end_date,
            frequency="1h",
        )
        for s in stocks
    }

    stock_symbol = "MSFT"
    stock_of_interest = stocks[stock_symbol]
    stock_df = stock_of_interest.get_as_df()  # must include time + Close

    # ---- make a chart image and save it into static ----
    plt.figure(figsize=(10, 4))
    plt.plot(stock_df.index, stock_df[independent_variable])
    plt.title(f"{stock_symbol} ({independent_variable})")
    plt.xlabel("Date")
    plt.ylabel(independent_variable)
    plt.tight_layout()

    out_dir = os.path.join(settings.BASE_DIR, "ts_dashboard", "static", "ts_dashboard")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "msft.png")
    plt.savefig(out_path, dpi=150)
    plt.close()

    time_type = 'hours'
    stock_data = True

    get_stats = stock_of_interest.get_statistics(time_type, stock_data)

    # give template the static path
    context = {"chart_path": "ts_dashboard/msft.png", 
               "symbol": stock_symbol,
               "stats": get_stats
               }
    return render(request, "ts_dashboard/base.html", context)
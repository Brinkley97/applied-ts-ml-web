# AFTER: same URL (/dashboard_home/) every time, but reads query params from the URL
# Example URL:
# /dashboard_home/?symbol=MSFT&start_date=2026-03-05&end_date=2026-03-10&forecast=24

from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.conf import settings
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from tslearn.data_loader import build_stock_uts

ALLOWED_SYMBOLS = {"MSFT": "Microsoft", "INTC": "Intel", "AAPL": "Apple"}

def home(request):
    # Defaults (used when query params are missing)
    symbol = request.GET.get("symbol", "MSFT").upper()
    start_date = request.GET.get("start_date", "2026-03-05")
    end_date = request.GET.get("end_date", "2026-03-10")
    forecast_raw = request.GET.get("forecast", "24")

    # Validate
    if symbol not in ALLOWED_SYMBOLS:
        return HttpResponseBadRequest("Invalid symbol.")

    try:
        forecast_steps = int(forecast_raw)
        if forecast_steps < 1:
            raise ValueError
    except ValueError:
        return HttpResponseBadRequest("Forecast must be a positive integer.")

    if not start_date or not end_date or end_date <= start_date:
        return HttpResponseBadRequest("End date must be after start date.")

    metric = "Close"
    frequency = "1h"

    ts = build_stock_uts(
        symbol,
        ALLOWED_SYMBOLS[symbol],
        metric,
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
    )
    df = ts.get_as_df()

    # Save chart (still PNG for now)
    plt.figure(figsize=(10, 4))
    plt.plot(df.index, df[metric])
    plt.title(f"{symbol} ({metric})")
    plt.tight_layout()

    out_dir = os.path.join(settings.BASE_DIR, "ts_dashboard", "static", "ts_dashboard")
    os.makedirs(out_dir, exist_ok=True)
    filename = f"{symbol.lower()}.png"
    out_path = os.path.join(out_dir, filename)
    plt.savefig(out_path, dpi=150)
    plt.close()

    stats = ts.get_statistics(time_type="hours", type_of_data=metric)

    action = request.GET.get("action", "")
    stationarity = None
    if action == "stationarity":
        series = ts.get_series()
        stationarity = ts.stationarity_test(series)

    context = {
        "chart_url": f"{settings.STATIC_URL}ts_dashboard/{filename}",
        "forecast_chart_url": None,  # placeholder until forecast is implemented
        "symbol": symbol,
        "stats": stats,
        "stationarity": stationarity,
        "forecast_steps": forecast_steps,
        "form_symbol": symbol,
        "form_start_date": start_date,
        "form_end_date": end_date,
        "form_forecast": forecast_steps,
    }
    return render(request, "ts_dashboard/base.html", context)
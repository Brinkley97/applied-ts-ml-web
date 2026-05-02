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
from tslearn.ts_models import RandomWalk, EvaluationMetric

ALLOWED_SYMBOLS = {
    "MSFT": "Microsoft",
    "INTC": "Intel",
    "AAPL": "Apple",
}

def _get_validated_inputs(request):
    """
    Shared helper: read + validate common GET inputs.
    Returns a dict of clean values or raises HttpResponseBadRequest.
    """
    symbol = request.GET.get("symbol", "MSFT").upper()
    start_date = request.GET.get("start_date", "2026-03-05")
    end_date = request.GET.get("end_date", "2026-03-10")

    if symbol not in ALLOWED_SYMBOLS:
        return None, HttpResponseBadRequest(
            f"Invalid symbol '{symbol}'. Allowed: {list(ALLOWED_SYMBOLS.keys())}"
        )
    if not start_date or not end_date:
        return None, HttpResponseBadRequest("Start date and end date are required.")
    if end_date <= start_date:
        return None, HttpResponseBadRequest("End date must be after start date.")

    return {
        "symbol": symbol,
        "start_date": start_date,
        "end_date": end_date,
    }, None


def home(request):
    """
    Load original chart + summary stats + optional stationarity test.

    URL: /dashboard_home/
    Actions:
        (empty)      — chart + stats only
        stationarity — also run ADF stationarity test
    """
    inputs, error = _get_validated_inputs(request)
    if error:
        return error

    symbol = inputs["symbol"]
    start_date = inputs["start_date"]
    end_date = inputs["end_date"]
    action = request.GET.get("action", "")
    metric = "Close"
    frequency = "1h"

    # Build time series
    ts = build_stock_uts(
        symbol,
        ALLOWED_SYMBOLS[symbol],
        metric,
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
    )
    df = ts.get_as_df()

    # Save original chart
    out_dir = os.path.join(settings.BASE_DIR, "ts_dashboard", "static", "ts_dashboard")
    os.makedirs(out_dir, exist_ok=True)
    original_filename = f"{symbol.lower()}_original.png"
    plt.figure(figsize=(10, 4))
    plt.plot(df.index, df[metric])
    plt.title(f"{symbol} ({metric}) — Original")
    plt.xlabel("Date")
    plt.ylabel(metric)
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, original_filename), dpi=150)
    plt.close()

    # Summary stats
    stats = ts.get_statistics(time_type="hours", type_of_data=metric)

    # Stationarity (only if requested)
    stationarity = None
    if action == "stationarity":
        stationarity = ts.stationarity_test(ts.get_series())

    context = {
        "chart_url": f"{settings.STATIC_URL}ts_dashboard/{original_filename}",
        "forecast_chart_url": None,
        "symbol": symbol,
        "stats": stats,
        "stationarity": stationarity,
        "forecast_metrics": None,
        "form_symbol": symbol,
        "form_start_date": start_date,
        "form_end_date": end_date,
        "form_forecast": 24,
    }
    return render(request, "ts_dashboard/home.html", context)


def forecast(request):
    """
    Run Random Walk forecast and return chart + metrics.
    Called when user clicks "Run Forecast" button.

    URL: /dashboard_home/
    Action: forecast
    """
    inputs, error = _get_validated_inputs(request)
    if error:
        return error

    symbol = inputs["symbol"]
    start_date = inputs["start_date"]
    end_date = inputs["end_date"]
    metric = "Close"
    frequency = "1h"

    # Validate forecast steps
    forecast_raw = request.GET.get("forecast", "24")
    try:
        forecast_steps = int(forecast_raw)
        if forecast_steps < 1:
            raise ValueError
    except ValueError:
        return HttpResponseBadRequest("Forecast steps must be a positive integer.")

    # Build time series
    ts = build_stock_uts(
        symbol,
        ALLOWED_SYMBOLS[symbol],
        metric,
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
    )
    df = ts.get_as_df()

    # Save original chart (still needed for context)
    out_dir = os.path.join(settings.BASE_DIR, "ts_dashboard", "static", "ts_dashboard")
    os.makedirs(out_dir, exist_ok=True)
    original_filename = f"{symbol.lower()}_original.png"
    plt.figure(figsize=(10, 4))
    plt.plot(df.index, df[metric])
    plt.title(f"{symbol} ({metric}) — Original")
    plt.xlabel("Date")
    plt.ylabel(metric)
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, original_filename), dpi=150)
    plt.close()

    # Summary stats
    stats = ts.get_statistics(time_type="hours", type_of_data=metric)

    # Train/test split
    N = len(ts.get_series())
    train_length = N - forecast_steps
    train_uts, test_uts = ts.get_slice(1, train_length, both_train_test=True)
    train_df = train_uts.get_as_df()
    test_df = test_uts.get_as_df()
    train_col = train_df.columns[0]
    test_col = test_df.columns[0]

    # Run Random Walk model
    rw_model = RandomWalk(train_type_name="full")
    rw_predictions = rw_model.predict(train_df, test_df)
    rw_mse = EvaluationMetric.eval_mse(test_df, rw_predictions, per_element=False)
    rw_rmse = EvaluationMetric.eval_rmse(test_df, rw_predictions, per_element=False)
    rw_mae = EvaluationMetric.eval_mae(test_df, rw_predictions, per_element=False)
    rw_mape = EvaluationMetric.eval_mape(test_df, rw_predictions, per_element=False)

    # Save forecast chart
    forecast_filename = f"{symbol.lower()}_forecast.png"
    plt.figure(figsize=(10, 4))
    plt.plot(train_df.index, train_df[train_col], label="Train")
    plt.plot(test_df.index, test_df[test_col], label="Actual")
    plt.plot(
        test_df.index,
        rw_predictions,
        label="Forecast (Random Walk)",
        linestyle="--",
    )
    plt.title(f"{symbol} — Random Walk Forecast ({forecast_steps} steps)")
    plt.xlabel("Date")
    plt.ylabel(metric)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, forecast_filename), dpi=150)
    plt.close()

    forecast_metrics = {
        "Model": "Random Walk",
        "Forecast Steps": forecast_steps,
        "MSE": round(float(rw_mse), 4) if rw_mse is not None else "N/A",
        "RMSE": round(float(rw_rmse), 4) if rw_rmse is not None else "N/A",
        "MAE": round(float(rw_mae), 4) if rw_mae is not None else "N/A",
        "MAPE": round(float(rw_mape), 4) if rw_mape is not None else "N/A",
    }

    context = {
        "chart_url": f"{settings.STATIC_URL}ts_dashboard/{original_filename}",
        "forecast_chart_url": f"{settings.STATIC_URL}ts_dashboard/{forecast_filename}",
        "symbol": symbol,
        "stats": stats,
        "stationarity": None,
        "forecast_metrics": forecast_metrics,
        "form_symbol": symbol,
        "form_start_date": start_date,
        "form_end_date": end_date,
        "form_forecast": forecast_steps,
    }
    return render(request, "ts_dashboard/forecast.html", context)
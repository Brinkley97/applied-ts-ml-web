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

def home(request):
    """
    Main dashboard view for the time series forecasting app.
    Notebook reference: framework_for_time_series_data/nlp_ts/paper-daily-sse_stock-ts_models.ipynb

    URL: /dashboard_home/
    Example: /dashboard_home/?symbol=MSFT&start_date=2026-03-05&end_date=2026-03-10&forecast=24&action=forecast
    Actions:
        (empty)       — load chart + stats only
        stationarity  — also run ADF stationarity test
        forecast      — also run Random Walk forecast
    """

    # ---------------------------------------------------------------
    # 1) Read inputs from GET query params (with safe defaults)
    # ---------------------------------------------------------------
    symbol = request.GET.get("symbol", "MSFT").upper()
    start_date = request.GET.get("start_date", "2026-03-05")
    end_date = request.GET.get("end_date", "2026-03-10")
    forecast_raw = request.GET.get("forecast", "24")
    action = request.GET.get("action", "")

    # ---------------------------------------------------------------
    # 2) Validate inputs
    # ---------------------------------------------------------------
    if symbol not in ALLOWED_SYMBOLS:
        return HttpResponseBadRequest(f"Invalid symbol '{symbol}'. Allowed: {list(ALLOWED_SYMBOLS.keys())}")

    try:
        forecast_steps = int(forecast_raw)
        if forecast_steps < 1:
            raise ValueError
    except ValueError:
        return HttpResponseBadRequest("Forecast steps must be a positive integer.")

    if not start_date or not end_date:
        return HttpResponseBadRequest("Start date and end date are required.")
    if end_date <= start_date:
        return HttpResponseBadRequest("End date must be after start date.")

    # ---------------------------------------------------------------
    # 3) Build time series from backend library
    # ---------------------------------------------------------------
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

    # ---------------------------------------------------------------
    # 4) Save original chart
    # ---------------------------------------------------------------
    out_dir = os.path.join(
        settings.BASE_DIR, "ts_dashboard", "static", "ts_dashboard"
    )
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

    # ---------------------------------------------------------------
    # 5) Summary stats (always computed)
    # ---------------------------------------------------------------
    stats = ts.get_statistics(time_type="hours", type_of_data=metric)

    # ---------------------------------------------------------------
    # 6) Stationarity test (only if action == "stationarity")
    # ---------------------------------------------------------------
    stationarity = None
    if action == "stationarity":
        stationarity = ts.stationarity_test(ts.get_series())

    # ---------------------------------------------------------------
    # 7) Forecast (only if action == "forecast")
    # ---------------------------------------------------------------
    forecast_chart_url = None
    forecast_metrics = None

    if action == "forecast":
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
        # plt.plot(train_df.index, train_df[metric], label="Train")
        # plt.plot(test_df.index, test_df[metric], label="Actual")

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

        forecast_chart_url = f"{settings.STATIC_URL}ts_dashboard/{forecast_filename}"
        forecast_metrics = {
            "Model": "Random Walk",
            "Forecast Steps": forecast_steps,
            "MSE": round(float(rw_mse), 4) if rw_mse is not None else "N/A",
            "RMSE": round(float(rw_rmse), 4) if rw_rmse is not None else "N/A",
            "MAE": round(float(rw_mae), 4) if rw_mae is not None else "N/A",
            "MAPE": round(float(rw_mape), 4) if rw_mape is not None else "N/A",
        }

    # ---------------------------------------------------------------
    # 8) Build context and render
    # ---------------------------------------------------------------
    context = {
        # chart URLs
        "chart_url": f"{settings.STATIC_URL}ts_dashboard/{original_filename}",
        "forecast_chart_url": forecast_chart_url,
        # data
        "symbol": symbol,
        "stats": stats,
        "stationarity": stationarity,
        "forecast_metrics": forecast_metrics,
        # form state (keeps form filled in after submit)
        "form_symbol": symbol,
        "form_start_date": start_date,
        "form_end_date": end_date,
        "form_forecast": forecast_steps,
    }
    return render(request, "ts_dashboard/base.html", context)
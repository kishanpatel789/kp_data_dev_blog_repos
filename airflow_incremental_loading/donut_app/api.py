from datetime import datetime, date, timedelta, timezone
import logging

from faker import Faker
from flask import Flask, request
import polars as pl

fake = Faker()

logging.basicConfig(
    level=logging.INFO,
    format="{asctime} - {levelname} - {message}",
    style="{",
)


def get_orders_for_day(day: date):

    next_day = day + timedelta(days=1)
    orders = []
    for _ in range(fake.random_int(1, 100)):
        order = (
            fake.user_name(),
            fake.random_int(1, 50) * 6,
            fake.date_time_between_dates(
                day,
                next_day,
                timezone.utc,
            ),
        )
        orders.append(order)

    df = pl.from_records(
        orders, schema=["user_name", "num_donuts", "order_time"], orient="row"
    )

    return df


def get_orders_for_last_14_days(dt: date):
    multi_day_orders = pl.concat(
        [get_orders_for_day(day=dt - timedelta(days=(14 - i))) for i in range(14)]
    )
    return multi_day_orders


app = Flask(__name__)
app.config["orders"] = get_orders_for_last_14_days(date.today())


def parse_date_str(date_str):
    if date_str is None:
        return None

    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        logging.error(f"Improper date provided")
        raise
    return dt


@app.route("/orders")
def get_orders():
    start_date = parse_date_str(request.args.get("start_date", None))
    end_date = parse_date_str(request.args.get("end_date", None))

    orders = app.config["orders"]

    if start_date is not None:
        logging.debug(f"Filtering orders by start_date '{start_date}'")
        orders = orders.filter(pl.col("order_time") >= start_date)

    if end_date is not None:
        logging.debug(f"Filtering orders by end_date '{end_date}'")
        orders = orders.filter(pl.col("order_time") < end_date)

    return orders.to_dicts()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

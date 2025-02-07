from datetime import datetime, date, timedelta, timezone
from pprint import pprint
import logging

from faker import Faker
from flask import Flask, jsonify
import polars as pl

app = Flask(__name__)
fake = Faker()


def get_orders_for_day(day: date):

    next_day = day + timedelta(days=1)
    orders = []
    # for _ in range(fake.random_int(10, 12)):
    for _ in range(1):
        order = (
            fake.user_name(),
            fake.random_int(1, 100),
            fake.date_time_between_dates(
                day,
                next_day,
                timezone.utc,
            ).isoformat(),
        )
        orders.append(order)

    df = pl.from_records(
        orders, schema=["user_name", "num_donuts", "datetime"], orient="row"
    )

    return df


def get_orders_for_last_14_days(dt: date):
    multi_day_orders = pl.concat(
        [get_orders_for_day(day=dt - timedelta(days=(14 - i))) for i in range(14)]
    )
    return multi_day_orders


@app.route("/<date_str>")
def get_orders(date_str):
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        logging.error(f"You don goofed")
        raise

    # orders = get_orders_for_day(dt)
    orders = get_orders_for_last_14_days(dt)

    return jsonify(orders.to_dicts())


if __name__ == "__main__":
    # pprint(get_orders_for_day(date.today()))
    app.run(debug=True)

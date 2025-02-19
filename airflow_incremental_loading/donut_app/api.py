from datetime import datetime, date, timedelta, timezone
import logging

from faker import Faker
from fastapi import FastAPI
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


app = FastAPI()
app.state.orders = get_orders_for_last_14_days(date.today())


def parse_date_str(date_str: str | None) -> date | None:
    if date_str is None:
        return None

    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        logging.error(f"Improper date provided")
        raise
    return dt


@app.get("/orders")
def get_orders(start_date: str | None = None, end_date: str | None = None):
    start_dt = parse_date_str(start_date)
    end_dt = parse_date_str(end_date)

    orders = app.state.orders

    if start_dt is not None:
        logging.debug(f"Filtering orders by start_date '{start_dt}'")
        orders = orders.filter(pl.col("order_time") >= start_dt)

    if end_dt is not None:
        logging.debug(f"Filtering orders by end_date '{end_dt}'")
        orders = orders.filter(pl.col("order_time") < end_dt)

    return orders.to_dicts()


# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=5000)

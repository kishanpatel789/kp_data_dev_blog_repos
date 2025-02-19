from datetime import datetime, date, timedelta, timezone
import logging

from faker import Faker
from fastapi import FastAPI
from pydantic import BaseModel
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


description = """
## Donut Order API \U0001f369 \U0001f924
- `/orders`: allows you to get orders from last 14 days
"""
app = FastAPI(
    title="Donut App",
    summary="A delicious API that allows you to order donuts.",
    description=description,
    version="0.0.1",
)
app.state.orders = get_orders_for_last_14_days(date.today())


class Order(BaseModel):
    user_name: str
    num_donuts: int
    order_time: datetime


@app.get("/", tags=["root"], include_in_schema=False)
def health_check():
    return {"status": "ok"}


@app.get("/orders", response_model=list[Order], tags=["orders"])
def get_orders(start_date: date | None = None, end_date: date | None = None):
    orders = app.state.orders

    if start_date is not None:
        logging.debug(f"Filtering orders by start_date '{start_date}'")
        orders = orders.filter(pl.col("order_time") >= start_date)

    if end_date is not None:
        logging.debug(f"Filtering orders by end_date '{end_date}'")
        orders = orders.filter(pl.col("order_time") < end_date)

    return orders.to_dicts()

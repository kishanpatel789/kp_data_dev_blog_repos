from faker import Faker
from datetime import datetime, date, timedelta, timezone
from pprint import pprint

fake = Faker()

def get_orders_for_day(input_date: date):
    
    next_date = input_date + timedelta(days=1)
    orders = []

    for _ in range(fake.random_int(10, 100)):
        order = (
            fake.user_name(),
            fake.random_int(1, 100),
            fake.date_time_between_dates(
                input_date, 
                next_date,
                timezone.utc,
            ).isoformat()
        )

        orders.append(order)
    
    return orders

def get_orders_for_last_14_days():
    pass

if __name__ == "__main__":
    pprint(get_orders_for_day(date.today()))
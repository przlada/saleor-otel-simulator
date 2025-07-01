import random
import threading
import time
import os

import requests
from opentelemetry import trace

from storefront_queries import CATEGORY_DETAILS, CHECKOUT_CREATE, USER_DETAILS

tracer = trace.get_tracer("saleor.service")


VARIABLES = {
    "channel": "default-channel",
    "variantID": "UHJvZHVjdFZhcmlhbnQ6Mzg2",
    "quantity": 1,
    "address": {
        "firstName": "John",
        "lastName": "Doe",
        "streetAddress1": "t",
        "city": "Wroclaw",
        "country": "PL",
        "postalCode": "50-345",
    },
}

BASE_URL = "http://api:8000/graphql/"


def checkout_create():
    data = {
        "query": CHECKOUT_CREATE,
        "variables": VARIABLES,
        "operationName": "checkoutCreate",
    }
    response = requests.post(BASE_URL, json=data)
    if response.status_code != 200:
        print("ERROR - checkout_create")


def category_details():
    variables = {
        "attributes": {},
        "pageSize": 6,
        "priceGte": None,
        "priceLte": None,
        "sortBy": None,
        "channel": "default-channel",
        "id": "Q2F0ZWdvcnk6MjA=",
    }
    data = {
        "query": CATEGORY_DETAILS,
        "variables": variables,
        "operationName": "CategoryProducts",
    }
    response = requests.post(BASE_URL, json=data)
    if response.status_code != 200:
        print("ERROR - CATEGORY_DETAILS")


def user_details():
    data = {
        "query": USER_DETAILS,
        "operationName": "UserDetails",
    }
    response = requests.post(BASE_URL, json=data)
    if response.status_code != 200:
        print("ERROR - UserDetails")


OPERATIONS = {
    "checkoutCreate": checkout_create,
    "userDetails": user_details,
    "categoryDetails": category_details,
}


def worker():
    while True:
        name, operation = random.choice(list(OPERATIONS.items()))
        with tracer.start_as_current_span(name):
            operation()
        time.sleep(random.random() * float(os.getenv("MAX_SLEEP", 5)))


print("Starting storefront simulator!")
delay = float(os.environ.get("STARTUP_DELAY", 25))
print(f"Initial delay {delay}s")
time.sleep(delay)
workers_count = int(os.environ.get("WORKERS_COUNT", 3))
print(f"Starting {workers_count} workers")
threads = []
for i in range(workers_count):
    thread = threading.Thread(target=worker)
    threads.append(thread)
    thread.start()


for thread in threads:
    thread.join()

print("All threads completed")

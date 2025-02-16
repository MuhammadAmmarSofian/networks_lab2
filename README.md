# Fake Food Delivery API - McDonald's Clone

## Description

This project is a REST API for a fake food delivery system using FastAPI. It allows managing a menu for a single restaurant (McDonald's) and includes endpoints for creating, retrieving, updating, and deleting menu items. The API also supports image uploads, sorting, filtering, and batch operations.

## Setup Instructions

Clone the Repository

$ git clone https://github.com/MuhammadAmmarSofian/networks_lab2

$ docker compose up --build

API will be available at: http://127.0.0.1:8000

## API Endpoints & Examples

### GET Requests


Get all menu items:

GET /menu


Get menu items sorted by price:

GET /menu?sortBy=price


Get top 3 menu items:

GET /menu?count=3


Get a single menu item by ID:

GET /menu/{item_id}


### POST Requests


Add a new menu item:

POST /menu
{
    "item_id": "7",
    "name": "Big Mac",
    "price": 5.99,
    "category": "Burger"
}


### PUT Requests


Update a menu item:

PUT /menu/{item_id}
{
    "item_id": "1",
    "name": "Cheeseburger Deluxe",
    "price": 3.49,
    "category": "Burger"
}


Batch update prices:

PUT /menu/batch_update
{
    "category": "Burger",
    "price_change_percent": 10
}


### DELETE Requests

Delete a single menu item:

DELETE /menu/{item_id}

Batch delete items by category:

DELETE /menu/batch_delete?category=Burger



## Idempotency Analysis

### Idempotent Routes:

These routes return the same response when called multiple times with the same input:

GET /menu → Fetching menu items does not change the state.

GET /menu/{item_id} → Fetching a specific item is read-only.

DELETE /menu/{item_id} → If the item exists, it is deleted; if repeated, it returns 404 (same result).

DELETE /menu/batch_delete → Deleting items by condition will always return the same response if repeated.

PUT /menu/{item_id} → Updating an item with the same data multiple times has no extra effect.


### Non-Idempotent Routes

These routes modify the state and return different results on repeated calls:

POST /menu → Creating a new item multiple times adds duplicates.

PUT /menu/batch_update → Increases prices each time it is called.

📌 Notes

Ensure the API is running before sending requests.

Use Postman or curl for API testing.
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

Example Result:

[
    {
        "item_id": "1",
        "name": "Cheeseburger",
        "price": 3.0,
        "category": "Burger"
    },
    {
        "item_id": "2",
        "name": "McChicken",
        "price": 3.5,
        "category": "Burger"
    },
    {
        "item_id": "3",
        "name": "Coke",
        "price": 1.0,
        "category": "Drink"
    },
    {
        "item_id": "4",
        "name": "Prosperity Burger",
        "price": 10.0,
        "category": "Burger"
    },
    {
        "item_id": "5",
        "name": "French Fries",
        "price": 2.5,
        "category": "Side"
    },
    {
        "item_id": "6",
        "name": "McFlurry",
        "price": 3.2,
        "category": "Dessert"
    }
]


Get menu items sorted by price:

GET /menu?sortBy=price

Example result:

[
    {
        "item_id": "3",
        "name": "Coke",
        "price": 1.0,
        "category": "Drink"
    },
    {
        "item_id": "5",
        "name": "French Fries",
        "price": 2.5,
        "category": "Side"
    },
    {
        "item_id": "1",
        "name": "Cheeseburger",
        "price": 3.0,
        "category": "Burger"
    },
    {
        "item_id": "6",
        "name": "McFlurry",
        "price": 3.2,
        "category": "Dessert"
    },
    {
        "item_id": "2",
        "name": "McChicken",
        "price": 3.5,
        "category": "Burger"
    },
    {
        "item_id": "4",
        "name": "Prosperity Burger",
        "price": 10.0,
        "category": "Burger"
    }
]


Get menu items sorted by category:

GET /menu?sortBy=category

Example result:

[
    {
        "item_id": "1",
        "name": "Cheeseburger",
        "price": 2.99,
        "category": "Burger"
    },
    {
        "item_id": "2",
        "name": "McChicken",
        "price": 3.49,
        "category": "Burger"
    },
    {
        "item_id": "4",
        "name": "Prosperity Burger",
        "price": 10.0,
        "category": "Burger"
    },
    {
        "item_id": "6",
        "name": "McFlurry",
        "price": 3.2,
        "category": "Dessert"
    },
    {
        "item_id": "3",
        "name": "Coke",
        "price": 1.0,
        "category": "Drink"
    },
    {
        "item_id": "5",
        "name": "French Fries",
        "price": 2.5,
        "category": "Side"
    }
]

Get top 3 menu items:

GET /menu?count=3

Example result:

[
    {
        "item_id": "1",
        "name": "Cheeseburger",
        "price": 3.0,
        "category": "Burger"
    },
    {
        "item_id": "2",
        "name": "McChicken",
        "price": 3.5,
        "category": "Burger"
    },
    {
        "item_id": "3",
        "name": "Coke",
        "price": 1.0,
        "category": "Drink"
    }
]

Get a single menu item by ID:

GET /menu/{item_id}

Example result:

{
    "item_id": "6",
    "name": "McFlurry",
    "price": 3.2,
    "category": "Dessert"
}

Get the image of a menu item:

GET /menu_image/{item_id}

Example result (if image exists):

image of menu_item

### POST Requests

Add a new menu item:

POST /menu
{
    "item_id": "7",
    "name": "Big Mac",
    "price": 5.50,
    "category": "Burger"
}

Example result:

{
    "item_id": "7",
    "name": "Big Mac",
    "price": 5.5,
    "category": "Burger"
}

Alternative case: Missing Field

{
    "name": "Big Mac",
    "price": 5.50,
    "category": "Burger"
}

Expected result:
{
    "detail": [
        {
            "type": "missing",
            "loc": [
                "body",
                "item_id"
            ],
            "msg": "Field required",
            "input": {
                "name": "Big Mac",
                "price": 5.5,
                "category": "Burger"
            }
        }
    ]
}

Upload image for menu item:

POST /upload_menu_image

Key-value:
file - cheeseburger.jpeg
item_id - 1

Example result:
{
    "message": "Image uploaded for item 1"
}

### PUT Requests


Update a menu item:

PUT /menu/{item_id}
{
    "item_id": "1",
    "name": "Cheeseburger",
    "price": 3.50,
    "category": "Burger"
}

Example result:

{
    "item_id": "1",
    "name": "Cheeseburger",
    "price": 3.5,
    "category": "Burger"
}

Alternative case: Item being edited does not exist

{
    "item_id": "1",
    "name": "FiletOFish",
    "price": 3.50,
    "category": "Burger"
}

Expected result:
{
    "detail": "Menu item not found"
}

Batch update prices:

PUT /menu/batch_update
{
    "category": "Drink",
    "price_change_percent": 100
}

Example result:

{
    "message": "1 menu items updated"
}

Alternative case: No items belong to the category being updated

{
    "category": "Breakfast",
    "price_change_percent": 100
}

Expected result:

{
    "detail": "No menu items found for the given category"
}

### DELETE Requests

Delete a single menu item:

DELETE /menu/{item_id}

Example result if item_id is nonexistant:

{
    "detail": "Menu item not found"
}

Batch delete items by category:

DELETE /menu/batch_delete?category=Burger

Example result:

{
    "message": "3 menu items deleted"
}

Alternative case: Batch delete finds no matches

http://127.0.0.1:8000/menu/batch_delete?category=Breakfast

Expected result:

{
    "detail": "No matching menu items found to delete."
}

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



from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Query, Body
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import os
from io import BytesIO
from menu_item import MenuItem  
from menu_db import menu  

app = FastAPI()

class MenuItem(BaseModel):
    item_id: str
    name: str
    price: float
    category: Optional[str] = None

class BatchUpdateRequest(BaseModel):
    category: str
    price_change_percent: float

@app.put("/menu/batch_update")
def batch_update(request: BatchUpdateRequest = Body(...)):
    """Update prices of all menu items in a specific category."""
    updated_count = 0
    for item in menu:
        if item["category"] == request.category:
            item["price"] = round(item["price"] * (1 + request.price_change_percent / 100), 2)
            updated_count += 1

    if updated_count == 0:
        raise HTTPException(status_code=404, detail="No menu items found for the given category")

    return {"message": f"{updated_count} menu items updated"}

@app.delete("/menu/batch_delete")
def batch_delete(
    category: Optional[str] = None, 
    min_price: Optional[float] = None, 
    max_price: Optional[float] = None
):
    """Delete all menu items matching a category or within a price range."""
    global menu

    if not category and min_price is None and max_price is None:
        raise HTTPException(status_code=400, detail="Must provide category or price range for batch delete")

    before_count = len(menu)

    menu = [
        item for item in menu
        if not (
            (category and item["category"] == category) or
            (min_price is not None and item["price"] < min_price) or
            (max_price is not None and item["price"] > max_price)
        )
    ]

    deleted_count = before_count - len(menu)

    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="No matching menu items found to delete.")

    return {"message": f"{deleted_count} menu items deleted"}

@app.get("/menu", response_model=List[MenuItem])
def get_menu(
    sortBy: Optional[str] = Query(None, description="Sort menu by any attribute"),
    count: Optional[int] = Query(None, description="Limit the number of items returned")
):
    """Retrieve all menu items with optional sorting and limiting."""
    sorted_menu = menu.copy()
    
    if sortBy and sortBy in sorted_menu[0]:  
        try:
            sorted_menu.sort(key=lambda x: (str(x[sortBy]).lower() if isinstance(x[sortBy], str) else x[sortBy]))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid sorting attribute: {sortBy}")
    
    if count:
        sorted_menu = sorted_menu[:count]
    
    return sorted_menu

@app.get("/menu/{item_id}", response_model=MenuItem)
def get_menu_item(item_id: str):
    """Retrieve a single menu item by ID."""
    for item in menu:
        if item["item_id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Menu item not found")

@app.post("/menu", response_model=MenuItem, status_code=201)
def add_menu_item(item: MenuItem):
    """Add a new menu item."""
    for existing_item in menu:
        if existing_item["item_id"] == item.item_id:
            raise HTTPException(status_code=400, detail="Item ID already exists")
    menu.append(item.dict())
    return item

@app.put("/menu/{item_id}", response_model=MenuItem)
def update_menu_item(item_id: str, item_update: MenuItem):
    """Update an existing menu item."""
    for index, item in enumerate(menu):
        if item["item_id"] == item_id:
            menu[index] = item_update.dict()
            return item_update
    raise HTTPException(status_code=404, detail="Menu item not found")

@app.delete("/menu/{item_id}", status_code=204)
def delete_menu_item(item_id: str):
    """Delete a menu item by ID."""
    global menu
    before_count = len(menu)
    menu = [item for item in menu if item["item_id"] != item_id]
    if len(menu) == before_count:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return {"message": "Menu item deleted successfully"}

@app.post("/upload_menu_image")
def upload_menu_image(file: UploadFile = File(...), item_id: str = Form(...)):
    """Upload an image for a menu item."""
    if file.content_type.startswith("image/"):
        file_path = f"images/{item_id}.png"
        os.makedirs("images", exist_ok=True)
        with open(file_path, 'wb') as f:
            f.write(file.file.read())
        return {"message": f"Image uploaded for item {item_id}"}
    else:
        raise HTTPException(status_code=415, detail="Only image files are allowed.")

@app.get("/menu_image/{item_id}")
def get_menu_image(item_id: str):
    """Retrieve an image for a menu item."""
    file_path = f"images/{item_id}.png"
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return StreamingResponse(BytesIO(f.read()), media_type="image/png")
    else:
        raise HTTPException(status_code=404, detail="Image not found")

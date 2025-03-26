from fastapi import Depends
from sqlalchemy.orm import Session
import logging
from config.database import get_db
from models.item import Item
from schemas.item import ItemSchema
from utils.general import success_response_handler, failed_response_handler

def create_item(item: ItemSchema, db: Session = Depends(get_db)):
    try:
        new_item = Item(name = item.name)
        db.add(new_item)
        db.commit()
        db.refresh(new_item)

        return success_response_handler(status_code = 201, detail = "Item created successfully", data = {"item id": new_item.id, "item name": new_item.name})
    except Exception as e:
        db.rollback()
        logging.error(f"Error in creating new item: {e}")
        return failed_response_handler(status_code = 500, detail = "Error creating new item")
    
def read_item(id: int, db: Session = Depends(get_db)):
    try:
        item = db.query(Item).filter(Item.id == id).first()
        if not item:
            return failed_response_handler(status_code = 404, detail = "Item not found")
        return success_response_handler(status_code = 200, detail = "Item fetched successfully", data = {"item": item.name})
    except Exception as e:
        logging.error(f"Error in reading item: {e}")
        return failed_response_handler(status_code = 500, detail = "Internal Server error")
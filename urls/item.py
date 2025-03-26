from fastapi import APIRouter
from apis.item import create_item, read_item

router = APIRouter(prefix = "/item")

router.post("/")(create_item)
router.get("/{id}")(read_item)
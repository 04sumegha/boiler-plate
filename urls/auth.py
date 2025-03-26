from fastapi import APIRouter
from apis.auth import signup, login

router = APIRouter(prefix = "/auth")

router.post("/signup")(signup)
router.post("/login")(login)
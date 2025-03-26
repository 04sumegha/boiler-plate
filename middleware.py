from fastapi import Request
import jwt
import os
import time
import logging
from utils.general import failed_response_handler
from utils.cache import cache_manager

async def auth_middleware(request: Request, call_next):
    if request.url.path.startswith("/auth"):
        return await call_next(request)

    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        return failed_response_handler(status_code = 401, detail = "Missing or invalid token")
    
    value = await cache_manager.get(token)
    if value is None:
        try:
            payload = jwt.decode(token.split("Bearer ")[1], os.getenv("SECRET_KEY", "boilerplate"), os.getenv("ALGORITHM", "HS256"))
        except Exception as e:
            logging.error(f"Error decoding token: {e}")
            return failed_response_handler(status_code = 401, detail = "Error decoding token")
        
        value = payload.get("user")
        exp_time = payload.get("exp")
        ttl = exp_time - int(time.time())
        await cache_manager.set(token, value, expire = ttl)

    request.state.user = value
    return await call_next(request)
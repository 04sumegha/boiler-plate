from fastapi import HTTPException
from datetime import datetime, timezone
import jwt
import os
import logging
import time

def create_token(username: str):
    try:
        expire_In = int(time.time()) + 86400
        payload = {
            "user": username,
            "exp": expire_In
        }

        return jwt.encode(payload, os.getenv("SECRET_KEY", "boilerplate"), os.getenv("ALGORITHM", "HS256"))
    except Exception as e:
        logging.error(f"Error in token generation: {e}")
        raise HTTPException(status_code = 500, detail = "Token generation failed")
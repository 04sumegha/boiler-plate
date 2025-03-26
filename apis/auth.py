from fastapi import Depends
from sqlalchemy.orm import Session
import logging
from config.database import get_db
from schemas.auth import UserSchema
from models.auth import User
from utils.auth import create_token
from utils.general import failed_response_handler, success_response_handler

def signup(user: UserSchema, db: Session = Depends(get_db)):
    try:
        new_user = User(username = user.username, password = user.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        logging.error(f"Error in signup: {e}")
        return failed_response_handler(status_code = 500, detail = "Error in creating user")
    
    try:
        token = create_token(user.username)
    except Exception as e:
        logging.error(f"Error in token generation: {e}")
        return failed_response_handler(status_code = 500, detail = "Error in token generation. Try logging in.")
    
    return success_response_handler(status_code = 201, detail = "User created successfully", data = {"user": new_user.username, "token": token})

def login(user: UserSchema, db: Session = Depends(get_db)):
    try:
        user_exist = db.query(User).filter(User.username == user.username).first()
        if not user_exist or user.password != user_exist.password:
            return failed_response_handler(status_code = 401, detail = "Invalid Credentials")
        
        token = create_token(user.username)

        return success_response_handler(status_code = 200, detail = "Login successful", data = {"user": user_exist.username, "token": token})
    except Exception as e:
        logging.error(f"Error in login: {e}")
        return failed_response_handler(status_code = 500, detail = "Internal server error")
from datetime import datetime
from pydantic import BaseModel
from cases.database import conn as db
from cases.logger import log, err, Colors
from cases.utils import flash_login
from cases import auth

class User(BaseModel):
    id : int
    email : str
    first_name : str
    last_name : str
    registered_since : datetime
    last_login : datetime
    
class UserAuth(User):
    auth_hash : str

async def get_user(email : str):
    res = await db.fetch_one(
        "SELECT * FROM `users` WHERE `email` = :email", {
            "email": email
        }
    )
    return UserAuth(**res) if res else None

async def update_last_login(email : str):
    await db.execute(
        "UPDATE `users` SET `last_login` = :last_login WHERE `email` = :email", {
            "last_login": datetime.now(),
            "email": email
        }
    )

def logout(request):
    response = flash_login(request, "Logged out successfully.", "success")
    response.delete_cookie(key="token")
    response.delete_cookie(key="token_type")
    return response

def logout_message(request, message, status):
    response = flash_login(request, message, status)
    response.delete_cookie(key="token")
    response.delete_cookie(key="token_type")
    return response

async def change_profile(
    current_user: User,
    new_email : str,
    first_name : str,
    last_name : str
) -> bool:
    if not new_email and not first_name and not last_name:
        return False
    
    query = ["UPDATE `users` SET"]
    params = { "old_email": current_user.email }
    
    if new_email and new_email != current_user.email:
        query.append("`email` = :new_email")
        params = params | { "new_email": new_email }
        
    if first_name and first_name != current_user.first_name:
        query.append("`first_name` = :first_name")
        params = params | { "first_name": first_name }
    
    if last_name and last_name != current_user.last_name:
        query.append("`last_name` = :last_name")
        params = params | { "last_name": last_name }
        
    if len(query) < 2:
        return True
    
    query = ", ".join(query)
    
    # remove the first ,
    idx = query.index(',')
    query = query[:idx]+query[idx+1:]
    
    query += " WHERE `email` = :old_email"
    
    try:
        await db.execute(
            query,
            params
        )
        return True
    except Exception as e:
        err(f"An error occured trying to record profile changes: {Colors.RED}{e}")
        return False
    
async def change_password(
    current_user : User,
    password : str,
    password_old : str,
    password_confirm : str
):
    if password != password_confirm:
        return "Passwords do not match."
    
    if not await auth.authenticate_user(current_user.email, password_old):
        return "Your old password is incorrect."
    try:
        await db.execute(
            "UPDATE `users` SET `auth_hash` = :auth_hash WHERE `email` = :email", {
                "auth_hash": auth.get_password_hash(password),
                "email": current_user.email
            }
        )
    except Exception as e:
        err(f"An error occured trying to change a password: {Colors.RED}{e}")
        return "A database error occured while trying to update your password."
    return True

async def update_last_login(email : str):
    await db.execute(
        "UPDATE `users` SET `last_login` = :last_login WHERE `email` = :email", {
            "last_login": datetime.now(),
            "email": email
        }
    )

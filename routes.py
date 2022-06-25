from datetime import timedelta
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from cases import auth
from datetime import datetime
from cases.utils import flash_dashboard, render_template, flash_login, flash_dashboard
from objects import user

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/")
@router.get("/home")
@router.get("/home/")
async def main_page(request : Request, current_user: user.User = Depends(auth.get_current_user)) -> HTMLResponse:
    if current_user:
        return RedirectResponse("/dashboard")
    
    return render_template("auth.html", request)

# GET
@router.get("/auth/login")
async def auth_login(request : Request, current_user: user.User = Depends(auth.get_current_user)) -> HTMLResponse:
    if current_user:
        return RedirectResponse("/dashboard")
    
    return render_template("auth.html", request)

# POST AUTH
@router.post("/auth/login", response_model=auth.Token)
async def access_token_retrieve(request : Request, email : str = Form(), password : str = Form()):
    if not email or not password:
        return flash_login(request, "Invalid parameters.", "error")
    _user = await auth.authenticate_user(email, password)
    
    if not _user:
        return flash_login(request, "Invalid email or password.", "error")
    
    token_expires = timedelta(minutes=auth.TOKEN_EXPIRITY)
    token = auth.create_access_token(
        data = { "current_user" : _user.email }, expires_delta = token_expires
    )
    
    response = RedirectResponse(
        url = "/dashboard",
        status_code = 302 # 302 FOUND - used for converting post to get
    )
    response.set_cookie(key="token", value=token)
    response.set_cookie(key="token_type", value="bearer")
    _user.last_login = datetime.now()
    await user.update_last_login(_user.email)
    return response

@router.get("/dashboard")
@router.get("/settings/profile")
@router.get("/settings/password")
async def settings_profile(request : Request, current_user: user.User = Depends(auth.get_current_user)):
    if not current_user:
        return flash_login(request, "Please log-in first.", "error")
    
    return render_template("dashboard.html", request, data = current_user)

@router.get("/auth/logout")
async def auth_logout(request : Request, current_user: user.User = Depends(auth.get_current_user)):
    if not current_user:
        return flash_login(request, "You are not logged in.", "error")
    
    return user.logout(request)
    
@router.post("/settings/profile")
async def settings_profile(
    request : Request,
    new_email : str = Form(),
    new_first_name : str = Form(),
    new_last_name : str = Form(),
    current_user: user.User = Depends(auth.get_current_user),
):
    if not current_user:
        return flash_login(request, "Please log-in first.", "error")
    
    res = await user.change_profile(current_user, new_email, new_first_name, new_last_name)
    
    if res == False:
        return flash_dashboard(request, current_user, "Error updating profile.", "error")
    
    if current_user.email != new_email:
        return user.logout_message(request, "Profile updated successfully, please log-in again.",  "success")
    
    current_user.first_name = new_first_name
    current_user.last_name = new_last_name
    return flash_dashboard(request, current_user, "Profile updated successfully.",  "success")
    
    
@router.post("/settings/password")
async def settings_profile(
    request : Request,
    password : str = Form(),
    password_old : str = Form(),
    password_confirm : str = Form(),
    current_user: user.User = Depends(auth.get_current_user),
):
    if not current_user:
        return flash_login(request, "Please log-in first.", "error")
    
    res = await user.change_password(
        current_user,
        password,
        password_old,
        password_confirm
    )
    
    if res != True:
        return flash_dashboard(request, current_user, res, "error")
    
    return user.logout_message(
        request,
        "Account password updated, please log-in again",
        "success"
    )
    
@router.get("/password/get")
async def temp_password_gen(request : Request, p : str):
    return { "password": auth.get_password_hash(p) }


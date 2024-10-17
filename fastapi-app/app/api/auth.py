from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr
from app.db.supabase import supabase
from pathlib import Path
from app.core.config import settings
from gotrue.errors import AuthApiError


router = APIRouter()

# Get the current file's directory
current_dir = Path(__file__).resolve().parent
# Go up one level to the 'app' directory, then into 'templates'
templates_dir = current_dir.parent / "templates"

templates = Jinja2Templates(directory=str(templates_dir))

class UserSignUp(BaseModel):
    email: EmailStr
    password: str

class LoginData(BaseModel):
    email: str
    password: str

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    access_token: str
    refresh_token: str
    new_password: str

@router.post("/signup")
async def signup(user: UserSignUp):
    try:
        response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password
        })
        return {"message": "Signup successful. Please check your email for verification."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(response: Response, login_data: LoginData):
    try:
        auth_response = supabase.auth.sign_in_with_password({
            "email": login_data.email,
            "password": login_data.password
        })
        
        # Set cookies
        response.set_cookie(key="access_token", value=auth_response.session.access_token, httponly=True, secure=True, samesite='lax')
        response.set_cookie(key="refresh_token", value=auth_response.session.refresh_token, httponly=True, secure=True, samesite='lax')
        
        # Return tokens in response body as well
        return {
            "access_token": auth_response.session.access_token,
            "refresh_token": auth_response.session.refresh_token,
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logout successful"}

@router.post("/forgot-password")
async def forgot_password(request: PasswordResetRequest):
    try:
        result = supabase.auth.reset_password_email(
            request.email,
            {"redirect_to": settings.formatted_reset_password_url}
        )
        return {"message": "Password reset email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/reset-password", response_class=HTMLResponse)
async def reset_password_page(request: Request):
    return templates.TemplateResponse("reset_password.html", {"request": request})

@router.post("/reset-password")
async def reset_password(reset_data: PasswordReset):
    try:
        # Set the access token for the client
        supabase.auth.set_session(reset_data.access_token,reset_data.refresh_token)
        
        # Update the user's password
        update_response = supabase.auth.update_user({
            "password": reset_data.new_password
        })
        
        if update_response.user:
            return {"message": "Password reset successfully"}
        else:
            raise HTTPException(status_code=400, detail="Password reset failed")
    except AuthApiError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

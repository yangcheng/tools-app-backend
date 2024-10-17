from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from pydantic import BaseModel, EmailStr
from app.db.supabase import supabase

router = APIRouter()

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
        result = supabase.auth.reset_password_email(request.email)
        return {"message": "Password reset email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/reset-password")
async def reset_password(reset_data: PasswordReset):
    try:
        result = supabase.auth.api.update_user(
            reset_data.access_token,
            {"password": reset_data.new_password}
        )
        return {"message": "Password reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


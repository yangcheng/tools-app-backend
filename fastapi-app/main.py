from fastapi import FastAPI, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from supabase import create_client, Client
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, UTC
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)


# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    email: EmailStr
    password: str
    is_admin: bool = False

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    access_token: str
    new_password: str

class UserSignUp(BaseModel):
    email: EmailStr
    password: str

class LoginData(BaseModel):
    email: str
    password: str


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


async def get_current_user(request: Request):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise credentials_exception
    
    try:
        # Verify the access token
        user = supabase.auth.get_user(access_token)
        return user.user, False, None
    except Exception:
        # Access token is invalid, try to refresh
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise credentials_exception
        
        try:
            # Attempt to refresh the session
            new_session = supabase.auth.refresh_session(refresh_token)
            return new_session.user, True, new_session.access_token
        except Exception:
            raise credentials_exception

@app.post("/signup")
async def signup(user: UserSignUp):
    try:
        response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password
        })
        return {"message": "Signup successful. Please check your email for verification."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/login")
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

@app.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logout successful"}


@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    if not current_user["email_confirmed_at"]:
        raise HTTPException(status_code=403, detail="Email not verified")
    return current_user

@app.get("/admin")
async def admin_only(current_user: User = Depends(get_current_user)):
    if not current_user["is_admin"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    return {"message": "Welcome, admin!"}

@app.post("/search")
async def search(query: str, current_user: User = Depends(get_current_user)):
    # Your search logic here
    return {"result": f"Search results for: {query}"}

@app.get("/")
async def root():
    return {"message": "Welcome to the search API"}

@app.post("/forgot-password")
async def forgot_password(request: PasswordResetRequest):
    try:
        result = supabase.auth.reset_password_email(request.email)
        return {"message": "Password reset email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/reset-password")
async def reset_password(reset_data: PasswordReset):
    try:
        result = supabase.auth.api.update_user(
            reset_data.access_token,
            {"password": reset_data.new_password}
        )
        return {"message": "Password reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.middleware("http")
async def token_refresh_middleware(request: Request, call_next):
    response = await call_next(request)
    if hasattr(request.state, 'new_access_token'):
        response.set_cookie(key="access_token", value=request.state.new_access_token, httponly=True, secure=True, samesite='lax')
    return response

@app.middleware("http")
async def protect_routes(request: Request, call_next):
    if request.url.path.startswith("/protected"):
        user, new_token_generated, new_access_token = await get_current_user(request)
        request.state.current_user = user
        if new_token_generated:
            request.state.new_access_token = new_access_token
    return await call_next(request)

@app.get("/protected/search")
async def protected_search(query: str, request: Request):
    current_user = request.state.current_user
    # Your search logic here
    return {"result": f"Search results for: {query}", "user": current_user["email"]}

@app.get("/protected/user")
async def protected_user_info(request: Request):
    current_user = request.state.current_user
    return {"user": current_user}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
